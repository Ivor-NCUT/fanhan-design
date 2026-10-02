const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path').join(__dirname,'../assets/html-starters/green-a25/a25-11.html');
const script=fs.readFileSync(path,'utf8').match(/<script>([\s\S]*)<\/script>/)[1];
const make=(dataset={})=>({dataset,style:{},children:[],attrs:{fill:dataset.color},handlers:{},addEventListener(k,f){this.handlers[k]=f},setAttribute(k,v){this.attrs[k]=v},replaceChildren(){this.children=[]},append(t){this.children.push(t)}});
const title=make({content:'Let’s Work',box:'101,102,1739,371',size:'419.2',color:'#232323'}),green=make({color:'#4f9242'}),palette=make({original:'#4f9242'}),controls={};
const document={createElementNS:()=>make(),querySelector:s=>controls[s]??=make(),querySelectorAll:s=>s==='[data-content]'?[title]:s==='image'?[]:s.startsWith('[fill=')?[green].filter(e=>e.attrs.fill===s.match(/"([^"]*)"/)[1]):s.startsWith('[data-color=')?[green].filter(e=>e.dataset.color===s.match(/"([^"]*)"/)[1]):[]};
vm.runInNewContext(script,{document,prompt:()=>'<script>unsafe</script>',Number,XMLSerializer:class{}});
title.handlers.click();assert.equal(title.children[0].textContent,'<script>unsafe</script>');assert.equal(title.children.length,1);
for(const value of ['#112233','#445566']){palette.value=value;document.querySelector('#palette').handlers.change({target:palette});assert.equal(green.attrs.fill,value);assert.equal(green.dataset.color,value)}
console.log('Text replacement uses textContent; repeated palette changes pass');
