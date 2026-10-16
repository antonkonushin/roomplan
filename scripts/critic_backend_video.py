"""Independent HTTP video output check with synthetic colored frame timeline."""
import base64, io, json, subprocess, tempfile, urllib.request, urllib.error
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
URL='http://127.0.0.1:8765/api/export/video'

def post(payload):
    request=urllib.request.Request(URL,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(request,timeout=60) as response:return response.status,response.headers.get('Content-Type'),response.read()
    except urllib.error.HTTPError as error:return error.code,error.headers.get('Content-Type'),error.read()

def main():
    rows=[]
    def check(name,passed,detail):
        rows.append((name,passed,detail));print(('PASS ' if passed else 'FAIL ')+name+': '+detail)
    frames=[];rawframes=[]
    for color in ['#e32a2a','#2ae32a','#2a2ae3']:
        stream=io.BytesIO();Image.new('RGB',(160,96),color).save(stream,format='JPEG',quality=95)
        rawframes.append(stream.getvalue());frames += [base64.b64encode(stream.getvalue()).decode()]*8
    payload={'frames':frames,'width':160,'height':96,'fps':12}
    status,mime,raw=post(payload)
    check('actual video endpoint',status==200 and mime=='video/webm',f'{status} {mime}; {len(raw)} bytes')
    with tempfile.TemporaryDirectory(prefix='roomplan-critic-video-') as directory:
        video=Path(directory)/'timeline.webm';video.write_bytes(raw)
        result=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,nb_read_frames,r_frame_rate:format=duration','-of','json',str(video)]))
        stream=result['streams'][0]
        check('encoded frame count size rate duration',stream['codec_name']=='vp9' and stream['width']==160 and stream['height']==96 and int(stream['nb_read_frames'])==24 and stream['r_frame_rate']=='12/1' and abs(float(result['format']['duration'])-2)<.001,json.dumps(result))
        pixels=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
        centers=[tuple(pixels[i*160*96*3+(48*160+80)*3:i*160*96*3+(48*160+80)*3+3]) for i in range(24)]
        expected=[0]*8+[1]*8+[2]*8
        check('decoded exact color timeline order',len(pixels)==24*160*96*3 and all(max(range(3),key=lambda c:rgb[c])==wanted for rgb,wanted in zip(centers,expected)),str(centers))
    variants=[('bool fps',{'fps':True}),('odd width',{'width':161}),('zero frames',{'frames':[]}),('too many frames',{'frames':[frames[0]]*901}),('bad base64',{'frames':['***','***']}),('wrong dimensions',{'width':162})]
    stream=io.BytesIO();Image.new('RGB',(160,96),'red').save(stream,format='PNG')
    variants.append(('non JPEG',{'frames':[base64.b64encode(stream.getvalue()).decode()]*2}))
    # Valid JPEG header but missing entropy-coded payload is malformed input.
    variants.append(('truncated JPEG',{'frames':[base64.b64encode(rawframes[0][:650]).decode()]*2}))
    for label,changes in variants:
        changed=dict(payload);changed.update(changes);status,mime,raw=post(changed)
        check('reject '+label,status==400 and 'application/json' in mime and 'error' in json.loads(raw) if status==400 else False,f'{status} {mime}; bytes={len(raw)}')
    failures=sum(not passed for _,passed,_ in rows)
    report='# Independent video API review\n\n'+f'{len(rows)-failures}/{len(rows)} probes pass. Current app server on localhost:8765, 2026-10-15.\n\n'+'\n'.join(f'- **{"PASS" if passed else "FAIL"} {name}** — {detail}' for name,passed,detail in rows)+'\n\nThis uses generated test frames, then probes and decodes the actual HTTP WebM response. It establishes encoding/timeline fidelity; it does not establish browser camera trajectory, absence of wall collisions, CG quality, or real apartment reconstruction.\n'
    (ROOT/'artifacts/reviews/backend-video-independent.md').write_text(report,encoding='utf-8')

if __name__=='__main__':main()
