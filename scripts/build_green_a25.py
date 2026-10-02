from pathlib import Path
from PIL import Image
import numpy as np, cv2, base64, io, json, html, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/html-starters/green-a25'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=OUT
PALETTE=np.array([[251,254,235],[79,146,66],[35,35,35],[0,0,0]],dtype=np.int32)
COLORS=['#fbfeeb','#4f9242','#232323','#000000']
# Photo bounds include the rounded corners; vectors retain original corner outlines.
PHOTOS={2:[(102,374,520,905),(542,374,1818,905)],3:[(0,0,1920,1080)],4:[(108,574,574,978),(1049,102,1818,978)],5:[(251,238,804,554),(791,129,1327,374),(1175,355,1739,724)],6:[(139,394,886,743),(1029,394,1777,743)],7:[(102,413,644,979),(688,413,1229,979),(1272,413,1818,979)],8:[(0,0,920,767),(472,77,1200,633),(1167,0,1920,489),(870,323,1816,864)],9:[(102,477,1188,979),(1341,437,1818,716)],10:[(102,477,1188,979),(1341,437,1818,716)],11:[]}
# Semantic editable text zones: original glyph geometry is preserved as paths.
T={
2:[('Creative',2,98,106,512,214),('PORTFOLIO',1,547,104,1818,388),('Film and Photography',0,610,762,1137,822),('Presented by',2,102,947,290,975),('Your Name',1,299,947,453,975),('www.reallygreatsite.com',1,1472,947,1818,975)],
3:[('Introduction',0,496,235,1423,412)],
4:[('Hello, Im',2,108,119,440,205),('Your',1,107,227,462,403),('Name',1,109,426,546,603)],
5:[('Education',0,106,739,1086,971),('Borcelle University, 2017',0,238,503,667,585),('Rimberio University, 2019',2,791,399,1202,429),('Fauget University, 2022',0,1216,647,1592,782)],
6:[('Personal',0,107,141,1122,398),('Skills',1,1184,129,1808,382),('Photography',0,183,785,391,821),('Videography',2,1074,785,1284,820)],
7:[('Work',2,107,117,634,345),('Experience',1,702,107,1816,379),('Fashion Photography',0,181,881,562,929),('Product Branding',0,803,881,1118,930),('Commercial Video',1,1381,881,1706,929)],
8:[('Project Portfolio',0,106,709,1817,980)],
9:[('Salford & Co.',1,107,104,1819,411),('Favorite Project',0,510,324,907,388)],
10:[('Larana, Inc.',0,116,59,1817,429),('Last Project',0,558,324,858,388)],
11:[('Let’s Work',2,101,102,1840,473),('Together',1,102,496,1137,784),('hello@reallygreatsite.com',2,1304,526,1756,564),('reallygreatsite.com',2,1304,615,1637,654),('+123-456-7890',2,1304,706,1580,746)]}
BODY1='Lorem ipsum dolor sit amet, consectetur adipiscing elit. In bibendum urna ac neque auctor imperdiet eu vel tortor. Praesent facilisis ex porta cursus tempus. Integer neque diam, blandit ac lacinia vitae, ultricies maximus justo. Nulla facilisi. Sed quis molestie neque.'
BODY2='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eget purus eu augue bibendum egestas. Nam id fermentum leo. Nunc lectus enim, efficitur varius dolor a, malesuada dapibus arcu. Duis id ante vehicula, tincidunt enim in, sagittis turpis.'
BODY={2:[(BODY1,2,1350,663,1765,861)],3:[(BODY1+' Nullam tincidunt finibus dui, ullamcorper accumsan augue maximus id. Nam tempus nunc augue, sit amet auctor orci ultrices vitae. Donec auctor lacus in diam facilisis, vel pharetra justo feugiat. Nulla volutpat lacus tempus, tincidunt orci at, ullamcorper neque. Phasellus porttitor condimentum enim.',0,521,466,1395,790)],4:[(BODY1,0,570,684,1278,860)],5:[(BODY2,0,219,561,767,755),(BODY2,2,790,455,1330,597),(BODY2,0,1220,667,1765,941)],6:[(BODY2.rsplit(' Duis',1)[0],0,138,842,889,934),(BODY2.rsplit(' Duis',1)[0],2,1028,842,1780,934)],9:[(BODY2,2,1280,835,1820,978)],10:[(BODY2,0,1280,835,1820,978)]}
# Areas where vector graphics intentionally overlay photographic material.
OVER={2:[(385,488,910,608),(565,725,1184,863),(1350,650,1780,866)],3:[(472,235,1544,945)],4:[(490,636,1358,909),(700,0,1920,389)],5:[(0,0,1920,1080)],6:[],7:[(145,852,599,959),(768,852,1154,959),(1345,852,1745,959),(400,567,928,681),(554,444,611,504),(1138,444,1199,504),(1729,444,1793,504)],8:[(0,0,1920,1080)],9:[],10:[(1175,219,1920,678)],11:[]}

def boxmask(box):
 m=np.zeros((1080,1920),np.uint8);x,y,r,b=box;m[max(0,y):min(1080,b),max(0,x):min(1920,r)]=1;return m

def paths(mask):
 contours,_=cv2.findContours(mask.astype(np.uint8),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
 chunks=[]
 for c in contours:
  if abs(cv2.contourArea(c))<0.4: continue
  c=cv2.approxPolyDP(c,0.28,True).reshape(-1,2)
  if len(c)<3:continue
  chunks.append('M'+' '.join(f'{x+.5:g},{y+.5:g}' for x,y in c)+'Z')
 return ''.join(chunks)

def data_png(im):
 buf=io.BytesIO();im.save(buf,format='PNG',optimize=True);return base64.b64encode(buf.getvalue()).decode()

SCRIPT='''document.querySelectorAll('[data-content]').forEach(e=>{e.style.cursor='text';e.addEventListener('click',()=>{const v=prompt('替换文字（原字形已转轮廓，替换使用本机字体）',e.dataset.content);if(v===null)return;const [x,y,w,h]=e.dataset.box.split(',').map(Number),s=Number(e.dataset.size);e.replaceChildren();v.split('\\n').forEach((line,i)=>{const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',x);t.setAttribute('y',y+s*.85+i*s*1.3);t.setAttribute('font-size',s);t.setAttribute('font-family',s>45?'Impact,Arial Narrow,sans-serif':'Arial,sans-serif');t.setAttribute('fill',e.dataset.color);if(s>45){t.setAttribute('textLength',w);t.setAttribute('lengthAdjust','spacingAndGlyphs')}t.textContent=line;e.append(t)});e.dataset.content=v})});let target;document.querySelectorAll('image').forEach(e=>{e.style.cursor='pointer';e.addEventListener('click',()=>{target=e;document.querySelector('#image').click()})});document.querySelector('#image').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=()=>{target.setAttribute('href',r.result);target.removeAttribute('data-source');target.setAttribute('preserveAspectRatio','xMidYMid slice')};r.readAsDataURL(f)});document.querySelector('#save').addEventListener('click',()=>{const svg=document.querySelector('svg').cloneNode(true);const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml'}));const a=document.createElement('a');a.href=url;a.download=document.title+'-edited.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});document.querySelector('#palette').addEventListener('change',e=>{const old=e.target.dataset.original;document.querySelectorAll('[fill="'+old+'"]').forEach(p=>p.setAttribute('fill',e.target.value));document.querySelectorAll('[data-color="'+old+'"]').forEach(p=>p.dataset.color=e.target.value);e.target.dataset.original=e.target.value});'''
records=[]
for n in range(2,12):
 original=SOURCE/f'a25-{n:02d}.jpeg'
 name=f'a25-{n:02d}'
 # Original JPEG is already stored beside the editable template.
 im=Image.open(original).convert('RGB');a=np.array(im).astype(np.int32)
 # Cream ink variants in the JPEG are treated as a single stable design token.
 dist=np.sum((a[:,:,None,:]-PALETTE[None,None,:,:])**2,axis=3,dtype=np.int32)
 labels=dist.argmin(axis=2);distance=dist.min(axis=2)
 photo=np.zeros((1080,1920),np.uint8)
 for b in PHOTOS[n]:photo|=boxmask(b)
 allow=1-photo
 for b in OVER[n]:allow|=boxmask(b)
 # Restrict photo overlays to coherent flat regions, avoiding photographic shadows.
 vec=(allow.astype(bool)&((photo==0)|(distance<900)))
 # Text groups extend over photos only for their own known color.
 zones=sorted(T[n]+BODY.get(n,[]),key=lambda z:(z[4]-z[2])*(z[5]-z[3]))
 masks=[(vec&(labels==k)).astype(np.uint8) for k in range(4)]
 defs=[];images=[];fg=[];semantic=[]
 for j,b in enumerate(PHOTOS[n]):
  x,y,r,bt=b;crop=im.crop(b).convert('RGBA');alpha=np.full((bt-y,r-x),255,np.uint8)
  alpha[vec[y:bt,x:r]]=0;crop.putalpha(Image.fromarray(alpha))
  images.append(f'<image id="photo-{j+1}" data-layer="photo" data-source="cropped-reference" x="{x}" y="{y}" width="{r-x}" height="{bt-y}" href="data:image/png;base64,{data_png(crop)}"/>')
 components=[]
 for cm in masks:
  count,cl,stats,_=cv2.connectedComponentsWithStats(cm,8)
  components.append((cl,stats))
 for j,(content,color,x,y,r,b) in enumerate(zones):
  m=(masks[2]|masks[3])&boxmask((x,y,r,b)) if color==2 else masks[color]&boxmask((x,y,r,b));masks[color][m>0]=0
  if color==2:masks[3][m>0]=0
  # Exclude card/background fragments that extend beyond the semantic text box.
  for ck in ([2,3] if color==2 else [color]):
   cl,stats=components[ck]
   for cid in np.unique(cl[m>0]):
    if not cid:continue
    cx,cy,cw,ch,area=stats[cid]
    if cx<x-12 or cy<y-12 or cx+cw>r+12 or cy+ch>b+12:
     fragment=(cl==cid)&(m>0);m[fragment]=0;masks[ck][fragment]=1
  d=paths(m)
  if not d:continue
  size=(b-y)*1.13 if (content,color,x,y,r,b) in T[n] else (28 if n in [3,4] else 24)
  semantic.append(f'<g id="text-{j+1}" data-layer="outlined-text" data-content="{html.escape(content,quote=True)}" data-box="{x},{y},{r-x},{b-y}" data-size="{size:.1f}" data-color="{COLORS[color]}" aria-label="{html.escape(content,quote=True)}"><title>{html.escape(content)}</title><path fill="{COLORS[color]}" fill-rule="evenodd" d="{d}"/></g>')
 for k,m in enumerate(masks):
  d=paths(m)
  if d:fg.append(f'<g id="geometry-{k}" data-layer="geometry" data-color="{COLORS[k]}"><path fill="{COLORS[k]}" fill-rule="evenodd" d="{d}"/></g>')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" role="img" aria-label="A25 {n:02d}"><title>A25 {n:02d} · 高级简约绿调</title><desc>Reference reconstruction: vector outlines and cropped photographic assets. Typography is outlined, not native source-font text. Hidden photo pixels are unavailable.</desc>'+''.join(images+fg+semantic)+'</svg>'
 (OUT/(name+'.svg')).write_text(svg)
 page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+name+'</title><style>body{margin:0;background:#232323;color:#fbfeeb;font-family:Arial,"PingFang SC",sans-serif}main{max-width:1920px;margin:auto;padding:16px}svg{display:block;width:100%;height:auto;background:#fbfeeb}nav{display:flex;align-items:center;gap:14px;padding:16px 0;flex-wrap:wrap}button,a{color:#fbfeeb;background:#4f9242;border:0;padding:10px 18px;border-radius:7px;text-decoration:none;cursor:pointer}p{line-height:1.6;color:#d8ddcf}input[type=file]{display:none}</style><main>'+svg+'<nav><button id="save">导出修改后的 SVG</button><a href="'+name+'.jpeg">原图对照</a><a href="index.html">全部模板</a><label>绿色 <input id="palette" type="color" data-original="#4f9242" value="#4f9242"></label><input id="image" type="file" accept="image/*" aria-label="替换照片"></nav><p>点击文字替换内容，点击照片替换图片。初始字形为可编辑矢量轮廓；替换文字采用本机字体。照片只有截图可见区域，不能还原被原图形遮住的像素。编辑后请导出 SVG 保存。</p></main><script>'+SCRIPT+'</script></html>'
 (OUT/(name+'.html')).write_text(page)
 records.append({'page':n,'stem':name,'source':original.name,'photos':len(images),'text_groups':len(semantic),'path_count':svg.count('<path'),'bytes':len(svg)})
 print(n,len(svg),len(semantic),flush=True)
(OUT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
index='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>A25 绿调模板 · 10 页</title><style>body{background:#fbfeeb;color:#232323;font-family:Arial,"PingFang SC",sans-serif;margin:32px}h1{font-size:30px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:24px}img{width:100%;display:block;border-radius:12px}a{color:#4f9242}p{line-height:1.7}</style><h1>A25 高级简约绿调 · 10 页模板</h1><p>1920×1080 · 轮廓文字与图形为矢量，照片为局部图像。选一页进入编辑。</p><main>'+''.join(f'<article><a href="{r["stem"]}.html"><img src="{r["stem"]}.png" alt="{r["stem"]}"></a><p>{r["stem"]} · <a href="{r["stem"]}.html">HTML 编辑</a> · <a href="{r["stem"]}.svg">SVG</a> · <a href="{r["stem"]}.jpeg">原图</a></p></article>' for r in records)+'</main></html>'
(OUT/'index.html').write_text(index)
