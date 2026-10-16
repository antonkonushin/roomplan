"""Independent known-layout fixtures; not a claim of real-world photo accuracy."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
import numpy as np

out = Path(__file__).resolve().parents[1] / 'artifacts' / 'fixtures'
out.mkdir(parents=True, exist_ok=True)
im = Image.new('RGB', (960, 760), '#faf9f5')
d = ImageDraw.Draw(im)
segments = [(80,80,880,80),(880,80,880,680),(880,680,80,680),(80,680,80,80),
            (500,80,500,290),(500,380,500,680),(500,420,640,420),(730,420,880,420)]
for s in segments: d.line(s, fill='#252c29', width=14)
im.save(out / 'two-room-plan.png')
im.rotate(3, resample=Image.Resampling.BICUBIC, fillcolor='#faf9f5').save(out / 'two-room-plan-skewed.png')
arr = np.array(im, dtype=np.int16)
noise = np.random.default_rng(14).normal(0,12,arr.shape[:2])[...,None]
Image.fromarray(np.clip(arr+noise,0,255).astype('uint8')).save(out / 'two-room-plan-noisy.jpg', quality=65)
blank = Image.new('RGB', (800,600), 'white')
blank.save(out / 'blank.png')
(out/'expected.json').write_text(json.dumps({'fixture':'two-room-plan.png','knownWidthMeters':8,'heightMeters':2.7,'wallSegments':8,'axisAligned':True,'notes':'Door gaps present. Skewed variant deliberately tests unsupported 3 degree scan skew; expect warning/rejection or observed limited quality, never silent demo.'},indent=2),encoding='utf-8')
print(out)
