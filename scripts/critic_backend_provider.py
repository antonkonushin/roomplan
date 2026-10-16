"""Local object adapter contract audit. Synthetic GLB; NO model/GPU inference."""
import base64, hashlib, io, json, os, socket, struct, subprocess, sys, tempfile, threading, time
import urllib.request, urllib.error
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server import Handler
from roomplan.model import demo_project

def request(url,payload=None):
    req=urllib.request.Request(url,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.read()
    except urllib.error.HTTPError as e:return e.code,e.read()

def main():
    results=[]
    def check(name,ok,detail):results.append((name,bool(ok),detail));print(('PASS ' if ok else 'FAIL ')+name+': '+detail)
    glb=(ROOT/'artifacts/fixtures/wide-test-object.glb').read_bytes()
    header=struct.unpack('<III',glb[:12]);chunklen,chunktype=struct.unpack('<II',glb[12:20]);gltf=json.loads(glb[20:20+chunklen])
    check('fixture GLB structurally valid',header==(0x46546c67,2,len(glb)) and chunktype==0x4e4f534a and gltf['asset']['version']=='2.0' and bool(gltf.get('meshes')),f'{len(glb)} bytes; SHA256 {hashlib.sha256(glb).hexdigest()}')
    files=[]
    for name,color in [('first.png','red'),('second.png','blue')]:
        stream=io.BytesIO();Image.new('RGB',(80,64),color).save(stream,format='PNG');files.append({'name':name,'mime':'image/png','data':base64.b64encode(stream.getvalue()).decode()})
    payload={'files':files,'name':'Synthetic contract object — not inference'}
    class Fixture(BaseHTTPRequestHandler):
        mode='valid';calls=[]
        def log_message(self,*args):pass
        def do_POST(self):
            type(self).calls.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
            asset={'name':'fixture.glb','mime':'model/gltf-binary','data':base64.b64encode(glb).decode()}
            status=200;body={'asset':asset,'method':'Stable Fast 3D'}
            if self.mode=='http-failure':status=503;body={'error':'synthetic failure'}
            elif self.mode=='wrong-mime':asset['mime']='image/png'
            elif self.mode=='invalid-base64':asset['data']='***'
            elif self.mode=='invalid-magic':asset['data']=base64.b64encode(b'invalid').decode()
            elif self.mode=='truncated-glb':asset['data']=base64.b64encode(b'glTF').decode()
            elif self.mode=='wrong-glb-version':asset['data']=base64.b64encode(glb[:4]+struct.pack('<I',3)+glb[8:]).decode()
            elif self.mode=='wrong-glb-length':asset['data']=base64.b64encode(glb[:8]+struct.pack('<I',len(glb)+16)+glb[12:]).decode()
            elif self.mode=='invalid-glb-json':asset['data']=base64.b64encode(glb[:20]+b'!'+glb[21:]).decode()
            elif self.mode=='missing-asset':body={}
            raw=json.dumps(body).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    fixture=ThreadingHTTPServer(('127.0.0.1',0),Fixture);app=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    for server in [fixture,app]:threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{app.server_port}';endpoint=f'http://127.0.0.1:{fixture.server_port}/reconstruct'
    try:
        with patch.dict(os.environ,{'ROOMPLAN_RECONSTRUCTION_URL':endpoint}):
            status,raw=request(base+'/api/reconstruct/object',payload);result=json.loads(raw)
            check('actual API successful local provider',status==200 and 'asset' in result,f'HTTP {status}; ephemeral app/provider ports')
            check('first image forwarded exactly',Fixture.calls[-1]['files']==files[:1] and Fixture.calls[-1]['name']==payload['name'],'single-image seam sends first image only')
            check('all originals preserved exactly',all({k:f[k] for k in ['name','mime','data']}==expected for f,expected in zip(result['sources'],files)) and len(result['sources'])==2,'both PNG bytes and metadata retained')
            check('returned GLB preserved exactly',base64.b64decode(result['asset']['data'])==glb,hashlib.sha256(base64.b64decode(result['asset']['data'])).hexdigest())
            check('asset bound to custom object',result['object']['assetId']==result['asset']['id'] and result['object']['kind']=='custom' and bool(result['warnings']),'custom asset id reference; scale/first-image limitations present')
            project=demo_project();project['objects'].append(result['object']);project['assets'].append(result['asset']);project['sources'].extend(result['sources'])
            status,archive=request(base+'/api/export/project',{'project':project});status2,restored=request(base+'/api/import/project',{'data':base64.b64encode(archive).decode()})
            check('provider result portable ZIP roundtrip',status==status2==200 and json.loads(restored)['project']==project,'actual HTTP ZIP and import; sources, GLB, object metadata equal')
            for mode in ['http-failure','wrong-mime','invalid-base64','invalid-magic','missing-asset','truncated-glb','wrong-glb-version','wrong-glb-length','invalid-glb-json']:
                Fixture.mode=mode;status,raw=request(base+'/api/reconstruct/object',payload);body=json.loads(raw)
                check('reject provider '+mode,status==503 and 'error' in body and 'asset' not in body,f'HTTP {status}; no geometry fallback expected')
            Fixture.mode='valid'
        # Exercise the real sf3d_service wrapper with an explicitly fake upstream run.py.
        # The wrapper subprocess and CLI contract are real; the GLB is copied, not inferred.
        with tempfile.TemporaryDirectory(prefix='roomplan-critic-provider-') as directory:
            repo=Path(directory);(repo/'fixture.glb').write_bytes(glb)
            code="""import argparse,json,shutil
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output-dir',required=True);p.add_argument('--texture-resolution',required=True);a=p.parse_args()
im=Image.open(a.input);im.load()
Path(__file__).with_name('invocation.json').write_text(json.dumps({'size':list(im.size),'mode':im.mode,'pixel':list(im.getpixel((0,0))),'texture':a.texture_resolution}))
out=Path(a.output_dir)/'0';out.mkdir(parents=True);shutil.copyfile(Path(__file__).with_name('fixture.glb'),out/'mesh.glb')
"""
            (repo/'run.py').write_text(code,encoding='utf-8')
            with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            service=subprocess.Popen([sys.executable,'-m','roomplan.sf3d_service','--repo',str(repo),'--port',str(port)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            try:
                service_url=f'http://127.0.0.1:{port}'
                for _ in range(50):
                    try:status,raw=request(service_url);break
                    except (urllib.error.URLError,ConnectionError):time.sleep(.1)
                else:raise RuntimeError('SF3D wrapper test did not start')
                check('wrapper health disclaims inference',status==200 and json.loads(raw)['inferenceVerified'] is False,'ready-to-run is not inference verification')
                with patch.dict(os.environ,{'ROOMPLAN_RECONSTRUCTION_URL':service_url+'/reconstruct'}):
                    status,raw=request(base+'/api/reconstruct/object',payload);body=json.loads(raw)
                    check('real wrapper + fixture CLI + real API success',status==200 and base64.b64decode(body['asset']['data'])==glb,f'HTTP {status}; exact fixture GLB, not model output')
                    invocation=json.loads((repo/'invocation.json').read_text())
                    check('wrapper official CLI shape and image conversion',invocation=={'size':[80,64],'mode':'RGBA','pixel':[255,0,0,255],'texture':'1024'},json.dumps(invocation))
                    (repo/'fixture.glb').write_bytes(b'glTF')
                    status,raw=request(service_url+'/reconstruct',payload)
                    check('wrapper rejects truncated GLB directly',status==503 and 'error' in json.loads(raw),f'HTTP {status}; invalid upstream output')
                    # Real wrapper must propagate subprocess failures without any generated fallback.
                    (repo/'run.py').write_text('raise SystemExit(7)\n',encoding='utf-8')
                    status,raw=request(base+'/api/reconstruct/object',payload)
                    check('wrapper process failure propagated',status==503 and 'error' in json.loads(raw),f'HTTP {status}; no asset returned')
            finally:
                service.terminate();service.communicate(timeout=10)
    finally:
        for server in [fixture,app]:server.shutdown();server.server_close()
    failures=sum(not ok for _,ok,_ in results)
    report='# Independent local object provider contract review\n\n'+f'{len(results)-failures}/{len(results)} probes pass. Synthetic contract fixture only. No model weights, GPU inference, external endpoint, or app server on port 8765 was used.\n\n'+'\n'.join(f'- **{"PASS" if ok else "FAIL"} {name}** — {detail}' for name,ok,detail in results)+'\n\nThe real Python app route and real sf3d_service wrapper were exercised on temporary loopback ports. The fake upstream run.py only copied a pre-existing valid synthetic GLB into the documented output path. This proves request/CLI/response and source/asset persistence contracts, not SF3D installation, model inference, shape quality, licensing, GPU performance, or browser rendering. Actual inference remains deferred.\n'
    (ROOT/'artifacts/reviews/backend-provider-independent.md').write_text(report,encoding='utf-8')

if __name__=='__main__':main()
