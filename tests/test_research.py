import base64
import copy
import hashlib
import json
import unittest
from roomplan.model import demo_project, validate_project
from roomplan.storage import load_project, save_project
from roomplan.research import validate_research_layers


def layer(kind='points'):
    value={'version':1,'id':kind,'name':f'Synthetic {kind}','kind':kind,'visible':True,
           'units':'m','coordinateFrame':'project-x-y-z','positions':[[1,.1,2],[2,1,2],[3,.1,2]],
           'color':'#e36695','sourceIds':[],'assetIds':[],
           'provenance':{'method':'test-fixture','isSynthetic':True,'arbitraryExtension':{'score':.25}}}
    if kind=='lines': value['segments']=[[0,1],[1,2]]
    return value


class ResearchTests(unittest.TestCase):
    def test_legacy_project_stays_unchanged(self):
        p=demo_project();q,_=validate_project(p)
        self.assertEqual(p,q);self.assertNotIn('researchLayers',q)

    def test_geometry_flags_provenance_and_original_json_roundtrip(self):
        p=demo_project();p['researchLayers']=[layer(),layer('lines')]
        p['researchLayers'][1]['visible']=False;p['layers']['research']=True
        original=b'{"original": "spacing retained", "positions": [[1, 0.1, 2]]}\n'
        p['assets']=[{'id':'original-json','name':'observations.json','mime':'application/json','data':base64.b64encode(original).decode()}]
        p['sources']=[{'id':'source-image','name':'source.bin','mime':'application/octet-stream','data':'YWJj'}]
        for value in p['researchLayers']:
            value['assetIds']=['original-json'];value['sourceIds']=['source-image']
        q,_=load_project(base64.b64encode(save_project(p)).decode())
        self.assertEqual(p,q)
        self.assertEqual(hashlib.sha256(base64.b64decode(q['assets'][0]['data'])).digest(),hashlib.sha256(original).digest())

    def test_invalid_schema_and_coordinates_are_not_silently_accepted(self):
        for field,value in [('version',2),('version',True),('kind','camera'),('units','cm'),('coordinateFrame','camera-z-forward'),
                            ('visible',1),('color','red'),('name',''),('positions',[]),('positions',[[0,0]]),
                            ('positions',[[1001,0,0]]),('positions',[[float('nan'),0,0]]),('positions',[[True,0,0]]),('provenance',[])]:
            with self.subTest(field=field,value=value):
                item=layer();item[field]=value
                with self.assertRaises(ValueError): validate_research_layers([item],set(),set())

    def test_lines_use_explicit_valid_indices(self):
        for segments in [[],[[0,3]],[[0,0]],[[0,1.0]],[[False,1]],[[0]],[[0,1,2]],None]:
            item=layer('lines');item['segments']=segments
            with self.subTest(segments=segments),self.assertRaises(ValueError): validate_research_layers([item],set(),set())
        item=layer();item['segments']=[[0,1]]
        with self.assertRaises(ValueError): validate_research_layers([item],set(),set())

    def test_duplicates_reference_integrity_and_limits(self):
        with self.assertRaises(ValueError): validate_research_layers([layer(),layer()],set(),set())
        with self.assertRaises(ValueError): validate_research_layers([layer()]*65,set(),set())
        for field in ['sourceIds','assetIds']:
            for refs in [['missing'],['known','known'],'known',[{}]]:
                item=layer();item[field]=refs
                with self.subTest(field=field,refs=refs),self.assertRaises(ValueError): validate_research_layers([item],{'known'},{'known'})
        item=layer();item['positions']=[[0,0,0]]*100001
        with self.assertRaises(ValueError): validate_research_layers([item],set(),set())

    def test_aggregate_limits_apply_across_layers(self):
        values=[]
        for i in range(3):
            item=layer();item['id']=str(i);item['positions']=[[0,0,0]]*70000;values.append(item)
        with self.assertRaises(ValueError): validate_research_layers(values,set(),set())


if __name__=='__main__': unittest.main()
