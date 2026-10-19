from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path('dist')
class Check(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.ids=set();self.links=[];self.h1=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if 'id' in d:
   assert d['id'] not in self.ids,d['id'];self.ids.add(d['id'])
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(t)
  for k in ['href','src']:
   u=d.get(k,'')
   if u.startswith('/') or u.startswith('#'):self.links.append(u)
  if t=='img':assert 'alt' in d
 def handle_endtag(self,t):
  assert self.stack and self.stack[-1]==t,(t,self.stack[-4:]);self.stack.pop()
pages={}
for f in ROOT.rglob('index.html'):
 p=Check();p.feed(f.read_text());assert p.h1==1 and not p.stack;pages[f]=p
for f,p in pages.items():
 for url in p.links:
  u=urlsplit(url);target=ROOT/unquote(u.path).lstrip('/') if u.path else f
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(f,url)
  if u.fragment:assert u.fragment in pages[target].ids,(target,u.fragment)
 print(f,'HTML, assets and links OK')
projects=json.loads((ROOT/'projects.json').read_text());assert len({p['slug'] for p in projects})==len(projects)
for p in projects:
 assert (ROOT/p['image'].lstrip('/')).exists(),p['image']
 if p.get('video'):
  video=ROOT/p['video'].lstrip('/')
  assert video.exists() and video.stat().st_size>10000,(p['slug'],p['video'])
print(f'{len(projects)} project records, images and {sum(bool(p.get("video")) for p in projects)} local players OK')
