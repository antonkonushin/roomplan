"""Deterministic ordinary-CG video encoding; no generative model involved."""
import base64
import io
import shutil
import subprocess
import tempfile
from pathlib import Path
from PIL import Image


def encode_walkthrough(payload):
    encoder=shutil.which('ffmpeg')
    if not encoder: raise ValueError('Для экспорта видео установите FFmpeg на Python-сервер и добавьте его в PATH.')
    frames=payload.get('frames');fps=payload.get('fps',15)
    width=payload.get('width');height=payload.get('height')
    if not isinstance(fps,int) or isinstance(fps,bool) or not 10<=fps<=30: raise ValueError('Частота кадров должна быть целой от 10 до 30')
    if not isinstance(frames,list) or not 2<=len(frames)<=900: raise ValueError('Ожидается от 2 до 900 кадров')
    if not all(isinstance(v,int) and not isinstance(v,bool) and 64<=v<=1920 and v%2==0 for v in [width,height]): raise ValueError('Размеры кадров должны быть чётными числами от 64 до 1920')
    total=0
    with tempfile.TemporaryDirectory(prefix='roomplan-video-') as directory:
        directory=Path(directory);input_path=directory/'frames.mjpeg';output_path=directory/'walkthrough.webm'
        with input_path.open('wb') as stream:
            for frame in frames:
                if not isinstance(frame,str) or len(frame)>8*1024*1024: raise ValueError('Слишком большой или неверный кадр')
                try:
                    raw=base64.b64decode(frame,validate=True)
                    with Image.open(io.BytesIO(raw)) as image:
                        if image.format!='JPEG' or image.size!=(width,height): raise ValueError('Все кадры должны быть JPEG с указанными одинаковыми размерами')
                        # Decode the pixels: JPEG verify() only checks metadata and
                        # can accept a truncated entropy stream that FFmpeg repairs.
                        image.load()
                except ValueError: raise
                except Exception as e: raise ValueError('Не удалось прочитать JPEG-кадр') from e
                total+=len(raw)
                if total>250*1024*1024: raise ValueError('Кадры превышают лимит 250 МБ')
                stream.write(raw)
        command=[encoder,'-v','error','-nostdin','-y','-f','image2pipe','-framerate',str(fps),'-vcodec','mjpeg','-i',str(input_path),'-an','-c:v','libvpx-vp9','-deadline','good','-cpu-used','4','-crf','26','-b:v','0','-pix_fmt','yuv420p','-threads','2',str(output_path)]
        try: result=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
        except subprocess.TimeoutExpired as e: raise ValueError('Кодирование не завершилось за 180 секунд; сократите маршрут') from e
        if result.returncode or not output_path.is_file(): raise ValueError('FFmpeg не смог собрать видео. Проверьте установку кодека VP9 на сервере.')
        return output_path.read_bytes()
