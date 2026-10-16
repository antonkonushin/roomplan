"""A second, genuinely different known layout for integrated import QA."""
import json
from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]/'artifacts/fixtures'
im=Image.new('RGB',(880,560),'white');d=ImageDraw.Draw(im)
walls=[((80,80),(800,80)),((800,80),(800,480)),((800,480),(80,480)),((80,480),(80,80)),((560,80),(560,240)),((560,320),(560,480))]
for a,b in walls:d.line([a,b],fill='#111111',width=14)
im.save(root/'wide-two-zone-plan.png')
(root/'wide-two-zone-plan.expected.json').write_text(json.dumps({'sourcePixels':[880,560],'wallSegments':6,'widthMeters':9,'depthMeters':5,'ceilingHeight':2.9,'doorGapMeters':1,'layout':'Wide rectangle, partition at two-thirds width with one central door gap'},indent=2),encoding='utf-8')
