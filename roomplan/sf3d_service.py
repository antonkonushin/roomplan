"""Optional real SF3D loopback service. Run using the installed SF3D environment.

python -m roomplan.sf3d_service --repo /path/to/stable-fast-3d --port 8877
The upstream model is NOT installed by RoomPlan. This wrapper runs its official
run.py, captures the actual GLB, and never substitutes procedural meshes.
"""
import argparse
import base64
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
from .glb import validate_glb

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',required=True);parser.add_argument('--port',type=int,default=8877)
    args=parser.parse_args();repo=Path(args.repo).resolve()
    if not (repo/'run.py').is_file(): parser.error('--repo must contain official Stable Fast 3D run.py')
    class Handler(BaseHTTPRequestHandler):
        def send(self,status,payload):
            raw=json.dumps(payload).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def do_GET(self): self.send(200,{'method':'Stable Fast 3D','status':'ready-to-run','inferenceVerified':False})
        def do_POST(self):
            if self.path!='/reconstruct': self.send(404,{'error':'Unknown route'});return
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<40*1024*1024: raise ValueError('Request exceeds 40 MB')
                payload=json.loads(self.rfile.read(length));file=payload['files'][0]
                with tempfile.TemporaryDirectory(prefix='roomplan-sf3d-') as td:
                    td=Path(td);image=Image.open(io.BytesIO(base64.b64decode(file['data'],validate=True)))
                    if image.width*image.height>25_000_000: raise ValueError('Image exceeds 25 megapixels')
                    image.convert('RGBA').save(td/'input.png')
                    process=subprocess.run([sys.executable,str(repo/'run.py'),str(td/'input.png'),'--output-dir',str(td/'output'),'--texture-resolution','1024'],cwd=str(repo),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=540)
                    if process.returncode:
                        print(process.stdout.decode(errors='replace'),file=sys.stderr);raise RuntimeError('SF3D failed; see local GPU service log')
                    glb=td/'output'/'0'/'mesh.glb'
                    raw=glb.read_bytes()
                    validate_glb(raw)
                    self.send(200,{'asset':{'name':'sf3d-mesh.glb','mime':'model/gltf-binary','data':base64.b64encode(raw).decode()},'method':'Stable Fast 3D'})
            except Exception as e: self.send(503,{'error':str(e)})
    print(f'SF3D adapter: http://127.0.0.1:{args.port}/reconstruct');HTTPServer(('127.0.0.1',args.port),Handler).serve_forever()

if __name__=='__main__': main()
