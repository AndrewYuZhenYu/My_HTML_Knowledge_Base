// Build-time SVG formula renderer. Output remains fully offline in the published HTML.
const fs = require('fs');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');
const adaptor = liteAdaptor(); RegisterHTMLHandler(adaptor);
const tex = new TeX({packages:AllPackages});
const svg = new SVG({fontCache:'none'});
const doc = mathjax.document('',{InputJax:tex, OutputJax:svg});
const formulas = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const result = {};
for(const f of formulas){
 try {const node=doc.convert(f.tex,{display:f.display});result[f.key]=adaptor.outerHTML(node);}
 catch(e){result[f.key]=`<span class="formula-error" title="${String(e).replaceAll('"','&quot;')}">${f.tex.replaceAll('<','&lt;')}</span>`}
}
fs.writeFileSync(process.argv[3],JSON.stringify(result));
