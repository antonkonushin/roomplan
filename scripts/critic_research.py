"""Independent research contract/archive audit; no production mutations."""
import base64, copy, hashlib, io, json, sys, zipfile, urllib.request, urllib.error
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from roomplan.model import validate_project
from roomplan.storage import load_project, save_project

rows=[]
def record(name, ok, detail):
    rows.append(dict(name=name, status='PASS' if ok else 'FAIL', detail=detail))
raw=(ROOT/'artifacts/fixtures/asset-project.zip').read_bytes()
p,_=load_project(base64.b64encode(raw).decode())
before=copy.deepcopy(p)
validate_project(p)
record('Valid two-layer project does not mutate', p==before, len(p['researchLayers']))
def reject(name, mutate):
    q=copy.deepcopy(p); mutate(q)
    try: validate_project(q); record(name,False,'accepted')
    except ValueError as e: record(name,True,str(e))
    except Exception as e: record(name,False,type(e).__name__+': '+str(e))
def field(key,value,index=0):
    return lambda q:q['researchLayers'][index].__setitem__(key,value)
for key,values in {
 'version':[True,2,'1'], 'id':['',12], 'name':['',None], 'kind':['mesh'],
 'visible':[1,'false'], 'units':['cm'], 'coordinateFrame':['camera'],
 'color':['red','#1234567'], 'positions':[[],[[1,2]],[[True,0,0]],[[1001,0,0]],[[float('nan'),0,0]],[[float('inf'),0,0]]],
 'sourceIds':[['missing'],['synthetic-photo','synthetic-photo']],
 'assetIds':[['missing']], 'provenance':[None], 'segments':[[[0,1]]]
}.items():
    for i,v in enumerate(values):reject(f'Reject {key} case {i+1}',field(key,v))
for i,v in enumerate([[],[[0,999]],[[0,0]],[[False,1]],[[0,1,2]],[[0,1.0]]]):
    reject(f'Reject line segments case {i+1}',field('segments',v,1))
reject('Reject duplicate layer ID',lambda q:q['researchLayers'][1].__setitem__('id',q['researchLayers'][0]['id']))
reject('Reject duplicate existing source references',field('sourceIds',[p['sources'][0]['id']]*2))
reject('Reject duplicate existing asset references',field('assetIds',[p['assets'][0]['id']]*2))
reject('Reject nonobject layer',lambda q:q['researchLayers'].append(None))
reject('Reject excessive layers',lambda q:q.__setitem__('researchLayers',[dict(q['researchLayers'][0],id=f'layer-{i}') for i in range(65)]))
reject('Reject excessive layer points',field('positions',[[0,0,0]]*100001))
reject('Reject total point budget',lambda q:q.__setitem__('researchLayers',[dict(q['researchLayers'][0],id=f'p{i}',positions=[[0,0,0]]*70000) for i in range(3)]))
q=copy.deepcopy(p);q['researchLayers'][0]['visible']=False;q['researchLayers'][0]['provenance']['criticMetadata']={'nested':['retained',17]};q['layers']['cameras']=True
z=save_project(q);r,_=load_project(base64.b64encode(z).decode())
record('Complete project data roundtrip after visibility and provenance edits',r==q,{'sources':len(r['sources']),'assets':len(r['assets']),'layers':len(r['researchLayers'])})
with zipfile.ZipFile(io.BytesIO(raw)) as original,zipfile.ZipFile(io.BytesIO(z)) as output:
    m=json.loads(original.read('project.json')); n=json.loads(output.read('project.json'))
    for kind in ['sources','assets']:
        for a in m[kind]:
            b=next(x for x in n[kind] if x['id']==a['id']);x=original.read(a['archivePath']);y=output.read(b['archivePath'])
            record('Archive exact bytes '+a['name'],x==y,{'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()})
            fixture=ROOT/'artifacts/fixtures'/a['name']
            record('Archive equals original fixture '+a['name'],fixture.is_file() and x==fixture.read_bytes(),str(fixture.relative_to(ROOT)))
def http(path,data):
    req=urllib.request.Request('http://127.0.0.1:8765'+path,json.dumps(data,allow_nan=False).encode(),{'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req) as response:return response.status,response.headers.get_content_type(),json.load(response)
    except urllib.error.HTTPError as e:return e.code,e.headers.get_content_type(),json.load(e)
status,mime,response=http('/api/import/project',{'data':base64.b64encode(z).decode()})
record('HTTP import same portable project',status==200 and response.get('project')==r,{'status':status,'mime':mime})
bad=copy.deepcopy(p);bad['researchLayers'][1]['segments']=[[0,999]]
status,mime,response=http('/api/validate',{'project':bad})
record('HTTP invalid segment yields actionable JSON',status==400 and mime=='application/json' and bool(response.get('error')),{'status':status,'mime':mime,'response':response})
(ROOT/'artifacts/reviews/research-roundtrip.zip').write_bytes(z)
(ROOT/'artifacts/reviews/research-project.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
report={'scope':'Direct production Python validator/storage. No browser claims.','results':rows}
(ROOT/'artifacts/reviews/research-contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(any(x['status']=='FAIL' for x in rows))
