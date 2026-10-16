import base64
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from PIL import Image,ImageDraw
from roomplan.video import encode_walkthrough


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg/ffprobe required')
class VideoExportTests(unittest.TestCase):
    def test_frame_count_resolution_and_duration_are_exact(self):
        frames=[]
        for index in range(30):
            image=Image.new('RGB',(320,180),'#dec09a');draw=ImageDraw.Draw(image)
            draw.rectangle((index*7,50,index*7+30,100),fill='#297153')
            buffer=io.BytesIO();image.save(buffer,format='JPEG')
            frames.append(base64.b64encode(buffer.getvalue()).decode())
        result=encode_walkthrough({'frames':frames,'fps':15,'width':320,'height':180})
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'video.webm';path.write_bytes(result)
            raw=subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=width,height,nb_read_frames:format=duration','-of','json',str(path)])
            info=json.loads(raw);stream=info['streams'][0]
            self.assertEqual((stream['width'],stream['height'],int(stream['nb_read_frames'])),(320,180,30))
            self.assertAlmostEqual(float(info['format']['duration']),2.0,places=2)

    def test_bad_frame_reports_input_error(self):
        with self.assertRaises(ValueError): encode_walkthrough({'frames':['YmFk','YmFk'],'fps':15,'width':320,'height':180})

    def test_truncated_jpeg_reports_input_error(self):
        buffer=io.BytesIO();Image.new('RGB',(320,180),'red').save(buffer,format='JPEG')
        frame=base64.b64encode(buffer.getvalue()[:650]).decode()
        with self.assertRaises(ValueError): encode_walkthrough({'frames':[frame,frame],'fps':15,'width':320,'height':180})


if __name__=='__main__': unittest.main()
