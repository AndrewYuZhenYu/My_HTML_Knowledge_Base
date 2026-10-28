/* Reader-first, dependency-free interactions. All settings stay on the device. */
(()=>{
'use strict';
const $=id=>document.getElementById(id);
const html=document.documentElement;
const get=(key,fallback)=>{try{return localStorage.getItem('hkb:'+key)??fallback}catch(e){return fallback}};
const set=(key,val)=>{try{localStorage.setItem('hkb:'+key,String(val))}catch(e){}};
const read={font:Math.max(16,Math.min(26,+get('font','19'))),line:+get('line','1.85'),wide:get('wide','false')==='true',theme:get('theme','light')};
function apply(){html.style.setProperty('--reading-size',read.font+'px');html.style.setProperty('--reading-leading',read.line);html.classList.toggle('site-wide',read.wide);html.dataset.theme=read.theme;$('fontRange').value=read.font;$('lineRange').value=read.line;$('fontVal').textContent=read.font+'px';$('lineVal').textContent=read.line.toFixed(2);$('wideToggle').textContent=read.wide?'关闭':'开启'}
apply();
$('fontRange').addEventListener('input',e=>{read.font=+e.target.value;set('font',read.font);apply()});
$('lineRange').addEventListener('input',e=>{read.line=+e.target.value;set('line',read.line);apply()});
$('wideToggle').onclick=()=>{read.wide=!read.wide;set('wide',read.wide);apply()};
function theme(){read.theme=read.theme==='dark'?'light':'dark';set('theme',read.theme);apply()}
$('themeToggle').onclick=theme;$('themeSetting').onclick=theme;
$('restoreDefaults').onclick=()=>{read.font=19;read.line=1.85;read.wide=false;['font','line','wide'].forEach(k=>set(k,read[k]));apply()};
function typography(show){$('typePanel').hidden=show===undefined?!$('typePanel').hidden:!show}
$('openTypography').onclick=()=>typography($('typePanel').hidden);$('closeTypography').onclick=()=>typography(false);
let fallbackFocus=false;
function syncFocus(){
 const native=!!document.fullscreenElement,active=native||fallbackFocus,button=$('focusToggle');
 html.classList.toggle('focused',active);
 button.setAttribute('aria-pressed',String(active));
 const label=native?'退出全屏':fallbackFocus?'退出专注阅读':document.fullscreenEnabled?'进入全屏阅读':'进入专注阅读';
 button.setAttribute('aria-label',label);button.title=label;
 $('focusLabel').textContent=native?'退出全屏':fallbackFocus?'专注中':document.fullscreenEnabled?'全屏':'专注';
}
$('focusToggle').onclick=async()=>{
 if(document.fullscreenElement){await document.exitFullscreen();return}
 if(fallbackFocus){fallbackFocus=false;syncFocus();return}
 if(document.fullscreenEnabled&&document.documentElement.requestFullscreen){
  try{await document.documentElement.requestFullscreen();syncFocus();return}catch(e){}
 }
 fallbackFocus=true;syncFocus();
};
document.addEventListener('fullscreenchange',syncFocus);
syncFocus();
const mobileNav=matchMedia('(max-width:760px)'),compactToc=matchMedia('(max-width:1130px)');
const panels={left:get('leftOpen','true')!=='false',right:get('rightOpen','true')!=='false'};
let navDrawerOpen=false,tocDrawerOpen=false;
for(const id of ['navToggle','tocToggle','sidebarClose','tocClose'])$(id).hidden=false;
function syncPanels(){
 html.classList.toggle('left-collapsed',!mobileNav.matches&&!panels.left);
 html.classList.toggle('right-collapsed',!compactToc.matches&&!panels.right);
 html.classList.toggle('toc-drawer-open',tocDrawerOpen&&compactToc.matches);
 $('sidebar').classList.toggle('open',navDrawerOpen&&mobileNav.matches);
 $('mobileShade').hidden=!(navDrawerOpen&&mobileNav.matches||tocDrawerOpen&&compactToc.matches);
 const leftVisible=mobileNav.matches?navDrawerOpen:panels.left,rightVisible=compactToc.matches?tocDrawerOpen:panels.right;
 for(const [id,open,label] of [['navToggle',leftVisible,'课程导航'],['tocToggle',rightVisible,'本页目录']]){
  const button=$(id);button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',(open?'收起':'展开')+label);button.title=(open?'收起':'展开')+label;
 }
}
function closeMobile(){navDrawerOpen=false;tocDrawerOpen=false;syncPanels()}
function toggleLeft(){
 if(mobileNav.matches){navDrawerOpen=!navDrawerOpen;tocDrawerOpen=false}
 else{panels.left=!panels.left;set('leftOpen',panels.left)}
 syncPanels();
}
function toggleRight(){
 if(compactToc.matches){tocDrawerOpen=!tocDrawerOpen;navDrawerOpen=false}
 else{panels.right=!panels.right;set('rightOpen',panels.right)}
 syncPanels();
}
$('navToggle').onclick=toggleLeft;$('sidebarClose').onclick=toggleLeft;
$('tocToggle').onclick=toggleRight;$('tocClose').onclick=toggleRight;
$('mobileShade').onclick=closeMobile;
addEventListener('resize',()=>{navDrawerOpen=false;tocDrawerOpen=false;syncPanels()},{passive:true});
syncPanels();
const overlay=$('searchOverlay');const searchInput=$('searchInput');
function searchOpen(){overlay.hidden=false;typography(false);searchInput.focus();renderResults(searchInput.value)}
function searchClose(){overlay.hidden=true}
$('openSearch').onclick=searchOpen;
overlay.addEventListener('click',e=>{if(e.target===overlay)searchClose()});
document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();searchOpen()}if(e.key==='Escape'){searchClose();typography(false);closeMobile();if(fallbackFocus){fallbackFocus=false;syncFocus()}} });
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const hrefFor=url=>{let root=new URL(document.querySelector('link[href*="assets/style.css"]').href); return new URL('../'+url,root).href};
function renderResults(q){
 const parent=$('searchResults');let key=(q||'').trim().toLowerCase();if(!key){parent.innerHTML='<div class="search-empty">输入关键词后，可在已导入的完整课程笔记中查找知识。</div>';return}
 const arr=(window.HKB_SEARCH_INDEX||[]).map(d=>{let title=(d.title||'').toLowerCase(),body=(d.text||'').toLowerCase();let a=title.indexOf(key),b=body.indexOf(key);return{...d,score:a>=0?100-a:b>=0?30-Math.min(b/20,20):0,pos:b}}).filter(d=>d.score>0).sort((a,b)=>b.score-a.score).slice(0,13);
 if(!arr.length){parent.innerHTML='<div class="search-empty">没有找到匹配的标题或正文片段。</div>';return}
 parent.innerHTML=arr.map(d=>{let text=d.text||'';let start=d.pos>=0?Math.max(0,d.pos-35):0;let snippet=text.slice(start,start+125);return `<a class="result-item" href="${esc(hrefFor(d.url))}"><strong>${esc(d.title)}</strong><small>${esc(d.page)}</small><p>${esc(snippet)}${text.length>start+125?'…':''}</p></a>`}).join('');
}
searchInput.addEventListener('input',()=>renderResults(searchInput.value));
// TOC is based on actual HTML headings, so all sections from the original MD are retained.
const toc=$('pageToc');let headings=[];
try{headings=JSON.parse($('tocData').textContent)}catch(e){}
if(headings.length){toc.innerHTML=headings.filter(x=>x.level<=3).map(x=>`<a class="toc-link level-${x.level}" href="#${esc(x.id)}">${esc(x.title)}</a>`).join('');
 const links=[...toc.querySelectorAll('.toc-link')];const ids=headings.map(h=>document.getElementById(h.id)).filter(Boolean);
 function activeToc(){let cur=ids[0]?.id;for(const el of ids){if(el.getBoundingClientRect().top<150)cur=el.id;else break}for(const a of links){a.classList.toggle('active',a.hash.slice(1)===cur)}}
 window.addEventListener('scroll',activeToc,{passive:true});activeToc();
}else{toc.innerHTML='<div class="toc-foot">此页面无需页内目录。</div>';html.classList.add('no-toc');$('tocToggle').hidden=true;$('tocClose').hidden=true}
// Remember last read chapter without tracking or external requests.
if(document.body.dataset.current==='note')set('lastRead',location.pathname+location.hash);
})();
