import base64
import io
import json
import math
import os
from pathlib import Path
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from PIL import Image, ImageDraw
from roomplan.model import CATALOG, demo_project, polygon_area, validate_project
from roomplan.reconstruction import reconstruct
from roomplan.storage import save_project, load_project
from roomplan.export import export_svg
from roomplan.providers import ProviderUnavailable, reconstruct_object
from server import Handler

def plan_image():
    image=Image.new('RGB',(1040,700),'white');draw=ImageDraw.Draw(image)
    draw.rectangle((20,20,1020,670),outline='black',width=12)
    draw.line((600,20,600,370),fill='black',width=10);draw.line((600,470,600,670),fill='black',width=10)
    draw.line((600,335,680,335),fill='black',width=10);draw.line((780,335,1020,335),fill='black',width=10)
    stream=io.BytesIO();image.save(stream,format='PNG');return stream.getvalue()

class ModelTests(unittest.TestCase):
    def test_demo_is_65_square_metres_and_two_references(self):
        p,w=validate_project(demo_project());self.assertEqual(w,[])
        self.assertAlmostEqual(sum(polygon_area(r['polygon']) for r in p['rooms']),65)
        for category in {c['category'] for c in CATALOG}: self.assertEqual(sum(c['category']==category for c in CATALOG),2)
    def test_nonfinite_and_duplicate_ids_rejected(self):
        p=demo_project();p['walls'][0]['a'][0]=math.nan
        with self.assertRaises(ValueError): validate_project(p)
        p=demo_project();p['objects'][1]['id']=p['objects'][0]['id']
        with self.assertRaises(ValueError): validate_project(p)
    def test_zero_wall_and_missing_asset_rejected(self):
        p=demo_project();p['walls'][0]['b']=p['walls'][0]['a']
        with self.assertRaises(ValueError): validate_project(p)
    def test_missing_exporter_fields_rejected_at_validation(self):
        for collection,key in [('objects','color'),('objects','name'),('rooms','name'),('rooms','color')]:
            p=demo_project();del p[collection][0][key]
            with self.assertRaises(ValueError): validate_project(p)
    def test_malformed_opening_and_ambiguous_files_rejected(self):
        p=demo_project();p['openings']=[None]
        with self.assertRaises(ValueError): validate_project(p)
        f={'id':'f1','name':'file.bin','mime':'application/octet-stream','data':'YWJj'}
        p=demo_project();p['assets']=[f.copy(),f.copy()]
        with self.assertRaises(ValueError): validate_project(p)
        p=demo_project();p['sources']=[f.copy()];del p['sources'][0]['data']
        with self.assertRaises(ValueError): validate_project(p)
        p=demo_project();p['objects'][0]['assetId']='absent'
        with self.assertRaises(ValueError): validate_project(p)
    def test_portable_roundtrip_preserves_binary_sources_assets_and_settings(self):
        p=demo_project();p['sources']=[{'id':'s1','name':'видео.mp4','mime':'video/mp4','data':base64.b64encode(bytes(range(256))).decode()}]
        p['assets']=[{'id':'a1','name':'custom.glb','mime':'model/gltf-binary','data':base64.b64encode(b'glTF-test-binary').decode()}]
        p['objects'][0]['assetId']='a1';p['customResearch']={'seed':17,'calibration':'manual'}
        raw=save_project(p)
        with zipfile.ZipFile(io.BytesIO(raw)) as z: self.assertIn('sources/000-видео.mp4',z.namelist())
        restored,w=load_project(base64.b64encode(raw).decode());self.assertEqual(p,restored)
    def test_archive_traversal_rejected_without_extracting(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z: z.writestr('../evil','bad');z.writestr('project.json','{}')
        with self.assertRaises(ValueError): load_project(base64.b64encode(stream.getvalue()).decode())
    def test_svg_is_xml_escapes_text_and_contains_furniture(self):
        import xml.etree.ElementTree as ET
        p=demo_project();p['name']='<script>bad & text</script>'
        raw=export_svg(p);root=ET.fromstring(raw)
        self.assertNotIn(b'<script>',raw);self.assertIn(b'65.0',raw)
        self.assertEqual(len(root.findall('.//{http://www.w3.org/2000/svg}title')),len(p['objects']))

class ReconstructionTests(unittest.TestCase):
    def test_plan_follows_input_and_calibrates_metric_width(self):
        f={'name':'test.png','mime':'image/png','data':base64.b64encode(plan_image()).decode()}
        p,w=reconstruct({'mode':'plan','files':[f],'ceilingHeight':3.1,'widthMeters':12})
        validate_project(p)
        xs=[a[0] for wall in p['walls'] for a in [wall['a'],wall['b']]]
        self.assertAlmostEqual(max(xs)-min(xs),12,places=3);self.assertFalse(p['provenance']['isSynthetic'])
        self.assertEqual(p['objects'],[]);self.assertTrue(all(w['height']==3.1 for w in p['walls']))
        self.assertGreater(len(p['walls']),4);self.assertEqual(p['sources'][0]['data'],f['data'])
    def test_blank_image_does_not_fall_back_to_demo(self):
        stream=io.BytesIO();Image.new('RGB',(200,200),'white').save(stream,format='PNG')
        with self.assertRaises(ValueError): reconstruct({'mode':'plan','files':[{'name':'blank.png','mime':'image/png','data':base64.b64encode(stream.getvalue()).decode()}]})
    def test_video_is_explicit_deterministic_stub_and_retains_input(self):
        f={'name':'clip.mp4','mime':'video/mp4','data':base64.b64encode(b'original-video-bytes').decode()}
        p,w=reconstruct({'mode':'video','files':[f]});q,_=reconstruct({'mode':'video','files':[f]})
        self.assertEqual(p['pointCloud'],q['pointCloud']);self.assertFalse(p['provenance']['inputUsedForGeometry'])
        self.assertTrue(w);self.assertGreater(len(p['pointCloud']),100);self.assertEqual(p['sources'][0]['data'],f['data'])
    def test_unconfigured_provider_fails_without_proxy(self):
        with patch.dict(os.environ,{'ROOMPLAN_RECONSTRUCTION_URL':''}):
            with self.assertRaises(ProviderUnavailable): reconstruct_object({'files':[{'name':'chair.png','mime':'image/png','data':'YWJj'}]})

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls): cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_health_and_export_have_correct_types(self):
        with urllib.request.urlopen(self.url+'/api/health') as r: self.assertEqual(json.load(r)['status'],'ok')
        req=urllib.request.Request(self.url+'/api/export/project',data=json.dumps({'project':demo_project()}).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.headers['Content-Type'],'application/zip');self.assertTrue(r.read().startswith(b'PK'))
    def test_bad_input_is_json_400(self):
        req=urllib.request.Request(self.url+'/api/validate',data=b'{"project":{}}')
        with self.assertRaises(urllib.error.HTTPError) as ctx: urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code,400);self.assertIn('error',json.load(ctx.exception))
    def test_static_traversal_blocked(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx: urllib.request.urlopen(self.url+'/%2e%2e/server.py')
        self.assertEqual(ctx.exception.code,403)

if __name__=='__main__': unittest.main()
