/* V3 progressive enhancement: the map is visible and linked without JavaScript. */
(()=>{
 'use strict';
 const $=id=>document.getElementById(id);
 const stage=$('mapStage'),sizer=$('mapSizer'),plane=$('mapPlane'),core=$('mapCore'),svg=$('mapLines');
 if(!stage||!sizer||!plane||!core||!svg)return;
 const baseWidth=1510;let scale=1;
 const branches=[...plane.querySelectorAll('details.map-branch')];
 function draw(){
  const canvas=plane.getBoundingClientRect(),center=core.getBoundingClientRect();
  const box=(r)=>({left:(r.left-canvas.left)/scale,right:(r.right-canvas.left)/scale,y:(r.top-canvas.top+r.height*.5)/scale});
  const c=box(center),height=Math.max(plane.offsetHeight,1050);svg.setAttribute('viewBox',`0 0 ${baseWidth} ${height}`);
  svg.innerHTML=branches.map(b=>{
   const left=!!b.closest('.map-col.left'), r=box(b.querySelector('summary').getBoundingClientRect());
   const x1=left?c.left:c.right, x2=left?r.right:r.left,dy=(r.y-c.y),dx=Math.max(35,Math.abs(x2-x1)*.55);
   const color=b.style.getPropertyValue('--branch')||'#7a9ab8';
   return `<path d="M${x1} ${c.y} C${x1+(left?-dx:dx)} ${c.y},${x2+(left?dx:-dx)} ${r.y},${x2} ${r.y}" fill="none" stroke="${color}" stroke-width="2.2" opacity=".72"/>`;
  }).join('');
 }
 function layout(){
  const natural=Math.max(plane.scrollHeight,plane.offsetHeight,1020);
  sizer.style.width=(baseWidth*scale)+'px';sizer.style.height=(natural*scale)+'px';
  plane.style.transform=`scale(${scale})`;
  $('zoomValue').textContent=Math.round(scale*100)+'%';
  requestAnimationFrame(draw);
 }
 function changeScale(next){
  const prev=scale;
  const centerX=(stage.scrollLeft+stage.clientWidth/2)/prev;
  const centerY=(stage.scrollTop+stage.clientHeight/2)/prev;
  scale=Math.max(.34,Math.min(1.65,next));layout();
  stage.scrollLeft=Math.max(0,centerX*scale-stage.clientWidth/2);
  stage.scrollTop=Math.max(0,centerY*scale-stage.clientHeight/2);
 }
 function fit(){
  const next=Math.min(1,(stage.clientWidth-30)/baseWidth);
  scale=Math.max(.34,next);layout();stage.scrollLeft=Math.max(0,(baseWidth*scale-stage.clientWidth)/2);stage.scrollTop=Math.max(0,(sizer.clientHeight-stage.clientHeight)/2);
 }
 $('mapZoomIn').addEventListener('click',()=>changeScale(scale*1.2));
 $('mapZoomOut').addEventListener('click',()=>changeScale(scale/1.2));
 $('mapFit').addEventListener('click',fit);
 $('mapExpand').addEventListener('click',()=>{branches.forEach(b=>b.open=true);requestAnimationFrame(layout)});
 $('mapCollapse').addEventListener('click',()=>{branches.forEach(b=>b.open=false);requestAnimationFrame(layout)});
 branches.forEach(b=>b.addEventListener('toggle',()=>requestAnimationFrame(layout)));
 addEventListener('resize',fit,{passive:true});
 // Start at a readable scale; the explicit Fit button can show the whole width.
 scale=Math.min(1,Math.max(.72,(stage.clientWidth-30)/baseWidth));
 layout();
 stage.scrollLeft=Math.max(0,(baseWidth*scale-stage.clientWidth)/2);
 stage.scrollTop=Math.max(0,(sizer.clientHeight-stage.clientHeight)/2);
})();
