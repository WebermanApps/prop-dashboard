/* Property panel: tiles, 12-month tracker (temporary; pattern from UpKeep ccm-cov-strip), attention, breakdown, documents. */
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const payAmt=(p,f)=>p.amount!=null?p.amount:(/in full/i.test(p.label||'')?f.rent:null);
const months=f=>{const ps=(f.rent_payments||[]).slice().sort((a,b)=>a.date<b.date?-1:1);const last=ps.length?ps[ps.length-1].month:new Date().toISOString().slice(0,7);
 let [y,m]=last.split('-').map(Number);const out=[];for(let i=11;i>=0;i--){let mm=m-i,yy=y;while(mm<1){mm+=12;yy--}const key=yy+'-'+String(mm).padStart(2,'0');
  const p=ps.filter(x=>x.month===key);const amt=p.length&&p.every(x=>payAmt(x,f)!=null)?p.reduce((t,x)=>t+payAmt(x,f),0):null;
  const est=f.expenses.some(x=>x.est||x.amount==null)||p.some(x=>x.est);
  out.push({m:MN[mm-1]+' '+yy,key,rent:amt,exp:f.known_total,est,date:p.length?p[p.length-1].date:null})}return out};
const gap=x=>{const n=x.rent-x.exp;return n>=0?'Paid For · +'+usd(+n.toFixed(2))+' ('+Math.round(n/x.exp*100)+'%)':'Short '+usd(+(-n).toFixed(2))+' ('+Math.round(-n/x.exp*100)+'%)'};
const cf12=f=>{const M=months(f),mx=Math.max(1.1,...M.filter(x=>x.rent!=null).map(x=>x.rent/x.exp));
 return `<div id="cf12" data-cf12-slot="temporary" data-cf12-source="upkeep ccm-cov-strip pattern"><div class="cf-h"><b>12-Month Cash Flow</b><span class="muted">rent vs known expenses${star(1)}</span></div><div class="cf-strip">`+M.map(x=>{
  if(x.rent==null)return `<span class="nd" title="${x.m}: no data"><div class="bx"><i></i><u style="bottom:${100/mx}%"></u></div><em>${x.m[0]}</em></span>`;
  const ok=x.rent>=x.exp;return `<span class="${ok?'ok':'bad'}" title="${x.m}: ${gap(x)}${x.est?' (estimated)':''}"><div class="bx"><i style="height:${Math.max(6,x.rent/x.exp/mx*100)}%"></i><u style="bottom:${100/mx}%"></u></div><em>${x.m[0]}${x.est?'<sup class="star">*</sup>':''}</em></span>`}).join('')+
  `</div><small class="muted">Grey = no data. Dashed line = break-even.</small></div>`};
const fold=(label,amt,body,cls='')=>`<details class="fold li ${cls}"><summary><span class="lt">${esc(label)}</span><span class="la">${amt}</span></summary><div class="ld">${body}</div></details>`;
const noDet='<p class="muted">No details yet</p>';
const short=l=>l.replace(/\s*\(.*\)\s*/,'').trim(),paren=l=>(l.match(/\((.*)\)/)||[])[1];
const expRow=x=>{const bits=[];if(paren(x.label))bits.push(paren(x.label));if(x.amount!=null)bits.push('Amount: '+usd(x.amount)+(x.est?' (estimated)':''));
 if(x.source&&x.amount!=null)bits.push('Source: '+x.source+(x.as_of?' · '+fmt(x.as_of):''));
 const ent=(x.entries||[]).map(e=>`<li>${e.date?fmt(e.date)+' · ':''}${esc(e.label||'')}${e.amount!=null?' · '+usd(e.amount):''}</li>`).join('');
 const body=(bits.length||ent)?(bits.map(b=>`<p>${esc(b)}</p>`).join('')+(ent?`<ul class="plain">${ent}</ul>`:'')):noDet+(x.source?`<p class="muted">${esc(x.source)}</p>`:'');
 return fold(short(x.label),usd(x.amount)+star(x.est||x.amount==null),body)};
const ATT_ST={missing:['Missing','bad'],needs_check:['Needs check','warn'],ok:['OK','ok']};
const attention=f=>{const a=(f.attention||[]).slice();(f.docs||[]).filter(d=>d.status==='missing').forEach(d=>a.push({item:d.slot+': '+d.title,status:'missing',note:'Document missing'}));
 const n=a.filter(x=>x.status!=='ok').length;
 return `<details class="fold att${n?' has':''}"><summary><span class="att-b">${n?n+' need attention':'All clear'}</span><span class="muted">Insurance, lease, registration</span></summary><ul class="att-l">`+a.map(x=>{const s=ATT_ST[x.status]||ATT_ST.needs_check;
  return `<li><span class="att-s ${s[1]}">${s[0]}</span><span><b>${esc(x.item)}</b>${x.date?' · '+new Date(x.date+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}):''}${x.note?`<small>${esc(x.note)}</small>`:''}</span></li>`}).join('')+`</ul></details>`};
const DST={on_file:['On File','ok'],missing:['Missing','bad'],needs_check:['Needs check','warn'],na:['N/A','na']};
const docsSec=(id,f)=>{const ds=f.docs||[];let gone=[];try{gone=JSON.parse(localStorage.getItem('propDocHide')||'[]')}catch(e){}
 const rows=ds.map((d,i)=>({d,k:id+':'+d.slot+':'+d.title})).filter(r=>!(r.d.status!=='on_file'&&!r.d.doc_id&&gone.includes(r.k)));
 const nOn=ds.filter(d=>d.status==='on_file').length,nMis=ds.filter(d=>d.status==='missing').length;
 const fo=`<details class="fold pdocs-fold"><summary><span class="lt">Documents · ${nOn} on file · ${nMis} missing</span></summary>`;
 if(!rows.length)return fo+'<p class="muted">No documents yet</p></details>';
 return fo+'<ul class="op-list pdocs">'+rows.map(({d,k})=>{const s=DST[d.status]||DST.needs_check;
  const t=d.link?`<a href="${esc(d.link)}" target="_blank" rel="noopener noreferrer">${esc(d.title)}</a>`:d.doc_id?`<a href="#" data-doc-open="${esc(d.title)}">${esc(d.title)}</a>`:`<span>${esc(d.title)}</span>`;
  return `<li><span class="att-s ${s[1]}">${s[0]}</span><div class="op-lt"><small>${esc(d.slot)}</small>${t}${d.note?`<small>${esc(d.note)}</small>`:''}</div><button type="button" class="tdx mw-hover pdx" data-k="${esc(k)}" ${d.doc_id?`data-doc-rm="${esc(d.title)}"`:''} aria-label="Remove ${esc(d.title)}">×</button></li>`}).join('')+'</ul></details>'};
const breakdown=(f,id)=>{if(!f)return '<p class="muted">Waiting for records</p>';
 const M=months(f),rec=M.filter(x=>x.rent!=null).pop(),ps=(f.rent_payments||[]).slice().sort((a,b)=>a.date<b.date?-1:1),lp=ps[ps.length-1];
 const late=lp?+lp.date.slice(8)>5:null,anyEst=f.expenses.some(x=>x.est||x.amount==null);
 const tiles=`<div class="bign b4"><div><span>Rent / Mo</span><b>${usd(f.rent)}</b></div>
 <div><span>Cash Flow · ${rec?rec.m.slice(0,3):'—'}</span><b class="${rec&&rec.rent<rec.exp?'neg':'pos'}">${rec?usd(+(rec.rent-rec.exp).toFixed(2))+star(rec.est):'No data'}</b></div>
 <div><span>Rent Status</span><b class="${late?'neg':'pos'}">${lp?(late?'Late':'On Time')+star(lp.est):'No data'}</b><small>${lp?'Received '+fmt(lp.date):''}</small></div>
 <div><span>Projected Annual</span><b class="pos">${usd(+(f.cash_flow*12).toFixed(2))}${star(f.cash_flow_est)}</b><small>cash flow × 12</small></div></div>`;
 const exps=f.expenses.slice().sort((a,b)=>(/repair/i.test(b.label)?1:0)-(/repair/i.test(a.label)?1:0));
 const payList=ps.length?'<ul class="plain">'+ps.map(p=>`<li>${fmt(p.date)} · ${payAmt(p,f)!=null?usd(payAmt(p,f)):esc(p.detail||'Amount not recorded')}${star(p.est)}</li>`).join('')+'</ul>':noDet;
 const table=`<h3 class="caps">Monthly Breakdown</h3><div class="lines">${exps.map(expRow).join('')}
 ${fold('Rent',usd(f.rent),payList)}
 <div class="li tot"><span class="lt">Known Expenses</span><span class="la">${usd(f.known_total)}${star(anyEst)}</span></div>
 <div class="li tot"><span class="lt">Cash Flow</span><span class="la">${usd(f.cash_flow)}${star(f.cash_flow_est)}</span></div></div>
 <h3 class="caps">Annual</h3><div class="lines"><div class="li"><span class="lt">Rent</span><span class="la">${usd(f.rent*12)}</span></div>
 <div class="li"><span class="lt">Known Expenses</span><span class="la">${usd(+(f.known_total*12).toFixed(2))}${star(1)}</span></div>
 <div class="li tot"><span class="lt">Cash Flow</span><span class="la">${usd(+(f.cash_flow*12).toFixed(2))}${star(1)}</span></div></div>
 ${f.extra.map(x=>`<p class="fp"><b>${esc(x.label)}:</b> ${esc(x.value)} <span class="pill">${esc(x.note)}</span></p>`).join('')}
 ${f.notes.map(n=>`<p class="fp muted">${esc(n)}</p>`).join('')}`;
 return tiles+attention(f)+cf12(f)+table+docsSec(id||'',f)+'<p class="legend">* Estimated, computed from estimated data, or waiting for records</p>'};
/* documents: open / X go through the kit Document Center card for that title (same open + Remove flow) */
document.addEventListener('click',e=>{const o=e.target.closest('[data-doc-open],[data-doc-rm],.pdx');if(!o)return;
 const kit=t=>[...document.querySelectorAll('#mw-projects .op-card,#mw-projects .op-list li')].find(c=>(c.getAttribute('aria-label')||(c.querySelector('b')||{}).textContent)===t);
 if(o.dataset.docOpen){e.preventDefault();const c=kit(o.dataset.docOpen);const b=c&&c.querySelector('.op-btn--open');if(b)b.click();else alert('Unlock the dashboard first');return}
 if(o.dataset.docRm){const c=kit(o.dataset.docRm),fd=document.getElementById('mw-docs-fold');if(fd)fd.open=true;const host=c&&c.closest('details.op-older');if(host)host.open=true;const b=c&&c.querySelector('.op-rm-btn');if(b){c.scrollIntoView({behavior:'smooth',block:'center'});b.click()}return}
 let g=[];try{g=JSON.parse(localStorage.getItem('propDocHide')||'[]')}catch(_){}g.push(o.dataset.k);try{localStorage.setItem('propDocHide',JSON.stringify(g))}catch(_){}o.closest('li').remove()});
