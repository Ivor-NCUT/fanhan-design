"""Minimal structural and rendered regression check for the ten A25 templates."""
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image, ImageChops, ImageStat
import base64, io, json
root=Path(__file__).resolve().parents[1]/'assets/html-starters/green-a25'
ns={'s':'http://www.w3.org/2000/svg'}
results=[]
for n in range(2,12):
 stem=root/f'a25-{n:02d}'
 svg=stem.with_suffix('.svg').read_text();xml=ET.fromstring(svg)
 assert xml.get('viewBox')=='0 0 1920 1080'
 assert svg in stem.with_suffix('.html').read_text()
 assert len(xml.findall('.//s:path',ns))>=4
 assert xml.findall('.//s:g[@data-content]',ns), stem
 for image in xml.findall('s:image',ns):
  im=Image.open(io.BytesIO(base64.b64decode(image.get('href').split(',',1)[1])))
  assert im.mode=='RGBA', stem
  if im.size==(1920,1080):assert im.getchannel('A').getextrema()==(0,255), stem
 source=Image.open(stem.with_suffix('.jpeg')).convert('RGB')
 rendered=Image.open(stem.with_suffix('.png')).convert('RGB')
 assert source.size==rendered.size==(1920,1080)
 error=sum(ImageStat.Stat(ImageChops.difference(source,rendered)).mean)/3
 assert error<4, (stem,error)
 results.append({'page':n,'mean_rgb_error':round(error,3)})
print('Verified 10 separated SVG/HTML/PNG/JPEG sets; RGB MAE < 4/255')
