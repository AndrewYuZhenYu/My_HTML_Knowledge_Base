#!/usr/bin/env python3
"""HKB V3: multi-file Markdown -> independent HTML documents; build-time SVG math.
Usage: python tools/build.py [--check]
Source of truth: sources/<course-id>/**/*.md; output: subjects/<course-id>/**/*.html.
"""
from __future__ import annotations
from pathlib import Path
from collections import OrderedDict
from string import Template
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString
import argparse, hashlib, html, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
import mistune
from visuals import ASSET_DIAGRAMS, SPECS, render as render_visual
from physics_widgets import WIDGETS, render_widget
from visual_catalog import EXTRA_SPECS
from learning_widgets import STEPS, TRUTHS, render_widget as render_learning_widget

ROOT=Path(__file__).resolve().parents[1]
COURSE_CONFIG=json.loads((ROOT/'config/courses.json').read_text(encoding='utf-8'))
SOURCES=ROOT/'sources'
SHELL=Template((ROOT/'tools/shell.html').read_text(encoding='utf-8'))
CALL_LABELS={'abstract':'摘要','tldr':'摘要','note':'注释','info':'信息','todo':'待办','important':'重点','warning':'警告','tip':'技巧','hint':'提示','success':'完成','check':'检查','done':'完成','question':'思考','help':'帮助','faq':'问答','example':'例题','summary':'总结','failure':'失败','fail':'失败','missing':'缺失','danger':'危险','error':'错误','bug':'问题','quote':'引用','cite':'引用','caution':'注意','attention':'注意'}
CALL_ICON={'abstract':'≡','tldr':'≡','note':'i','info':'i','todo':'□','important':'!','warning':'!','tip':'✦','hint':'✦','success':'✓','check':'✓','done':'✓','question':'?','help':'?','faq':'?','example':'◇','summary':'≡','failure':'×','fail':'×','missing':'×','danger':'!','error':'×','bug':'⚑','quote':'“','cite':'“','caution':'!','attention':'!'}
COURSES=sorted(COURSE_CONFIG['courses'],key=lambda c:c.get('order',100))
CONFIG_IDS={c['id'] for c in COURSES}
OVERRIDES=COURSE_CONFIG.get('overrides',{})
md=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])


def safe_slug(s):
 s=unicodedata.normalize('NFKC',s).strip().replace(' ','-')
 s=re.sub(r'[^\w\-\u4e00-\u9fff]+','-',s,flags=re.UNICODE).strip('-')
 return s or 'doc-'+hashlib.sha1(s.encode()).hexdigest()[:8]

def heading_slug(s):
 s=unicodedata.normalize('NFKC',s).lower().strip()
 s=re.sub(r'[^\w\s-]','',s,flags=re.UNICODE)
 return re.sub(r'\s+','-',s) or 'section'

def heading_label(node):
 def walk(part):
  if isinstance(part,NavigableString):return str(part)
  if 'math-inline' in part.get('class',[]) or 'math-display' in part.get('class',[]):
   return '$'+part.get('data-tex','')+'$'
  return ''.join(walk(child) for child in part.contents)
 return re.sub(r'\s+',' ',walk(node)).strip()

def docs_list():
 docs=[];outputs={}
 for c in COURSES:
  folder=SOURCES/c['id']
  if not folder.exists():continue
  for src in sorted(folder.rglob('*.md'),key=lambda x:x.as_posix().casefold()):
   if any(p.startswith('.') or p.startswith('_') for p in src.relative_to(folder).parts):continue
   rel=src.relative_to(SOURCES).as_posix()
   override=OVERRIDES.get(rel,{})
   out_name=override.get('output') or safe_slug(src.stem)+'.html'
   # Nested source folders retain matching nested URL hierarchy.
   sub=src.relative_to(folder).parent
   output=ROOT/'subjects'/c['id']/sub/out_name
   if not output.resolve().is_relative_to((ROOT/'subjects'/c['id']).resolve()):raise ValueError('output escapes course folder: '+rel)
   if output in outputs:raise ValueError(f'output collision: {outputs[output]} and {rel} -> {output}')
   outputs[output]=rel
   docs.append({'course':c,'source':src,'source_rel':rel,'output':output,'title':override.get('title') or src.stem,'description':override.get('description','')})
 return docs

def global_url(path):return path.relative_to(ROOT).as_posix()

def map_output(doc):
 if doc['source_rel']=='physics/12 气体动理论.md':return doc['output'].parent/'12-mindmap.html'
 return doc['output'].with_name(doc['output'].stem+'-mindmap.html')

def depth_root(path):return '../'*len(path.relative_to(ROOT).parents[:-1])

def esc(x):return html.escape(str(x),quote=True)

def course_nav(docs,root,current):
 chunks=[]
 for c in COURSES:
  items=[d for d in docs if d['course']['id']==c['id']]
  links=[]
  if items:
   overview=ROOT/'subjects'/c['id']/'index.html'
   links.append(f'<a class="nav-sub nav-overview{" active" if overview==current else ""}" href="{esc(root+global_url(overview))}"><span class="nav-dot"></span>课程总览</a>')
  for d in items:
   active=d['output']==current
   dest=root+global_url(d['output'])
   links.append(f'<a class="nav-sub{" active" if active else ""}" href="{esc(dest)}"><span class="nav-dot"></span>{esc(d["title"])}</a>')
   map_path=map_output(d)
   links.append(f'<a class="nav-sub nav-map{" active" if map_path==current else ""}" href="{esc(root+global_url(map_path))}"><span class="nav-dot"></span>↳ 思维导图</a>')
   # Special pages sit below their source chapter.
   if d['source_rel']=='physics/12 气体动理论.md':
    for label,file in [('交互函数实验室','12-lab.html')]:
     p=d['output'].parent/file
     links.append(f'<a class="nav-sub{" active" if p==current else ""}" href="{esc(root+global_url(p))}"><span class="nav-dot"></span>{label}</a>')
  icon=esc(c.get('icon','◇'))
  label=esc(c['name'])
  if links:
   chunks.append(f'<details class="course-group" open><summary class="course-title"><span class="course-emoji">{icon}</span>{label}<span class="course-expand">⌄</span></summary><div class="course-children">{"".join(links)}</div></details>')
  else:
   chunks.append(f'<div class="course-group folded"><div class="course-title"><span class="course-emoji">{icon}</span>{label}<small>尚未导入</small></div></div>')
 return '\n'.join(chunks)

def wrap(title,subtitle,inner,output,docs, *, current='note',toc=None,extra_script='',article_class='article-surface'):
 root=depth_root(output)
 nav=course_nav(docs,root,output)
 return SHELL.substitute(title=esc(title),subtitle=esc(subtitle),body=inner,root=root,
   course_navigation=nav,current=current,toc_json=json.dumps(toc or [],ensure_ascii=False).replace('<','\\u003c'),
   preamble=extra_script,article_class=article_class,right_panel='')

class Batch:
 def __init__(self):self.formulas=OrderedDict();self.math_counts={};self.warnings=[];self.math_errors=[]
 def protect(self,text,doc_key):
  # Math is protected before Markdown punctuation processing (both display and inline).
  # Leave fenced and inline code intact: dollar signs there are examples, not formulas.
  code={};lines=[];fence=None;block=[]
  for line in text.splitlines(keepends=True):
   marker=re.match(r'^ {0,3}(`{3,}|~{3,})',line)
   if fence is None and marker:
    fence=(marker.group(1)[0],len(marker.group(1)));block=[line];continue
   if fence is not None:
    block.append(line)
    if re.match(r'^ {0,3}'+re.escape(fence[0])+r'{'+str(fence[1])+r',}\s*$',line):
     placeholder=f'CODEPLACEHOLDER{len(code)+1:07d}END';code[placeholder]=''.join(block)
     lines.append(placeholder+'\n');fence=None;block=[]
    continue
   lines.append(line)
  if block:lines.extend(block)
  text=''.join(lines)
  def hide_code(m):
   placeholder=f'CODEPLACEHOLDER{len(code)+1:07d}END';code[placeholder]=m.group(0);return placeholder
  text=re.sub(r'(?<!`)(`+)(?!`)(.*?)\1(?!`)',hide_code,text,flags=re.S)
  def add(tex,display):
   key=f'MATHPLACEHOLDER{len(self.formulas)+1:07d}END'
   self.formulas[key]={'key':key,'tex':tex.strip(),'display':display}
   self.math_counts[doc_key]=self.math_counts.get(doc_key,0)+1
   return key
  text=re.sub(r'(?<!\\)\$\$(.*?)(?<!\\)\$\$',lambda m:add(m.group(1),True),text,flags=re.S)
  text=re.sub(r'(?<![\\$])\$(?!\$)([^\n$]+?)(?<!\\)\$(?!\$)',lambda m:add(m.group(1),False),text)
  for placeholder,original in code.items():text=text.replace(placeholder,original)
  return text
 def render_all(self):
  if not self.formulas:return {}
  with tempfile.TemporaryDirectory(prefix='hkb-math-') as tmp:
   a=Path(tmp)/'input.json';b=Path(tmp)/'output.json'
   a.write_text(json.dumps(list(self.formulas.values()),ensure_ascii=False),encoding='utf-8')
   cmd=['node',str(ROOT/'tools/render_math.js'),str(a),str(b)]
   env=os.environ.copy()
   env['NODE_PATH']=os.pathsep.join(x for x in [str(ROOT/'node_modules'),env.get('NODE_PATH','')] if x)
   result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env,timeout=600)
   if result.returncode:
    raise RuntimeError('MathJax conversion failed. Run npm install and retry:\n'+result.stderr[-1400:])
   rendered=json.loads(b.read_text(encoding='utf8'))
  for key,formula in self.formulas.items():
   output=rendered.get(key,'')
   if '<svg' not in output or 'data-mml-node="merror"' in output or 'class="formula-error"' in output:
    self.math_errors.append(f'{key}: {formula["tex"][:100]}')
  return rendered

def transform(doc,batch,svg_map):
 text=doc['source'].read_text(encoding='utf8');key=doc['source_rel']
 soup=BeautifulSoup(md(batch.protected[key]),'html.parser')
 for tn in list(soup.find_all(string=True)):
  if not re.search(r'MATHPLACEHOLDER\d{7}END',str(tn)):continue
  parts=re.split(r'(MATHPLACEHOLDER\d{7}END)',str(tn))
  for part in parts:
   if not part:continue
   if part in batch.formulas:
    f=batch.formulas[part];node=soup.new_tag('span');node['class']='math-display' if f['display'] else 'math-inline';node['data-tex']=f['tex']
    fragment=BeautifulSoup(svg_map.get(part,''),'html.parser')
    for elem in list(fragment.contents):node.append(elem.extract())
    tn.insert_before(node)
   else:tn.insert_before(NavigableString(part))
  tn.extract()
 callout_count=0
 for bq in reversed(soup.find_all('blockquote')):
  firstp=next((p for p in bq.children if getattr(p,'name',None)=='p'),None)
  if firstp is None:continue
  firsttext=firstp.get_text(' ',strip=True)
  match=re.match(r'^\[!(\w+)\]([+-])?\s*(.*)',firsttext)
  if not match:continue
  kind=match.group(1).lower()
  title=match.group(3).split('\n')[0].strip() or CALL_LABELS.get(kind,kind)
  first=next((n for n in firstp.descendants if isinstance(n,NavigableString)),None)
  if first is not None:
   new=re.sub(r'^\s*\[!\w+\][+-]?\s*[^\n]*\n?', '',str(first),count=1)
   if new.strip():first.replace_with(new)
   else:first.extract()
  box=soup.new_tag('aside');box['class']=f'callout callout-{kind}';box['data-callout']=kind
  head=soup.new_tag('div');head['class']='callout-title';head['data-icon']=CALL_ICON.get(kind,'i');head.string=title
  body=soup.new_tag('div');body['class']='callout-content'
  for n in list(bq.contents):body.append(n.extract())
  box.append(head);box.append(body);bq.replace_with(box);callout_count+=1
 # Obsidian tag-only lines are metadata, not ordinary prose paragraphs.
 for paragraph in list(soup.find_all('p')):
  if paragraph.find(True):continue
  value=paragraph.get_text(' ',strip=True)
  if not re.fullmatch(r'#[^\s#]+(?:\s+#[^\s#]+)*',value):continue
  group=soup.new_tag('div');group['class']='note-tags';group['aria-label']='笔记标签'
  label=soup.new_tag('span');label['class']='note-tags-label';label.string='标签';group.append(label)
  for tag in value.split():
   chip=soup.new_tag('span');chip['class']='note-tag';chip.string=tag;group.append(chip)
  paragraph.replace_with(group)
 # Convert relative media paths to real copied local resources. Never fetch external URLs.
 asset_visual_count=0
 for tag,attr in [('img','src'),('a','href')]:
  for node in soup.select(tag+f'[{attr}]'):
   raw=node[attr]
   if not raw or raw.startswith(('#','http:','https:','data:','mailto:')):continue
   if raw.startswith(('javascript:','file:','//')):
    del node[attr];batch.warnings.append(key+': blocked unsafe link '+raw);continue
   source_candidate=(doc['source'].parent/unquote(raw.split('#')[0].split('?')[0])).resolve()
   if not source_candidate.is_relative_to(SOURCES.resolve()):
    batch.warnings.append(key+': relative file outside sources not copied '+raw);continue
   if not source_candidate.is_file():
    diagram=ASSET_DIAGRAMS.get(source_candidate.name) if tag=='img' and key=='physics/14 振动 扩充版.md' else None
    if diagram:
     batch.warnings.append(key+': original image missing; source-based diagram shown for '+source_candidate.name)
     target=node.parent if node.parent.name=='p' and not node.parent.get_text(strip=True) and len(node.parent.find_all('img'))==1 else node
     target.replace_with(BeautifulSoup(render_visual(diagram),'html.parser'))
     asset_visual_count+=1
     continue
    batch.warnings.append(key+': local asset missing '+raw)
    if tag=='img':
     missing=soup.new_tag('span');missing['class']='missing-image';missing['role']='img'
     missing['aria-label']='原笔记配图缺失：'+node.get('alt','')
     missing.string='配图待补：'+(node.get('alt') or raw)
     node.replace_with(missing)
    continue
   if source_candidate.suffix.lower()=='.md':
    # Link to generated chapter (resolved after all articles have been discovered).
    matching=next((d for d in ALL_DOCS if d['source'].resolve()==source_candidate),None)
    if matching:
     fragment='#'+raw.split('#',1)[1] if '#' in raw else ''
     node[attr]=os.path.relpath(matching['output'],doc['output'].parent).replace(os.sep,'/')+fragment
    continue
   dest=ROOT/'assets'/'imported'/safe_slug(doc['course']['id'])/(hashlib.sha1(str(source_candidate).encode()).hexdigest()[:10]+'-'+source_candidate.name)
   dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source_candidate,dest)
   node[attr]=os.path.relpath(dest,doc['output'].parent).replace(os.sep,'/')
 heads=[]
 for i,heading in enumerate(soup.select('h1,h2,h3,h4,h5,h6'),1):
  title=heading_label(heading)
  slug=heading_slug(title)
  count=sum(h['id']==slug or h['id'].startswith(slug+'-') for h in heads)
  heading['id']=slug if not count else f'{slug}-{count}'
  alias=soup.new_tag('span');alias['id']=f'sec-{i:02d}';alias['class']='anchor-alias';alias['aria-hidden']='true';heading.insert(0,alias)
  heads.append({'id':heading['id'],'level':int(heading.name[1]),'title':title})
 first=soup.find('h1')
 if first:
  links=f'<a href="{esc(map_output(doc).name)}">◈ 本章思维导图</a>'
  if key=='physics/12 气体动理论.md':links+='<a href="12-lab.html">⌁ 麦克斯韦交互图</a>'
  first.insert_before(BeautifulSoup(f'<div class="chapter-links">{links}<span>导图与插图为辅助阅读内容</span></div>','html.parser'))
 if key=='physics/12 气体动理论.md':
  for h in soup.select('h2,h3'):
   if '3.2.4 分布曲线的特点' in h.get_text(' ',strip=True):
    embed='''<div class="inline-viz"><div class="inline-viz-head"><div><b>交互插图 · 麦克斯韦速率分布</b><small>在知识点旁直接调节气体和温度</small></div><a href="12-lab.html">全屏查看 ↗</a></div><div class="inline-viz-controls"><label>气体 <select id="gasSelect"><option value="o2">氧气 O₂</option><option value="n2">氮气 N₂</option><option value="h2">氢气 H₂</option><option value="he">氦气 He</option></select></label><label>温度 <input type="range" id="tempSelect" min="200" max="900" step="25" value="300"><strong id="tempLabel">300 K</strong></label></div><svg id="maxwellPlot" viewBox="0 0 820 365" aria-label="随参数变化的麦克斯韦速率分布函数图"></svg><div class="plot-legend"><span><i style="background:#3675bd"></i><span id="legend1">300 K</span></span><span><i style="background:#d39959"></i><span id="legend2">510 K 对照</span></span></div><div class="inline-viz-stats"><span>最概然速率<b id="statVp">—</b></span><span>平均速率<b id="statMean">—</b></span><span>方均根速率<b id="statRms">—</b></span></div><p id="formulaSummary" class="inline-viz-tip">拖动滑块观察曲线变化。</p></div>'''
    h.insert_after(BeautifulSoup(embed,'html.parser'));break
 visual_count=asset_visual_count
 for spec in SPECS.get(key,[])+EXTRA_SPECS.get(key,[]):
  matches=[h for h in soup.select('h1,h2,h3,h4,h5,h6') if spec['match'] in heading_label(h)]
  if len(matches)!=1:raise ValueError(f'{key}: visual heading {spec["match"]!r} matched {len(matches)} sections')
  matches[0].insert_after(BeautifulSoup(render_visual(spec),'html.parser'))
  visual_count+=1
 for spec in WIDGETS.get(key,[]):
  matches=[h for h in soup.select('h1,h2,h3,h4,h5,h6') if spec['match'] in heading_label(h)]
  if len(matches)!=1:raise ValueError(f'{key}: widget heading {spec["match"]!r} matched {len(matches)} sections')
  matches[0].insert_after(BeautifulSoup(render_widget(spec),'html.parser'))
  visual_count+=1
 for widget_kind,widget_specs in (('stepper',STEPS),('truth',TRUTHS)):
  spec=widget_specs.get(key)
  if not spec:continue
  matches=[h for h in soup.select('h1,h2,h3,h4,h5,h6') if spec['match'] in heading_label(h)]
  if len(matches)!=1:raise ValueError(f'{key}: {widget_kind} heading {spec["match"]!r} matched {len(matches)} sections')
  matches[0].insert_after(BeautifulSoup(render_learning_widget(spec,widget_kind),'html.parser'))
  visual_count+=1
 snippet_entries=[]
 for h in soup.select('h1,h2,h3'):
  parts=[]
  for next_el in h.next_siblings:
   if getattr(next_el,'name',None) in ('h1','h2','h3'):break
   if getattr(next_el,'name',None):
    if {'concept-visual','inline-viz'} & set(next_el.get('class',[])):continue
    snippet=next_el.get_text(' ',strip=True)
    texs=' '.join(x.get('data-tex','') for x in next_el.select('[data-tex]'))
    parts.append(snippet+' '+texs)
  snippet_entries.append({'page':doc['title'],'title':heading_label(h),'url':global_url(doc['output'])+'#'+h['id'],'text':' '.join(parts)})
 root=depth_root(doc['output'])
 source_href=os.path.relpath(doc['source'],doc['output'].parent).replace(os.sep,'/')
 intro=f'<div class="eyebrow">{esc(doc["course"]["name"])} · 完整讲义</div><h1 class="page-title">{esc(doc["title"])}</h1><p class="page-deck">{esc(doc["description"] or "按照原始 Markdown 完整保留正文层次、公式和语义提示块。")}</p><div class="meta-line">完整迁移 · 可调字号与行距 · <a href="{esc(source_href)}">查看 Markdown 原文</a></div>'
 inner=f'<div class="reading-head">{intro}</div><article class="reading-content" data-pagefind-body>{soup}</article>'
 extra=f'<script defer src="{root}assets/lab.js"></script>' if key=='physics/12 气体动理论.md' else ''
 if key in WIDGETS:extra+=f'<script defer src="{root}assets/physics-widgets.js"></script>'
 if key in STEPS or key in TRUTHS:extra+=f'<script defer src="{root}assets/learning-widgets.js"></script>'
 doc['output'].parent.mkdir(parents=True,exist_ok=True)
 doc['output'].write_text(wrap(doc['title'],'完整 Markdown 转换',inner,doc['output'],ALL_DOCS,toc=heads,extra_script=extra),encoding='utf-8')
 return {'headings':heads,'source_headings':len(re.findall(r'^#{1,6} ',text,re.M)),'math_count':batch.math_counts.get(key,0),'svg_count':len(soup.select('.math-inline,.math-display')),'callout_count':callout_count,'source_callouts':len(re.findall(r'^>\s*(?:>\s*)*\[!\w+\]',text,re.M)),'tables':len(soup.select('table')),'visual_count':visual_count,'asset_visual_count':asset_visual_count,'search':snippet_entries}

def map_html(heads):
 def link(prefix):
  for h in heads:
   if prefix in h['title']:return '12-gas-theory.html#'+h['id']
  return '12-gas-theory.html'
 branches=[
  ('基础状态','#5089ad',[('热平衡和温度','1.2.1'),('平衡态 / 稳恒态','1.1.2'),('准静态过程','1.1.4'),('物态方程','1.3.4')]),
  ('气体微观模型','#6d9d8a',[('四条微观假设','2.1.2'),('各向同性统计假设','2.1.3'),('分子数密度','1.3.4'),('宏观与微观量','2.1.1')]),
  ('压强与温度','#b08b63',[('压强公式','2.2.2'),('分子碰撞器壁','2.2.1'),('平均平动动能','2.3.1'),('方均根速率','2.3.3')]),
  ('能量与内能','#ab82a3',[('自由度','2.4.1'),('能量均分','2.4.2'),('内能公式','2.4.3'),('内能仅与温度有关','2.4.3')]),
  ('统计速率','#648cb9',[('最概然速率','3.2.3'),('平均速率','3.2.3'),('方均根速率','3.2.3'),('三种速率关系','3.2.3')]),
  ('速率分布','#5e9d91',[('分布函数','3.2.1'),('麦克斯韦分布','3.2.2'),('温度与曲线','3.2.4'),('区间概率','3.2.5')]),
  ('碰撞与输运','#b38e64',[('平均碰撞频率','4.1.1'),('平均自由程','4.1.1'),('碰撞公式','4.1.2'),('恒压/恒容升温','4.1.2')]),
  ('复习与辨析','#957bb0',[('公式速查','五、总结'),('高频易错点','五、总结'),('温度统计意义','2.3.1'),('内能与自由度','2.4.3')])]
 def card(t):
  name,color,leaves=t
  items=''.join(f'<a class="map-leaf" href="{esc(link(sub))}"><b>{esc(label)}</b><span class="leaf-sub">定位讲义知识点 ↗</span></a>' for label,sub in leaves)
  return f'<details class="map-branch" style="--branch:{color}" open><summary class="map-branch-head"><b>{esc(name)}</b><span class="fold-icon" aria-hidden="true">⌄</span></summary><div class="map-branch-body">{items}</div></details>'
 left=''.join(map(card,branches[:4]));right=''.join(map(card,branches[4:]))
 return f'''<div class="map-wrap"><div class="map-intro"><div class="eyebrow">大学物理 · 第12章 · 知识结构</div><h1 class="map-title">气体动理论 · 双侧思维导图</h1><p class="map-desc">左右共八条主分支，点击任意知识点可直达讲义对应段落。双侧结构是原生 HTML，默认可横向滚动；脚本只负责辅助缩放和连线。</p><div class="map-tools"><button id="mapZoomOut" type="button">缩小 −</button><span class="map-zoom" id="zoomValue">100%</span><button id="mapZoomIn" type="button">放大 ＋</button><button id="mapFit" type="button">适合窗口</button><button id="mapExpand" type="button">全部展开</button><button id="mapCollapse" type="button">全部折叠</button><a href="12-gas-theory.html">阅读完整讲义 ↗</a></div></div><div class="map-stage" id="mapStage" tabindex="0" aria-label="左右双侧知识导图，可滚动查看"><div class="map-sizer" id="mapSizer"><div class="map-plane" id="mapPlane"><div class="map-grid" id="mapGrid"><svg class="map-lines" id="mapLines" aria-hidden="true"></svg><div class="map-col left">{left}</div><div class="map-core" id="mapCore"><small>第12章</small><b>气体动理论</b><em>知识中心</em></div><div class="map-col right">{right}</div></div></div></div></div><p class="map-help">操作：单击分支标题折叠；点击知识点跳转；滚动查看画布，使用上方按钮缩放。即使 JavaScript 未运行，所有知识分支和链接仍然可用。</p></div>'''

def outline_map_html(doc,heads):
 first_level=sum(h['level']==1 for h in heads)
 branch_level=1 if first_level>1 else 2
 groups=[];current=None
 for i,h in enumerate(heads):
  if h['level']<branch_level:continue
  if h['level']==branch_level:
   if (branch_level==1 and i==0) or h['title'].strip()=='目录':
    current=None;continue
   current={'head':h,'children':[]};groups.append(current)
  elif current is not None:
   current['children'].append(h)
 if not groups:groups=[{'head':heads[0],'children':heads[1:]}]
 palette=['#5089ad','#6d9d8a','#b08b63','#ab82a3','#648cb9','#5e9d91','#b38e64','#957bb0']
 article=os.path.relpath(doc['output'],map_output(doc).parent).replace(os.sep,'/')
 def card(group,index):
  head=group['head'];color=palette[index%len(palette)]
  leafs=[f'<a class="map-leaf map-section-link" href="{esc(article+"#"+head["id"])}"><b>阅读本节</b><span class="leaf-sub">定位正文 ↗</span></a>']
  for h in group['children']:
   leafs.append(f'<a class="map-leaf map-depth-{min(h["level"]-branch_level,3)}" href="{esc(article+"#"+h["id"])}"><b>{esc(h["title"])}</b><span class="leaf-sub">定位讲义 ↗</span></a>')
  return f'<details class="map-branch" style="--branch:{color}" open><summary class="map-branch-head"><b>{esc(head["title"])}</b><span class="fold-icon" aria-hidden="true">⌄</span></summary><div class="map-branch-body">{"".join(leafs)}</div></details>'
 split=(len(groups)+1)//2
 left=''.join(card(g,i) for i,g in enumerate(groups[:split]))
 right=''.join(card(g,i+split) for i,g in enumerate(groups[split:]))
 return f'''<div class="map-wrap outline-map"><div class="map-intro"><div class="eyebrow">{esc(doc['course']['name'])} · 章节知识结构</div><h1 class="map-title">{esc(doc['title'])} · 思维导图</h1><p class="map-desc">依据本文标题层级生成，含 {len(groups)} 个主分支。每个知识节点都链接到对应讲义段落；折叠、导航无需 JavaScript。</p><div class="map-tools"><button id="mapZoomOut" type="button">缩小 −</button><span class="map-zoom" id="zoomValue">100%</span><button id="mapZoomIn" type="button">放大 ＋</button><button id="mapFit" type="button">适合窗口</button><button id="mapExpand" type="button">全部展开</button><button id="mapCollapse" type="button">全部折叠</button><a href="{esc(article)}">阅读完整讲义 ↗</a></div></div><div class="map-stage" id="mapStage" tabindex="0" aria-label="双侧知识导图，可滚动查看"><div class="map-sizer" id="mapSizer"><div class="map-plane" id="mapPlane"><div class="map-grid" id="mapGrid"><svg class="map-lines" id="mapLines" aria-hidden="true"></svg><div class="map-col left">{left}</div><div class="map-core" id="mapCore"><small>{esc(doc['course']['name'])}</small><b>{esc(doc['title'])}</b><em>知识中心</em></div><div class="map-col right">{right}</div></div></div></div></div><p class="map-help">点击分支标题折叠；点击知识节点跳转；滚动浏览，或使用上方按钮缩放。导图正文和链接在脚本关闭时仍可阅读。</p></div>'''

def special_pages(docs,meta):
 target=next((d for d in docs if d['source_rel']=='physics/12 气体动理论.md'),None)
 if not target:return
 output=target['output'];heads=meta[target['source_rel']]['headings'];folder=output.parent
 lab_html=(ROOT/'templates/lab_content.html').read_text(encoding='utf8')
 lab_out=folder/'12-lab.html';lab_out.write_text(wrap('麦克斯韦速率分布','函数交互实验室',lab_html,lab_out,docs,current='lab',article_class='experiment-page',extra_script=f'<script defer src="{depth_root(lab_out)}assets/lab.js"></script>'),encoding='utf8')

def make_maps(docs,meta):
 for doc in docs:
  output=map_output(doc);heads=meta[doc['source_rel']]['headings']
  inner=map_html(heads) if doc['source_rel']=='physics/12 气体动理论.md' else outline_map_html(doc,heads)
  output.write_text(wrap(doc['title']+' · 思维导图','可交互知识地图',inner,output,docs,current='map',article_class='map-page',extra_script=f'<script defer src="{depth_root(output)}assets/mindmap.js"></script>'),encoding='utf8')

def make_course_pages(docs):
 for c in COURSES:
  mine=[d for d in docs if d['course']['id']==c['id']]
  if not mine:continue
  output=ROOT/'subjects'/c['id']/'index.html'
  output.parent.mkdir(parents=True,exist_ok=True)
  items=[]
  for i,d in enumerate(mine,1):
   href=os.path.relpath(d['output'],output.parent).replace(os.sep,'/')
   map_href=os.path.relpath(map_output(d),output.parent).replace(os.sep,'/')
   items.append(f'<li><a class="course-note" href="{esc(href)}"><span class="course-note-number">{i:02d}</span><span class="course-note-copy"><strong>{esc(d["title"])}</strong><small>{esc(d["description"] or "完整 Markdown 知识笔记")}</small></span><span class="course-note-arrow" aria-hidden="true">→</span></a><a class="course-map-shortcut" href="{esc(map_href)}">查看本篇思维导图 →</a></li>')
  extras=''
  if c['id']=='physics' and any(d['source_rel']=='physics/12 气体动理论.md' for d in mine):
   extras='<section class="course-extras"><h2>配套学习工具</h2><div class="course-extra-links"><a href="12-lab.html">麦克斯韦速率分布实验室 →</a></div></section>'
  inner=f'<div class="course-content"><a class="course-back" href="../../index.html">← 返回知识库总览</a><div class="reading-head"><div class="eyebrow">课程知识体系 · {len(mine)} 篇笔记</div><h1 class="page-title">{esc(c["name"])}</h1><p class="page-deck">按章节顺序阅读本课程的全部知识笔记。选择一篇即可进入完整讲义。</p></div><section class="course-notes" id="course-notes"><h2>全部笔记</h2><ol class="course-note-list">{"".join(items)}</ol></section>{extras}</div>'
  output.write_text(wrap(c['name'],'课程总览',inner,output,docs,current='course',toc=[{'id':'course-notes','level':2,'title':'全部笔记'}],article_class='course-page'),encoding='utf8')

def make_home(docs):
 items=[]
 for c in COURSES:
  mine=[d for d in docs if d['course']['id']==c['id']]
  if mine:
   preview=' · '.join(d['title'] for d in mine[:3])+(' · …' if len(mine)>3 else '')
   href=global_url(ROOT/'subjects'/c['id']/'index.html')
   items.append(f'<a class="course-card" href="{esc(href)}"><div class="topline">{esc(c["name"])} · {len(mine)} 篇</div><h3>{esc(c["name"])}</h3><p class="course-preview">{esc(preview)}</p><span class="course-enter">进入课程，查看全部笔记 <span aria-hidden="true">→</span></span></a>')
  else:items.append(f'<div class="empty-card">{esc(c["name"])}<small>将 Markdown 放入 sources/{esc(c["id"])}/ 后构建即可显示</small></div>')
 homepage='<div class="home-content"><div class="home-kicker">个人知识库 · V3</div><h1>为阅读而设计的知识空间。</h1><p class="home-lead">原始 Markdown 不改写，完整生成 HTML 讲义；彩色语义提示块、LaTeX 矢量公式、课程树导航和可交互的知识图谱共同服务于学习。</p><div class="home-section-head"><h2>我的课程</h2><small>自动扫描与收录</small></div><div class="home-empty">'+''.join(items)+'</div><div class="home-section-head"><h2>样式验收</h2></div><p><a href="docs/Callout_色彩预览.html">查看全部 Obsidian Callout 语义颜色 →</a></p></div>'
 (ROOT/'index.html').write_text(wrap('首页','我的课程',homepage,ROOT/'index.html',docs,current='home'),encoding='utf8')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true',help='Build then validate conversions and local links');args=parser.parse_args()
 ALL_DOCS=docs_list()
 if not ALL_DOCS:sys.exit('No Markdown files found under sources/<course-id>/')
 b=Batch()
 for d in ALL_DOCS:
  key=d['source_rel'];b.protected=getattr(b,'protected',{})
  b.protected[key]=b.protect(d['source'].read_text(encoding='utf8'),key)
 svg=b.render_all();entries=[];meta={}
 for d in ALL_DOCS:
  result=transform(d,b,svg);meta[d['source_rel']]=result;entries.extend(result['search'])
  print(f'✓ {d["source_rel"]} → {global_url(d["output"])} : {result["math_count"]} math, {result["callout_count"]} callouts')
 special_pages(ALL_DOCS,meta);make_maps(ALL_DOCS,meta);make_course_pages(ALL_DOCS);make_home(ALL_DOCS)
 (ROOT/'assets/search-data.js').write_text('window.HKB_SEARCH_INDEX='+json.dumps(entries,ensure_ascii=False)+';\n',encoding='utf8')
 report={'version':'3.1','files':{k:{name:value for name,value in v.items() if name not in ('headings','search')} for k,v in meta.items()},'total_documents':len(ALL_DOCS),'total_search_entries':len(entries),'warnings':b.warnings,'math_errors':b.math_errors}
 (ROOT/'docs/conversion-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 if args.check:
  errors=[]
  for d in ALL_DOCS:
   r=meta[d['source_rel']]
   if r['source_headings']!=len(r['headings']):errors.append(d['source_rel']+': heading mismatch')
   if r['math_count']!=r['svg_count']:errors.append(d['source_rel']+': math mismatch')
   if r['callout_count']!=r['source_callouts']:errors.append(d['source_rel']+': callout mismatch')
   if r['visual_count']!=len(SPECS.get(d['source_rel'],[]))+len(EXTRA_SPECS.get(d['source_rel'],[]))+len(WIDGETS.get(d['source_rel'],[]))+int(d['source_rel'] in STEPS)+int(d['source_rel'] in TRUTHS)+r['asset_visual_count']:errors.append(d['source_rel']+': visual mismatch')
   if r['visual_count']<15:errors.append(d['source_rel']+': fewer than 15 teaching figures')
   if d['source_rel']=='physics/14 振动 扩充版.md' and r['asset_visual_count']!=len(ASSET_DIAGRAMS):errors.append(d['source_rel']+': redraw count mismatch')
   article=BeautifulSoup(d['output'].read_text(encoding='utf8'),'html.parser')
   if len(article.select('article figure.concept-visual svg'))!=r['visual_count']:errors.append(d['source_rel']+': generated SVG diagram mismatch')
   map_page=map_output(d)
   if not map_page.is_file() or not BeautifulSoup(map_page.read_text(encoding='utf8'),'html.parser').select('details.map-branch a.map-leaf[href]'):
    errors.append(d['source_rel']+': mind map missing or empty')
  errors.extend('math render failed: '+message for message in b.math_errors)
  id_cache={}
  for page in [ROOT/'index.html',*ROOT.glob('subjects/**/*.html')]:
   soup=BeautifulSoup(page.read_text(encoding='utf8'),'html.parser')
   for e in soup.select('[src],[href]'):
    v=e.get('href') or e.get('src')
    if not v or v.startswith(('http:','https:','data:','mailto:','#')):continue
    file=(page.parent/unquote(v.split('#')[0].split('?')[0])).resolve()
    if not file.exists():errors.append(f'{global_url(page)}: missing {v}')
    elif '#' in v and file.suffix.lower() in ('.html','.htm'):
     if file not in id_cache:
      target=BeautifulSoup(file.read_text(encoding='utf8'),'html.parser')
      id_cache[file]={n['id'] for n in target.select('[id]')}
     if unquote(v.split('#',1)[1]) not in id_cache[file]:errors.append(f'{global_url(page)}: missing anchor {v}')
  if errors:print('\n'.join(errors),file=sys.stderr);sys.exit(1)
  print('PASS: heading/formula/callout counts and local assets/links')
  if b.warnings:print('Warnings (manual review required):',*b.warnings,sep='\n - ')
 print('DONE:',len(ALL_DOCS),'Markdown documents,',len(entries),'search entries')
