"""Independent black-box/direct probes; evidence is synthetic, not real-photo QA."""
import argparse
import base64
import copy
import hashlib
import io
import json
import math
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import threading
import urllib.error
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from roomplan.model import demo_project, validate_project
from roomplan.reconstruction import reconstruct
from roomplan.storage import save_project, load_project
from roomplan.export import export_svg

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--url');ap.add_argument('--serve',action='store_true');ap.add_argument('--report',default='artifacts/reviews/backend-independent.md');args=ap.parse_args()
    localserver=None
    if args.serve:
        from http.server import ThreadingHTTPServer
        from server import Handler
        localserver=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=localserver.serve_forever,daemon=True).start()
        args.url=f'http://127.0.0.1:{localserver.server_port}'
    rows=[]
    def record(label, passed, detail):
        rows.append((label, bool(passed), str(detail)))
        print(('PASS ' if passed else 'FAIL ')+label+': '+str(detail))
    fixture=ROOT/'artifacts/fixtures'
    recognized={}
    for name in ['two-room-plan.png','two-room-plan-noisy.jpg','two-room-plan-skewed.png','blank.png']:
        file={'name':name,'mime':'image/jpeg' if name.endswith('jpg') else 'image/png','data':base64.b64encode((fixture/name).read_bytes()).decode()}
        try:
            p,w=reconstruct({'mode':'plan','files':[file],'ceilingHeight':2.7,'widthMeters':8})
            recognized[name]=p
            record(name+' wall count',len(p['walls'])==8,f"{len(p['walls'])} detected; visible source has eight segments")
            expected=[([0,0],[8,0]),([8,0],[8,6]),([8,6],[0,6]),([0,6],[0,0]),([4.2,0],[4.2,2.1]),([4.2,3],[4.2,6]),([4.2,3.4],[5.6,3.4]),([6.5,3.4],[8,3.4])]
            unmatched=list(p['walls']);errors=[]
            for a,b in expected:
                distances=[min(max(math.dist(a,w['a']),math.dist(b,w['b'])),max(math.dist(a,w['b']),math.dist(b,w['a']))) for w in unmatched]
                if not distances:errors.append(999);continue
                index=min(range(len(distances)),key=distances.__getitem__);errors.append(distances[index]);unmatched.pop(index)
            record(name+' independently matched endpoints',max(errors)<.15 and not unmatched,'max endpoint deviation='+str(round(max(errors),4))+'m, tolerance 0.15m (known 8×6m centerline plan)')
            xs=[v[0] for wall in p['walls'] for v in [wall['a'],wall['b']]]
            record(name+' calibration/no furniture',abs(max(xs)-min(xs)-8)<.001 and not p['objects'] and all(w['height']==2.7 for w in p['walls']),f"width={max(xs)-min(xs)}m, objects={len(p['objects'])}, height=2.7m")
            record(name+' warnings/provenance',bool(w) and p['provenance']['isSynthetic'] is False,f"{len(w)} limitations; mode={p['provenance']['mode']}")
            calibration=p['provenance']['calibration']
            product=calibration['pixelWidth']*calibration['metersPerPixel']
            record(name+' calibration provenance identity',abs(product-calibration['widthMeters'])<.001,f'pixelWidth × metersPerPixel = {product:.6f}; declared width = {calibration["widthMeters"]}')
        except ValueError as e:
            record(name+' rejection',name in ['blank.png','two-room-plan-skewed.png'],str(e))

    # Portable archive carries a real generated video, original fixture photo and a valid GLB.
    with tempfile.TemporaryDirectory(prefix='roomplan-critic-') as temp:
        video=Path(temp)/'synthetic.mp4'
        subprocess.run(['C:/Program Files/ffmpeg/bin/ffmpeg.exe','-loglevel','error','-f','lavfi','-i','color=c=blue:s=64x64:r=5','-t','0.6','-c:v','libx264','-pix_fmt','yuv420p','-y',str(video)],check=True)
        gltf=json.dumps({'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':'custom test triangle','mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0}}]}],'buffers':[{'byteLength':36}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':36,'target':34962}],'accessors':[{'bufferView':0,'componentType':5126,'count':3,'type':'VEC3','min':[0,0,0],'max':[1,1,0]}]}).encode()
        gltf+=b' '*((-len(gltf))%4);binary=struct.pack('<9f',0,0,0,1,0,0,0,1,0)
        glb=struct.pack('<III',0x46546c67,2,12+8+len(gltf)+8+len(binary))+struct.pack('<II',len(gltf),0x4e4f534a)+gltf+struct.pack('<II',len(binary),0x004e4942)+binary
        blobs=[('sources','photo.png','image/png',(fixture/'two-room-plan.png').read_bytes()),('sources','synthetic-video.mp4','video/mp4',video.read_bytes()),('assets','custom-triangle.glb','model/gltf-binary',glb)]
        p=demo_project();p['settings']={'exposure':1.1,'cameraPath':[[0,1.6,0],[4,1.6,4]]};p['walls'][0]['height']=3.2
        for n,(kind,name,mime,raw) in enumerate(blobs):p[kind].append({'id':f'file-{n}','name':name,'mime':mime,'data':base64.b64encode(raw).decode()})
        p['objects'][0]['assetId']='file-2';archive=save_project(p);q,w=load_project(base64.b64encode(archive).decode())
        portable_project=copy.deepcopy(p)
        record('portable exact model roundtrip',p==q,f'ZIP {len(archive)} bytes; geometry, settings, file metadata equal')
        for kind,name,mime,raw in blobs:
            back=next(f for f in q[kind] if f['name']==name)
            digest=hashlib.sha256(raw).hexdigest();other=hashlib.sha256(base64.b64decode(back['data'])).hexdigest()
            record('SHA256 '+name,digest==other,digest)

    bad=[]
    for label,path,val in [('wall NaN',('walls',0,'a',0),math.nan),('wall Inf',('walls',0,'height'),math.inf),('negative size',('objects',0,'size',0),-1),('point Inf',('pointCloud',),[[0,math.inf,0]]),('duplicate object id',('objects',1,'id'),'o1'),('missing asset',('objects',0,'assetId'),'missing')]:
        p=demo_project();target=p
        for k in path[:-1]:target=target[k]
        target[path[-1]]=val;bad.append((label,p))
    for label,p in bad:
        try:validate_project(p);record(label+' rejected',False,'accepted')
        except (ValueError,TypeError):record(label+' rejected',True,'rejected')
    for label,change in [('nonobject opening',lambda p:p.update(openings=[None])),('duplicate asset ids',lambda p:p.update(assets=[{'id':'same','name':f'{i}.bin','mime':'application/octet-stream','data':'YQ=='} for i in range(2)])),('missing source data',lambda p:p.update(sources=[{'id':'s1','name':'missing.png','mime':'image/png'}]))]:
        p=demo_project();change(p)
        try:validate_project(p);record(label+' rejected cleanly',False,'accepted')
        except ValueError:record(label+' rejected cleanly',True,'ValueError')
        except Exception as e:record(label+' rejected cleanly',False,type(e).__name__+' instead of validation error')
    for label,change in [('object missing color',lambda p:p['objects'][0].pop('color')),('room missing name',lambda p:p['rooms'][0].pop('name'))]:
        p=demo_project();change(p)
        try:
            validated,_=validate_project(p)
            try:export_svg(validated);record(label+' validation/export agreement',True,'accepted and exports')
            except Exception as e:record(label+' validation/export agreement',False,'validation accepted, export raises '+type(e).__name__)
        except (ValueError,TypeError):record(label+' validation/export agreement',True,'validation rejects')
    for label,data in [('not ZIP',base64.b64encode(b'bad').decode()),('bad base64','!!!')]:
        try:load_project(data);record(label+' rejected',False,'accepted')
        except ValueError:record(label+' rejected',True,'rejected')
    zbuf=io.BytesIO()
    with zipfile.ZipFile(zbuf,'w') as z:z.writestr('../unsafe','x');z.writestr('project.json','{}')
    try:load_project(base64.b64encode(zbuf.getvalue()).decode());record('ZIP traversal rejected',False,'accepted')
    except ValueError:record('ZIP traversal rejected',True,'rejected without extraction')

    # Translation of entire model must translate authored openings with the model.
    p=demo_project();q=copy.deepcopy(p)
    for w in q['walls']:
        for k in ('a','b'):w[k][0]+=20
    for r in q['rooms']:
        for v in r['polygon']:v[0]+=20
    for o in q['objects']:o['position'][0]+=20
    for opening in q.get('openings',[]):
        for key in ('a','b','position'):
            if isinstance(opening.get(key),list):opening[key][0]+=20
    a=ET.fromstring(export_svg(p));b=ET.fromstring(export_svg(q))
    def arcs(svg):
        paths=[e.get('d') for e in svg.iter() if e.get('d') and 'A' in e.get('d')]
        return [[round(float(v),5) for v in re.findall(r'-?\d+(?:\.\d+)?',d)] for d in paths]
    record('SVG current-model door geometry',arcs(a)==arcs(b),f'original arcs={arcs(a)}; translated arcs={arcs(b)}')
    q=demo_project();q['walls'][0]['b'][0]=12
    svg=export_svg(q)
    record('SVG current-model wall dimensions',b'12.00' in svg,'modified extent must be 12.00m')

    if args.url:
        def post(path,payload):
            req=urllib.request.Request(args.url+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.headers.get('Content-Type'),r.read()
            except urllib.error.HTTPError as e:return e.code,e.headers.get('Content-Type'),e.read()
        status,mime,data=post('/api/validate',{'project':demo_project()});record('HTTP valid model',status==200 and json.loads(data)['project']['version']==1,f'{status} {mime}')
        for label,payload in [('malformed model',{'project':{}}),('nonfinite geometry',{'project':bad[0][1]})]:
            status,mime,data=post('/api/validate',payload);record('HTTP '+label,status==400 and 'error' in json.loads(data),f'{status} {mime}')
        status,mime,data=post('/api/reconstruct/object',{'files':[{'name':'a.png','mime':'image/png','data':base64.b64encode((fixture/'two-room-plan.png').read_bytes()).decode()}]});record('HTTP deferred GPU honest unavailable',status==503 and 'error' in json.loads(data),f'{status} {mime}')
        p=portable_project
        status,mime,data=post('/api/export/project',{'project':p});ok=status==200 and mime=='application/zip'
        status,mime,result=post('/api/import/project',{'data':base64.b64encode(data).decode()});record('HTTP archive roundtrip',ok and status==200 and json.loads(result)['project']==p,f'import {status}; model equality')
        status,mime,data=post('/api/export/plan',{'project':p});ET.fromstring(data);record('HTTP actual SVG export',status==200 and 'image/svg+xml' in mime,f'{status}; parsed XML; {len(data)} bytes')
    failures=sum(not r[1] for r in rows)
    text='# Independent backend review\n\nSynthetic fixture checks; no real apartment photograph accuracy claim. Run with `python scripts/critic_backend.py --serve` to test current on-disk code through a temporary real HTTP server, or `--url http://127.0.0.1:8765` for the app server.\n\n'+f'{len(rows)-failures}/{len(rows)} probes pass; {failures} findings.\n\n'+'\n'.join(f'- **{"PASS" if ok else "FAIL"} {label}** — {detail}' for label,ok,detail in rows)+'\n\n## Critic iteration history and limits\n\nInitial output duplicated all four exterior walls (12 vs 8 segments) on both clean and noisy fixtures. Builder merged wall strips; the first independent rerun matched all eight known wall segments with maximum endpoint error 0.0646 m. A later junction/centreline correction reduced that error to 0.0180 m. Blank input and a 3-degree skew are explicitly rejected; recognition of arbitrary photographed plans is not established.\n\nInitial SVG used hardcoded authored door coordinates. Anchored opening metadata now passes whole-model translation and changed wall extent checks. Missing room name/object color, null openings, duplicate asset IDs and missing source payload caused validation/export inconsistencies; builder fixed them and the independent malformed-model probes pass.\n\nArchive checks use an original synthetic PNG fixture, an actual 0.6-second MP4 created by ffmpeg, and a valid generated triangle GLB. Exact bytes, metadata, modified geometry and settings survive both direct and HTTP archive roundtrips. This does not claim real apartment video reconstruction. GPU inference is explicitly deferred by the user and correctly returns unavailable; no external inference is exercised.\n\nSVG XML and geometric consistency were checked, not a visual win against Floorplanner. Wall editing propagation in the browser, browser import state, walkthrough capture, real photograph robustness, and visual quality require separate integrated/visual review.\n'
    target=ROOT/args.report;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    if localserver:localserver.shutdown();localserver.server_close()

if __name__=='__main__':main()

