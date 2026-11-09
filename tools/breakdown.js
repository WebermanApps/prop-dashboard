/* Property panel v4 — desktop-first: status row, refined tiles, statement, side cards. */
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const payAmt=(p,f)=>p.amount!=null?p.amount:(/in full/i.test(p.label||'')?f.rent:null);
/* Current lease year: lease_start month through +11 months. Rolls forward when today is past that window. */
const leaseWindow=f=>{
  if(!f.lease_start)return null;
  let [y,m]=f.lease_start.slice(0,7).split('-').map(Number);
  const today=new Date();const ty=today.getFullYear(),tm=today.getMonth()+1;
  // advance whole lease years until today is inside [start, start+12mo)
  for(;;){let ey=y,em=m+12;if(em>12){ey++;em-=12}
    const afterEnd=(ty>ey)||(ty===ey&&tm>=em);
    if(!afterEnd)break;y=ey;m=em}
  return {y,m}};
const monLabel=(yy,mm,showYear)=>MN[mm-1]+(showYear?" '"+String(yy).slice(2):'');
const months=f=>{
  const ps=(f.rent_payments||[]).slice().sort((a,b)=>a.date<b.date?-1:1);
  const w=leaseWindow(f);
  let y,m,count=12;
  if(w){y=w.y;m=w.m}else{
    const last=ps.length?ps[ps.length-1].month:new Date().toISOString().slice(0,7);
    [y,m]=last.split('-').map(Number); // legacy fallback: last 12 ending at latest payment
    for(let i=0;i<11;i++){m--;if(m<1){m=12;y--}}
  }
  const today=new Date();const curKey=today.getFullYear()+'-'+String(today.getMonth()+1).padStart(2,'0');
  const out=[];let yy=y,mm=m;const startY=y;
  for(let i=0;i<count;i++){
    const key=yy+'-'+String(mm).padStart(2,'0');
    const p=ps.filter(x=>x.month===key);
    const amt=p.length&&p.every(x=>payAmt(x,f)!=null)?p.reduce((t,x)=>t+payAmt(x,f),0):null;
    const est=f.expenses.some(x=>x.est||x.amount==null)||p.some(x=>x.est);
    const upcoming=key>curKey;
    const showYear=(i===0)||(mm===1)||(yy!==startY&&mm===m);
    out.push({m:monLabel(yy,mm,true),short:monLabel(yy,mm,i===0||mm===1),key,rent:amt,exp:f.known_total,est,upcoming,date:p.length?p[p.length-1].date:null});
    mm++;if(mm>12){mm=1;yy++}
  }
  return out};
const gap=x=>{const n=x.rent-x.exp;return n>=0?'Paid For · +'+usd(+n.toFixed(2))+' ('+Math.round(n/x.exp*100)+'%)':'Short '+usd(+(-n).toFixed(2))+' ('+Math.round(-n/x.exp*100)+'%)'};
const noDet='<p class="muted">No details yet</p>';
const short=l=>l.replace(/\s*\(.*\)\s*/,'').trim();
const ymd=d=>d?new Date(d+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}):'';
const daysLeft=d=>{if(!d)return null;const t=new Date(d+'T12:00:00'),n=new Date();n.setHours(12,0,0,0);return Math.round((t-n)/86400000)};
const ST={ok:['OK','ok','✓'],missing:['Missing','bad','!'],needs_check:['Needs Check','warn','!'],unknown:['Not Tracked','na','–'],na:['N/A','na','–']};
const mark=(k,extra='')=>{const s=ST[k]||ST.unknown;return `<span class="st-mark ${s[1]}" title="${s[0]}">${s[2]}</span>`};

const statusRow=f=>{
  const s=f.status||{},items=[
    ['rent_on_time','Rent On Time','#stmt'],
    ['renters_insurance','Renters Insurance','#docs-card'],
    ['mortgage_paid','Mortgage Paid','#bills-card'],
    ['landlord_insurance','Landlord Insurance','#docs-card'],
    ['lease_current','Lease Current','#dates-card']
  ];
  const covered=/rent on time|renters insurance|mortgage|landlord (policy|insurance)|lease (ends|current|end)/i;
  const extra=(f.attention||[]).filter(a=>a.status!=='ok'&&!covered.test(a.item));
  return `<section class="pcard status-card" aria-label="Status Check"><header class="pcard-h"><h3>Status Check</h3><span class="muted">This month</span></header>
  <div class="status-row">`+items.map(([k,label,href])=>{const x=s[k]||{status:'unknown'};const st=ST[x.status]||ST.unknown;
    return `<a class="status-item ${st[1]} mw-hover" href="${href}" data-jump="${href.slice(1)}"><span class="st-mark ${st[1]}">${st[2]}</span><span class="st-body"><b>${label}</b><small>${esc(x.note||st[0])}${x.date?' · '+ymd(x.date):''}</small></span></a>`}).join('')+
  `</div>`+(extra.length?`<div class="status-extra">`+extra.map(a=>{const st=ST[a.status]||ST.needs_check;return `<span class="status-chip ${st[1]}"><span class="st-mark ${st[1]}">${st[2]}</span><b>${esc(a.item)}</b>${a.note?`<small>${esc(a.note)}</small>`:''}</span>`}).join('')+`</div>`:'')+`</section>`};

const tiles=(f,M)=>{
  const rec=M.filter(x=>x.rent!=null).pop(),ps=(f.rent_payments||[]).slice().sort((a,b)=>a.date<b.date?-1:1),lp=ps[ps.length-1];
  const late=lp?+lp.date.slice(8)>5:null;
  const cell=(lab,val,cls,sub)=>`<div class="ktile"><span class="kt-lab">${lab}</span><b class="kt-val ${cls||''}">${val}</b>${sub?`<small class="kt-sub">${sub}</small>`:''}</div>`;
  return `<section class="pcard tiles-card" aria-label="Key Figures"><header class="pcard-h"><h3>Key Figures</h3></header>
  <div class="ktiles">
   ${cell('Rent / Mo',usd(f.rent),'','Lease')}
   ${cell('Cash Flow · '+(rec?rec.m.slice(0,3):'—'),rec?usd(+(rec.rent-rec.exp).toFixed(2))+star(rec.est):'No data',rec&&rec.rent<rec.exp?'neg':'pos',rec?'Most recent month':'')}
   ${cell('Rent Status',lp?(late?'Late':'On Time')+star(lp.est):'No data',late?'neg':'pos',lp?'Received '+fmt(lp.date):'')}
   ${cell('Projected Annual',usd(+(f.cash_flow*12).toFixed(2))+star(f.cash_flow_est),'pos','Cash flow × 12')}
  </div></section>`};

const cf12=f=>{const M=months(f),mx=Math.max(1.1,...M.filter(x=>x.rent!=null).map(x=>x.rent/x.exp));
 const prorate=f.lease_prorate?`<p class="cf-note muted">${esc(f.lease_prorate.label)}: ${esc(f.lease_prorate.detail)}${f.lease_prorate.amount!=null?' · '+usd(f.lease_prorate.amount):''} — shown as a note, not a tracker month.</p>`:'';
 const assume=f.lease_start_note?`<p class="cf-note muted">${esc(f.lease_start_note)}</p>`:'';
 const win=M.length?`${M[0].m} – ${M[M.length-1].m}`:'';
 return `<section class="pcard cf-card" aria-label="12-Month Cash Flow"><header class="pcard-h"><h3>12-Month Cash Flow</h3><span class="muted">${win} · rent vs known expenses${star(1)}</span></header>
 <div id="cf12" data-cf12-slot="temporary" data-cf12-source="upkeep ccm-cov-strip pattern" data-lease-start="${esc(f.lease_start||'')}"><div class="cf-strip">`+M.map(x=>{
  if(x.upcoming&&x.rent==null)return `<span class="up" title="${x.m}: upcoming"><div class="bx"><i></i><u style="bottom:${100/mx}%"></u></div><em>${esc(x.short)}</em></span>`;
  if(x.rent==null)return `<span class="nd" title="${x.m}: no data"><div class="bx"><i></i><u style="bottom:${100/mx}%"></u></div><em>${esc(x.short)}</em></span>`;
  const ok=x.rent>=x.exp;return `<span class="${ok?'ok':'bad'}" title="${x.m}: ${gap(x)}${x.est?' (estimated)':''}"><div class="bx"><i style="height:${Math.max(6,x.rent/x.exp/mx*100)}%"></i><u style="bottom:${100/mx}%"></u></div><em>${esc(x.short)}${x.est?'<sup class="star">*</sup>':''}</em></span>`}).join('')+
  `</div>${prorate}${assume}<small class="muted">Hatched = no data. Light = upcoming. Dashed line = break-even.</small></div></section>`};

const detBody=x=>{
  const bits=[];
  if(x.amount!=null)bits.push('Amount: '+usd(x.amount)+(x.est?' (estimated)':''));
  if(x.source)bits.push('Source: '+x.source+(x.as_of?' · '+fmt(x.as_of):''));
  if(x.note)bits.push(x.note);
  if(x.payment_status)bits.push('Payment: '+(x.payment_status==='unknown'?'Unpaid / Unknown':x.payment_status));
  if(x.landlord_cost)bits.push('Landlord cost — not billable to tenant');
  const inv=(x.invoices||[]).map(i=>`<li><b>#${esc(i.number)}</b> · ${ymd(i.date)} · ${usd(i.amount)}${i.due?' · due '+(i.due==='on receipt'?'on receipt':ymd(i.due)):''}<br><span class="muted">${esc(i.detail||'')} · ${esc(i.status==='unknown'?'Unpaid / Unknown':i.status||'')}</span></li>`).join('');
  const ent=(x.entries||[]).map(e=>`<li>${e.date?fmt(e.date)+' · ':''}${esc(e.label||'')}${e.amount!=null?' · '+usd(e.amount):''}</li>`).join('');
  if(!bits.length&&!inv&&!ent)return noDet;
  return bits.map(b=>`<p>${esc(b)}</p>`).join('')+(inv?`<ul class="plain">${inv}</ul>`:'')+(ent?`<ul class="plain">${ent}</ul>`:'')};

const statement=(f)=>{
  const anyEst=f.expenses.some(x=>x.est||x.amount==null);
  const ps=(f.rent_payments||[]).slice().sort((a,b)=>a.date<b.date?-1:1);
  const payList=ps.length?'<ul class="plain">'+ps.map(p=>`<li>${fmt(p.date)} · ${payAmt(p,f)!=null?usd(payAmt(p,f)):esc(p.detail||'Amount not recorded')}${star(p.est)}</li>`).join('')+'</ul>':noDet;
  const row=(lab,mo,an,est,det,cls='')=>`<tr class="stmt-row ${cls}" tabindex="0" data-det="${esc(JSON.stringify({t:lab,h:det}))}"><td class="stmt-lab">${esc(lab)}</td><td class="stmt-num">${mo}${star(est)}</td><td class="stmt-num">${an}${star(est||true)}</td></tr>`;
  const expRows=f.expenses.map(x=>{
    const mo=x.amount!=null?usd(x.amount):'—';
    const an=x.amount!=null?usd(+(x.amount*12).toFixed(2)):(x.invoices||[]).length?usd((x.invoices||[]).reduce((t,i)=>t+i.amount,0))+' <span class="muted">inv</span>':'—';
    return row(short(x.label),mo,an,x.est||x.amount==null,detBody(x));
  }).join('');
  return `<section class="pcard stmt-card" id="stmt" aria-label="Financial Statement"><header class="pcard-h"><h3>Financial Statement</h3><span class="muted">Click a line for details</span></header>
  <div class="stmt-wrap"><table class="stmt"><thead><tr><th>Line</th><th class="stmt-num">Monthly</th><th class="stmt-num">Annual</th></tr></thead>
  <tbody>
   <tr class="stmt-sec"><td colspan="3">Income</td></tr>
   ${row('Rent',usd(f.rent),usd(f.rent*12),false,payList)}
   <tr class="stmt-sec"><td colspan="3">Expenses</td></tr>
   ${expRows}
   <tr class="stmt-tot"><td>Known Expenses</td><td class="stmt-num">${usd(f.known_total)}${star(anyEst)}</td><td class="stmt-num">${usd(+(f.known_total*12).toFixed(2))}${star(1)}</td></tr>
   <tr class="stmt-tot net"><td>Net Cash Flow</td><td class="stmt-num">${usd(f.cash_flow)}${star(f.cash_flow_est)}</td><td class="stmt-num">${usd(+(f.cash_flow*12).toFixed(2))}${star(1)}</td></tr>
  </tbody></table></div>
  ${(f.extra||[]).map(x=>`<p class="fp"><b>${esc(x.label)}:</b> ${esc(x.value)} <span class="pill">${esc(x.note)}</span></p>`).join('')}
  ${(f.notes||[]).map(n=>`<p class="fp muted">${esc(n)}</p>`).join('')}
  <p class="legend">* Estimated, computed from estimated data, or waiting for records. Lawn invoices sit under Expenses but are not in Known Expenses until a monthly rate is set.</p>
  <aside class="stmt-pop" id="stmt-pop" hidden><button type="button" class="stmt-pop-x" aria-label="Close">×</button><h4 id="stmt-pop-t"></h4><div id="stmt-pop-b"></div></aside>
  </section>`};

const billsCard=f=>{
  const bs=f.bills||[];
  return `<section class="pcard" id="bills-card" aria-label="Bills Paid This Month"><header class="pcard-h"><h3>Bills Paid This Month</h3></header>
  ${bs.length?`<ul class="check-list">`+bs.map(b=>{const st=ST[b.status]||ST.unknown;return `<li>${mark(b.status)}<span><b>${esc(b.label)}</b>${b.amount!=null?' · '+usd(b.amount):''}${b.due?' · due '+ymd(b.due):''}<small>${esc(b.note||st[0])}</small></span></li>`}).join('')+`</ul>`:`<p class="muted">No bills tracked</p>`}
  </section>`};

const owedCard=f=>{
  const o=f.owed||[];
  return `<section class="pcard" id="owed-card" aria-label="Owed To Me"><header class="pcard-h"><h3>Owed To Me</h3></header>
  ${o.length?`<ul class="check-list">`+o.map(x=>`<li><span class="att-s warn">${esc(x.status)}</span><span><b>${esc(x.label)}</b>${x.amount!=null?' · '+usd(x.amount):''}<small>${esc(x.note||'')}</small></span></li>`).join('')+`</ul>`:`<p class="muted">Nothing owed right now</p>`}
  </section>`};

const datesCard=f=>{
  const ds=f.key_dates||[];
  return `<section class="pcard" id="dates-card" aria-label="Key Dates"><header class="pcard-h"><h3>Key Dates</h3></header>
  ${ds.length?`<ul class="check-list">`+ds.map(d=>{const left=daysLeft(d.date);const c=left==null?'':left<0?`${-left}d past`:left===0?'Today':`${left}d`;
    return `<li><span class="att-s ${d.status==='missing'?'bad':d.status==='unknown'||d.status==='needs_check'?'warn':left!=null&&left<60?'warn':'ok'}">${c||(ST[d.status]||ST.unknown)[0]}</span><span><b>${esc(d.label)}</b>${d.date?' · '+ymd(d.date):''}<small>${esc(d.note||'')}</small></span></li>`}).join('')+`</ul>`:`<p class="muted">No key dates</p>`}
  </section>`};

const DST={on_file:['On File','ok'],missing:['Missing','bad'],needs_check:['Needs Check','warn'],na:['N/A','na']};
const docsSec=(id,f)=>{const ds=f.docs||[];let gone=[];try{gone=JSON.parse(localStorage.getItem('propDocHide')||'[]')}catch(e){}
 const rows=ds.map(d=>({d,k:id+':'+d.slot+':'+d.title})).filter(r=>!gone.includes(r.k));
 const nOn=ds.filter(d=>d.status==='on_file').length,nMis=ds.filter(d=>d.status==='missing').length;
 const fo=`<details class="fold pdocs-fold"><summary><span class="lt">Documents · ${nOn} on file · ${nMis} missing</span></summary>`;
 if(!rows.length)return fo+'<p class="muted">No documents yet</p></details>';
 return fo+'<ul class="op-list pdocs">'+rows.map(({d,k})=>{const s=DST[d.status]||DST.needs_check;
  const t=d.link?`<a href="${esc(d.link)}" target="_blank" rel="noopener noreferrer">${esc(d.title)}</a>`:d.file?`<a href="#" data-enc-file="${esc(d.file)}">${esc(d.title)}</a>`:`<span>${esc(d.title)}</span>`;
  return `<li><span class="att-s ${s[1]}">${s[0]}</span><div class="op-lt"><small>${esc(d.slot)}</small>${t}${d.note?`<small>${esc(d.note)}</small>`:''}</div><button type="button" class="tdx mw-hover pdx" data-k="${esc(k)}" aria-label="Remove ${esc(d.title)}">×</button></li>`}).join('')+'</ul></details>'};
const docsCard=(id,f)=>`<section class="pcard" id="docs-card" aria-label="Documents"><header class="pcard-h"><h3>Documents</h3></header>${docsSec(id,f)}</section>`;

const breakdown=(f,id)=>{if(!f)return '<p class="muted">Waiting for records</p>';
 const M=months(f);
 return `<div class="pview">${statusRow(f)}${tiles(f,M)}${cf12(f)}${statement(f)}
 <div class="pgrid">${billsCard(f)}${owedCard(f)}${datesCard(f)}${docsCard(id||'',f)}</div>
 </div>`};

/* Statement popover + jump links + doc hide */
document.addEventListener('click',e=>{
  const jump=e.target.closest('[data-jump]');
  if(jump){e.preventDefault();const el=document.getElementById(jump.dataset.jump);if(el)el.scrollIntoView({behavior:'smooth',block:'start'});return}
  const row=e.target.closest('.stmt-row[data-det]');
  if(row){const pop=document.getElementById('stmt-pop');if(!pop)return;const d=JSON.parse(row.getAttribute('data-det'));
    document.getElementById('stmt-pop-t').textContent=d.t;document.getElementById('stmt-pop-b').innerHTML=d.h;pop.hidden=false;
    const card=row.closest('.stmt-card');if(card&&window.innerWidth>480){const rr=row.getBoundingClientRect(),cr=card.getBoundingClientRect();
      let top=rr.bottom-cr.top+8;const max=Math.max(24,card.clientHeight-pop.offsetHeight-16);if(top>max)top=Math.max(24,rr.top-cr.top-pop.offsetHeight-8);pop.style.top=top+'px'}
    else pop.style.top='';return}
  if(e.target.closest('.stmt-pop-x')||e.target.id==='stmt-pop'&&e.target.classList.contains('stmt-pop')){const pop=document.getElementById('stmt-pop');if(pop)pop.hidden=true;return}
  const o=e.target.closest('.pdx');if(!o)return;
  let g=[];try{g=JSON.parse(localStorage.getItem('propDocHide')||'[]')}catch(_){}g.push(o.dataset.k);try{localStorage.setItem('propDocHide',JSON.stringify(g))}catch(_){}o.closest('li').remove()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){const pop=document.getElementById('stmt-pop');if(pop)pop.hidden=true}
  if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('stmt-row')){e.preventDefault();e.target.click()}});

/* Standing-rule UI: every to-do list gets delete-one + delete-all (remembered). */
(function(){const K='propTodoDone';document.querySelectorAll('ul.todo').forEach(ul=>{
  if(ul.dataset.tdWired)return;ul.dataset.tdWired='1';
  let gone;try{gone=JSON.parse(localStorage.getItem(K)||'[]')}catch(e){gone=[]}
  const save=()=>{try{localStorage.setItem(K,JSON.stringify(gone))}catch(e){}};
  const key=li=>{const s=li.querySelector('span');return (s&&s.textContent)||li.textContent};
  const empty=()=>{if(!ul.querySelector('li')){const p=document.createElement('p');p.className='muted';p.id=ul.id||'todo-empty';p.textContent='All clear.';ul.replaceWith(p)}};
  [...ul.children].forEach(li=>{if(li.tagName!=='LI')return;if(gone.includes(key(li))){li.remove();return}
    if(li.querySelector('.tdx'))return;
    const x=document.createElement('button');x.type='button';x.className='tdx mw-hover';x.setAttribute('aria-label','Delete item');x.textContent='×';
    x.onclick=()=>{gone.push(key(li));save();li.remove();empty()};li.appendChild(x)});
  if(!ul.isConnected)return;
  if(ul.parentNode.querySelector('.tdclear'))return;
  const c=document.createElement('button');c.type='button';c.className='mw-btn mw-hover tdclear';c.textContent='Delete all';
  c.onclick=()=>{if(!confirm('Delete all to-do items?'))return;ul.querySelectorAll('li').forEach(li=>gone.push(key(li)));save();ul.innerHTML='';empty();c.remove()};
  empty();if(ul.isConnected)ul.after(c)})})();

/* Standing-rule UI: legacy Documents Status lists get a small X (remembered). */
(function(){const K='propLegacyDocHide';document.querySelectorAll('#docs-sec ul.docs li').forEach(li=>{
  if(li.querySelector('.tdx'))return;
  const title=(li.querySelector('span:last-child')||li).textContent.trim();
  let gone;try{gone=JSON.parse(localStorage.getItem(K)||'[]')}catch(e){gone=[]}
  if(gone.includes(title)){li.remove();return}
  const x=document.createElement('button');x.type='button';x.className='tdx mw-hover';x.setAttribute('aria-label','Remove '+title);x.textContent='×';
  x.onclick=()=>{let g;try{g=JSON.parse(localStorage.getItem(K)||'[]')}catch(_){g=[]}g.push(title);try{localStorage.setItem(K,JSON.stringify(g))}catch(_){}li.remove()};
  li.appendChild(x)})})();

/* Standing-rule UI: links to other dashboards open in a new tab (after kit layout). */
(function(){const apply=()=>{document.querySelectorAll('a[href]').forEach(a=>{
  const href=a.getAttribute('href')||'';if(!/^https?:/i.test(href))return;
  let u;try{u=new URL(href,location.href)}catch(e){return}
  if(u.origin!==location.origin){if(u.hostname.endsWith('github.io')||u.hostname.endsWith('webermanapps.com')||u.hostname==='smartupkeep.ai'){a.target='_blank';a.rel='noopener noreferrer'}}
  else if(!u.pathname.replace(/\/+$/,'').startsWith((location.pathname.replace(/\/[^/]*$/,'')||''))){ /* other repo pages on same host */
    if(/webermanapps\\.github\\.io/.test(u.host)&&!u.pathname.startsWith('/prop-dashboard')){a.target='_blank';a.rel='noopener noreferrer'}}
  if(a.classList.contains('mw-apps-home')||a.classList.contains('mw-stick-home')){a.target='_blank';a.rel='noopener noreferrer'}
})};
document.addEventListener('mw-layout',apply);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(apply,50));else setTimeout(apply,50);setTimeout(apply,800)})();
