// Real Maxwell speed distribution. Single SVG dynamically generated from the formula.
(()=>{
'use strict';const R=8.31;const gases={o2:{M:0.032,name:'氧气 O₂'},n2:{M:0.028,name:'氮气 N₂'},h2:{M:0.002,name:'氢气 H₂'},he:{M:0.004,name:'氦气 He'}};
const $=id=>document.getElementById(id);const select=$('gasSelect'),temp=$('tempSelect'),tempLabel=$('tempLabel');
const svg=$('maxwellPlot');let locked=false;
function density(v,T,M){let x=M/(2*Math.PI*R*T);return 4*Math.PI*Math.pow(x,1.5)*v*v*Math.exp(-M*v*v/(2*R*T))}
const f=n=>Number(n).toFixed(0);
function make(){const g=gases[select.value],T=+temp.value,M=g.M;tempLabel.textContent=T+' K';const vp=Math.sqrt(2*R*T/M),mean=Math.sqrt(8*R*T/(Math.PI*M)),rms=Math.sqrt(3*R*T/M);
 $('statVp').textContent=f(vp)+' m/s';$('statMean').textContent=f(mean)+' m/s';$('statRms').textContent=f(rms)+' m/s';
 const T2=Math.min(900,Math.max(350,T*1.7));const xmax=Math.ceil(Math.sqrt(3*R*Math.max(T,T2)/M)*2.4/300)*300;const n=240;
 let ymax=0;for(let i=0;i<=n;i++){let v=i*xmax/n;ymax=Math.max(ymax,density(v,T,M),density(v,T2,M))}ymax*=1.16;
 const W=820,H=365,left=67,right=25,top=26,bottom=55,pw=W-left-right,ph=H-top-bottom;
 const X=v=>left+(v/xmax)*pw,Y=y=>top+ph-(y/ymax)*ph;
 const colors=['#3675bd','#d39959'];
 const path=(t)=>Array.from({length:n+1},(_,i)=>{let v=i*xmax/n;return(i?'L':'M')+X(v).toFixed(2)+' '+Y(density(v,t,M)).toFixed(2)}).join(' ');
 let grid='';for(let j=0;j<=4;j++){let y=top+ph*j/4;grid+=`<line x1="${left}" y1="${y}" x2="${left+pw}" y2="${y}" stroke="currentColor" stroke-opacity=".11"/>`}
 for(let j=0;j<=5;j++){let x=left+pw*j/5;grid+=`<line x1="${x}" y1="${top}" x2="${x}" y2="${top+ph}" stroke="currentColor" stroke-opacity=".06"/><text x="${x}" y="${top+ph+23}" text-anchor="middle" fill="currentColor" opacity=".55" font-size="12">${f(xmax*j/5)}</text>`}
 svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML=`<g>${grid}</g><line x1="${left}" y1="${top}" x2="${left}" y2="${top+ph}" stroke="currentColor" stroke-opacity=".45"/><line x1="${left}" y1="${top+ph}" x2="${left+pw}" y2="${top+ph}" stroke="currentColor" stroke-opacity=".45"/><text x="${left}" y="15" font-size="13" fill="currentColor" opacity=".8">f(v)</text><text x="${W/2}" y="${H-8}" text-anchor="middle" font-size="13" fill="currentColor" opacity=".8">速率 v（m/s）</text><path d="${path(T2)}" stroke="${colors[1]}" stroke-dasharray="7 6" stroke-width="3" fill="none"/><path d="${path(T)}" stroke="${colors[0]}" stroke-width="3.3" fill="none"/><line x1="${X(vp)}" y1="${Y(density(vp,T,M))}" x2="${X(vp)}" y2="${top+ph}" stroke="${colors[0]}" stroke-opacity=".5" stroke-dasharray="3 4"/><circle cx="${X(vp)}" cy="${Y(density(vp,T,M))}" r="5" fill="${colors[0]}" stroke="white" stroke-width="2"/>`;
 $('legend1').textContent=`${T} K`; $('legend2').textContent=`${T2} K（对照）`;
 $('formulaSummary').textContent=`相同气体（${g.name}）的温度从 ${T} K 升至 ${T2} K，分布峰向右移动，曲线变矮、变宽，但曲线下的总面积始终为 1。`;
}
select.addEventListener('change',make);temp.addEventListener('input',make);make();
})();
