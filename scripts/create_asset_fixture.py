"""Public synthetic asset/portable-project fixture; contains no personal data."""
import base64
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from roomplan.model import demo_project
from roomplan.storage import save_project

# Deliberately non-cubic proportions expose incorrect floor anchoring after fit.
vertices = [(0,0,0),(3,0,0),(3,.5,0),(0,.5,0),(0,0,1),(3,0,1),(3,.5,1),(0,.5,1)]
faces = [(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),(3,7,6),(3,6,2),(0,4,7),(0,7,3),(1,2,6),(1,6,5)]
coords = [n for face in faces for i in face for n in vertices[i]]
binary = struct.pack('<'+'f'*len(coords), *coords)
gltf = {'asset':{'version':'2.0','generator':'RoomPlan synthetic QA'},'scene':0,'scenes':[{'nodes':[0]}], 'nodes':[{'mesh':0}],
        'meshes':[{'primitives':[{'attributes':{'POSITION':0},'material':0}]}],
        'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[.85,.12,.04,1],'metallicFactor':0,'roughnessFactor':.6},'doubleSided':True}],
        'buffers':[{'byteLength':len(binary)}],'bufferViews':[{'buffer':0,'byteLength':len(binary),'target':34962}],
        'accessors':[{'bufferView':0,'componentType':5126,'count':len(coords)//3,'type':'VEC3','min':[0,0,0],'max':[3,.5,1]}]}
raw=json.dumps(gltf,separators=(',',':')).encode();raw+=b' '*((-len(raw))%4)
glb=struct.pack('<III',0x46546c67,2,28+len(raw)+len(binary))+struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(binary),0x004e4942)+binary
folder=ROOT/'artifacts/fixtures';folder.mkdir(exist_ok=True)
(folder/'wide-test-object.glb').write_bytes(glb)
p=demo_project();p['name']='Synthetic asset and sources QA'
p['assets']=[{'id':'qa-glb','name':'wide-test-object.glb','mime':'model/gltf-binary','data':base64.b64encode(glb).decode()}]
p['objects'].append({'id':'qa-object','catalogId':'custom','kind':'custom','name':'QA red wide mesh','size':[1,1,1],'position':[3,0,3],'rotation':0,'mount':'floor','color':'#ee2200','assetId':'qa-glb'})
for i,(name,mime) in enumerate([('two-room-plan.png','image/png'),('synthetic-walkthrough.mp4','video/mp4')]):
    p['sources'].append({'id':f'qa-source-{i}','name':name,'mime':mime,'data':base64.b64encode((folder/name).read_bytes()).decode()})
p['customResearch']={'fixture':'synthetic-only','confidence':.75}
# Research data are explicitly synthetic, separate from CG camera-path helpers.
# Save the exact imported JSON bytes as an ordinary portable asset. Parsed layers
# reference that asset; no generated model is misrepresented as image inference.
research_layers=[
    {'version':1,'id':'qa-observations','name':'Synthetic sparse observations','kind':'points','visible':True,
     'units':'m','coordinateFrame':'project-x-y-z','positions':[[1.4,.2,3],[1.6,.4,3],[1.8,.6,3],[2,.8,3],[2.2,1,3],[2.4,1.2,3]],
     'color':'#d94d7d','sourceIds':[],'assetIds':[],
     'provenance':{'method':'deterministic-qa-fixture','isSynthetic':True,'inputUsedForGeometry':False}},
    {'version':1,'id':'qa-wall-hypothesis','name':'Synthetic wall hypothesis','kind':'lines','visible':True,
     'units':'m','coordinateFrame':'project-x-y-z','positions':[[3,.15,3.5],[4.4,.15,3.5],[4.4,1.7,3.5],[3,1.7,3.5]],
     'segments':[[0,1],[1,2],[2,3],[3,0],[0,2]],'color':'#126fd6','sourceIds':[],'assetIds':[],
     'provenance':{'method':'deterministic-qa-fixture','isSynthetic':True,'inputUsedForGeometry':False}},
]
research_bytes=json.dumps({'version':1,'researchLayers':research_layers},ensure_ascii=False,indent=2).encode('utf-8')
(folder/'research-layers.json').write_bytes(research_bytes)
p['assets'].append({'id':'qa-research-json','name':'research-layers.json','mime':'application/json','data':base64.b64encode(research_bytes).decode()})
p['researchLayers']=research_layers
for layer in p['researchLayers']: layer['assetIds'].append('qa-research-json')
p['layers']['research']=True
(folder/'asset-project.zip').write_bytes(save_project(p))
print('Created synthetic GLB, two research layers, original research JSON asset, and portable project')
