"""Builds index.html + property pages with finance.json/report.json EMBEDDED (those files are local-only, gitignored).
Run: python3 tools/build.py, then relock per page-lock-rule.md."""
import re,json
import os
D=os.path.dirname(os.path.abspath(__file__))+'/..'
style=open(D+'/tools/style.css').read()
FIN=json.load(open(D+'/finance.json'));REP=json.load(open(D+'/report.json'))
DATA='const FIN='+json.dumps(FIN)+';const REP='+json.dumps(REP)+';'
HEAD_LINKS='''<link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/dash-theme.css?v=cc7"><link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/mw-layout.css?v=ly8"><script src="https://webermanapps.github.io/style-swipe/kit/mw-layout.js?v=ly8" defer></script>'''
OVR='''
/* R80 (Max Oct 16 12:44): Apps Home colors, white with light beige accents, light only */
:root{--beige:#FAF6EE;--beige2:#F1E9DA;--ink:#171717;--lagoon:#8a6d3b;--bd:#E5E0D8;--r:.75rem;--mut:#525252}
html{color-scheme:light}body{background:#fff}
.topnav{background:var(--beige);color:var(--ink);box-shadow:0 1px 0 var(--bd)}.topnav .homelink,.navtitle{color:var(--ink)}.upd{color:var(--mut)}
.topnav .shareico{border-color:var(--ink);color:var(--ink)}
.drop,.drop.report{background:#fff;border-color:var(--bd);border-left-color:var(--beige2)}.drop.report{border-left:4px solid #d9c7a3}
.cnt,ol.num li::before{background:var(--beige2)}
.mw-section h2{font-size:1.5rem;margin:0 0 10px}
ul.todo{list-style:none;margin:0;padding:0;border:1px solid var(--bd);border-radius:.6rem;overflow:hidden}
ul.todo li{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border-top:1px solid var(--bd);font-weight:500}ul.todo li:first-child{border-top:0}
ul.todo li i{flex:none;width:18px;height:18px;border:1.5px solid var(--ink);border-radius:4px;margin-top:3px}
ul.todo .tg{flex:none;margin-left:auto;font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--beige);border:1px solid var(--beige2);border-radius:999px;padding:1px 9px;white-space:nowrap}
ul.todo .tg.due{background:#fbf1d6;border-color:#D4A017;color:#7a5a00}
.car{position:relative}.ptrack{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;scrollbar-width:none;-webkit-overflow-scrolling:touch;padding:2px}.ptrack::-webkit-scrollbar{display:none}
.pc{flex:0 0 100%;scroll-snap-align:center;border:1px solid var(--bd);border-radius:var(--r);background:#fff;text-decoration:none;color:inherit;overflow:hidden;display:block}
@media(min-width:720px){.pc{flex-basis:calc(50% - 7px)}}
.pv{background:var(--beige);border-bottom:1px solid var(--bd);padding:14px}
.pv .bign{margin:0}.pv .bign div{background:#fff}
.pt{padding:12px 14px;display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center}.pt b{font-family:Khand,sans-serif;font-size:22px}.pt small{flex-basis:100%;color:var(--mut)}.pt .open{margin-left:auto;font-weight:600;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase}
.pc .pill.st{background:var(--beige);color:var(--ink);border:1px solid var(--beige2)}
.pcnav{position:absolute;top:104px;z-index:2;width:44px;height:44px;border-radius:50%;border:1px solid var(--bd);background:#fff;font-size:26px;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.1)}.prev{left:6px}.next{right:6px}
.pdots{display:flex;justify-content:center;gap:4px;margin-top:6px}.pdots button{width:44px;height:44px;border:0;background:none;cursor:pointer;position:relative}.pdots button:after{content:"";position:absolute;inset:17px;border-radius:50%;background:#d4d4d4}.pdots button.on:after{background:#171717}
@media(min-width:720px){.pcnav,.pdots{display:none}}
.bign b.pos{color:#0B6E4F}.star{color:#8a5a2b}
.docs{list-style:none;margin:0;padding:0}.docs li{display:flex;gap:10px;padding:7px 0;border-top:1px solid var(--bd)}.docs li:first-child{border-top:0}.docs li span:first-child{flex:none;white-space:nowrap;min-width:64px}.docs .ok{color:#0B6E4F;font-weight:700}.docs .no{color:#9a3412;font-weight:700}
'''
def head(title):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><meta name="color-scheme" content="light only"><meta name="theme-color" content="#FAF6EE"><title>{title}</title>
<link rel="icon" href="favicon-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Khand:wght@600;700&family=Hind:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="brand-tokens.css">
<link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/deck-shelf.css?v=5">
<link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/routines-section.css?v=5">
<style>{style}</style>{HEAD_LINKS}</head><body><main>'''
NAV=lambda name,extra='':f'''<nav class="topnav">{extra}<span class="navtitle">{name}</span><span class="upd" id="upd"></span><button class="shareico mw-hover" id="share" aria-label="Share" title="Share"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M12 3v12M7 8l5-5 5 5M5 13v8h14v-8"/></svg></button></nav>'''
LOGO='<div class="mw-cc-logo" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="#2B2B2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="16" cy="24" r="2.5" fill="#8a6d3b" stroke="none"/><circle cx="16" cy="24" r="7"/><circle cx="16" cy="24" r="2.5"/><path d="M23 24 H40 M34 24 v5 M39 24 v4"/></svg></div>'
def CCH(t,d): return f'<div class="mw-cc-header">{LOGO}<div class="mw-cc-text"><h1 class="mw-cc-title">{t}</h1><p class="mw-cc-desc">{d}</p></div></div>'
FOOT_BAR='<div class="mw-footer-bar"><button class="mw-btn mw-hover sharebtn" id="share2" type="button">Share</button><a class="mw-hover" href="https://maxweberman.com"><span class="mw-machan" style="display:inline-flex;align-items:center;gap:6px;vertical-align:middle;white-space:nowrap"><svg class="mw-machan-mark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false" style="display:block;flex:none;width:22px;height:22px"><path d="M12 5.2C11.2 3 9.4 2 7.6 2.3c.3 1.9 1.9 3.2 4.4 2.9z" fill="#3F7D58"/><path d="M12 5.2c.8-2.2 2.6-3.2 4.4-2.9-.3 1.9-1.9 3.2-4.4 2.9z" fill="#5E9A6E"/><rect x="3.5" y="5.5" width="17" height="16" rx="7" fill="#C8643F"/><rect x="5.5" y="9" width="13" height="10" rx="5" fill="#FAF6EE"/><circle cx="9.6" cy="13.3" r="1.35" fill="#2E6F86"/><circle cx="14.4" cy="13.3" r="1.35" fill="#2E6F86"/><path d="M10.6 16.1q1.4 1.1 2.8 0" fill="none" stroke="#C8643F" stroke-width="1.1" stroke-linecap="round"/><circle cx="7.6" cy="15.6" r=".9" fill="#E9B9A3"/><circle cx="16.4" cy="15.6" r=".9" fill="#E9B9A3"/></svg>Built by Machan</span></a></div>'
SHARE='''const doShare=async()=>{const url=location.href.split('#')[0],text=document.title;
 if(navigator.share){try{await navigator.share({title:text,text,url});return}catch(e){if(e.name==='AbortError')return}}
 if(/iPhone|iPad|Android/i.test(navigator.userAgent)){location.href='sms:?&body='+encodeURIComponent(text+' '+url);return}
 const b=document.getElementById('share');try{await navigator.clipboard.writeText(url);b.title='Copied'}catch(e){prompt('Copy link',url)}setTimeout(()=>b.title='Share',1800)};document.getElementById('share').onclick=doShare;document.getElementById('share2').onclick=doShare;
const BUILT="2026-10-16T13:00:00+07:00";const setUpd=iso=>{const d=new Date(iso);document.getElementById('upd').textContent='Updated '+d.toLocaleDateString('en-US',{month:'short',day:'numeric',timeZone:'Asia/Bangkok'})+' · '+d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',timeZone:'Asia/Bangkok'})+' ICT'};setUpd(BUILT);
const fmt=d=>new Date(d+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric'});
const usd=v=>v==null?'Waiting':'$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:v%1?2:0,maximumFractionDigits:2});
const star=e=>e?'<sup class="star" title="Estimated or waiting for records">*</sup>':'';
const big=f=>`<div class="bign"><div><span>Rent / Mo</span><b>${usd(f.rent)}</b></div><div><span>Cash Flow / Mo</span><b class="pos">${usd(f.cash_flow)}${star(f.cash_flow_est)}</b></div><div><span>Last Rent</span><b>${fmt(f.last_rent.date)}${star(f.last_rent.est)}</b></div></div>`;'''
CHAT='<script src="ptr.js" defer></script>\n<script src="https://webermanapps.github.io/style-swipe/kit/mw-chat.js?v=cc12" data-agent-id="f466837e-6ecd-4c83-9ac9-5f031aa92add" data-agent-name="Prop Agent" defer></script>\n</body></html>\n'

PROPS=[
 dict(id="mellow-wood",name="Mellow Wood",addr="6631 Mellow Wood Ln",status="Rented",line="Rented from Oct 1 on a one-year lease; paperwork and utilities left to close out.",
  todo=["Send the Steadily request to add the lender (confirm the lender address first)","Move the utilities out of your name and cancel the internet","Pick the walkthrough date","Township rental certificate follow-up","Re-send the Steadily DP-3 declarations page","Confirm the old Homesite policy is cancelled","Re-send the Staelens and Arian invoices","Confirm the lockbox and key pickup date"],
  docs=[(1,"Executed lease (Dropbox)"),(1,"Renters insurance certificate (Dropbox)"),(1,"Deposit and Sep/Oct rent receipts (Dropbox)"),(1,"Move-in checklist and photos (Dropbox)"),(0,"Steadily DP-3 declarations page"),(0,"Township rental certificate"),(0,"HOA name, contact and dues statement"),(0,"Utility transfer details")]),
 dict(id="wickfield",name="Wickfield",addr="2573 Wickfield Rd",status="Rented",line="Rented. Receipts, homestead removal, mail forwarding and lease extension open.",
  todo=[("USPS forwarding ID check","2026-10-30"),"Send the 2026 receipts email","Homestead Form 2602: move-out date and signature","Upload the signed lease extension (end date unconfirmed)","Re-send the renters insurance certificate","Re-send the HOA contact and dues statement","Soffit repair: Prop or Weberman Construction?","Jun–Aug: which months the summer deposits covered"],
  docs=[(1,"2024 lease (unsigned copy)"),(1,"Tax bills, 1098s and rental summaries (Dropbox)"),(0,"Signed 2024 lease"),(0,"Signed lease extension"),(0,"Renters insurance certificate"),(0,"HOA contact and dues statement"),(0,"2026 receipts packet"),(0,"Key and garage-code inventory")]),
]
def todo_li(t,tag):
    if isinstance(t,tuple): return f'<li><i></i><span>{t[0]}</span><span class="tg due" data-due="{t[1]}">Due {t[1][5:7].lstrip("0")}/{t[1][8:]}</span></li>'
    return f'<li><i></i><span>{t}</span><span class="tg">{tag}</span></li>'
# main To-Do: short
TOP=[("Wickfield",("USPS forwarding ID check","2026-10-30")),("Mellow Wood","Send the Steadily lender request (confirm the lender address)"),("Mellow Wood","Move the utilities out of your name"),("Wickfield","Send the 2026 receipts email"),("Wickfield","Homestead Form 2602: move-out date and signature"),("Both","Re-send the missing documents (lease extension, insurance pages, HOA contacts, invoices)"),("Address","Confirm the new mailing address")]
todo_html='<ul class="todo">'+''.join(todo_li(t,g) for g,t in TOP)+'</ul>'
cards=''.join(f'<a class="pc mw-hover" href="{p["id"]}.html" aria-label="Open {p["name"]}"><div class="pv" id="fin-{p["id"]}"><p class="muted">Loading numbers</p></div><div class="pt"><b>{p["name"]}</b><span class="pill st">{p["status"]}</span><span class="open">Open →</span><small>{p["addr"]} · {p["line"]}</small></div></a>' for p in PROPS)
ROUT='''<footer class="mw-footer" id="routines-sec">
<div class="week-wrap" id="routines-block"><section data-routines="routines.json" id="routines"></section></div>
<script src="https://webermanapps.github.io/style-swipe/kit/routines-section.js?v=5" defer></script>
'''+FOOT_BAR+'</footer>'
idx=head("Prop Command Center")+NAV("Prop")+CCH("Prop Command Center","Rental properties: tenants, finances and upkeep for each property")+f'''
<div class="mw-sections">
<section class="mw-section mw-section--plain" id="decks-sec"><section data-shelf="shelf.json" id="ready-shelf"></section>
<script src="https://webermanapps.github.io/style-swipe/submit.js?v=9921428" defer></script>
<script src="https://webermanapps.github.io/style-swipe/kit/deck-shelf.js?v=5" defer></script>
<details data-mw-slot="morning" class="drop report" id="report" hidden><summary><span class="sumtxt"><b id="rtype">Report</b><span class="muted" id="rsum"></span></span><span class="chev" aria-hidden="true"></span></summary>
<div class="rep" id="rep"><div id="rbody"></div></div></details>
</section>
<section class="mw-section mw-todo" id="todo-sec" data-mw-slot="todo" aria-label="To-Do List"><h2>To-Do List</h2>{todo_html}</section>
<section class="mw-section projects" id="props-sec" aria-label="Properties"><h2>Properties</h2>
<div class="car"><button class="pcnav prev" type="button" aria-label="Previous property">&#8249;</button><div class="ptrack" id="ptrack">{cards}</div><button class="pcnav next" type="button" aria-label="Next property">&#8250;</button></div>
<div class="pdots"><button type="button" aria-label="Property 1"></button><button type="button" aria-label="Property 2"></button></div>
<p class="legend">* Estimated or waiting for records</p></section>
</div>
{ROUT}
</main>
<script>
{DATA}
{SHARE}
Promise.resolve(FIN).then(F=>{{for(const id of ['mellow-wood','wickfield']){{const f=F.properties[id],el=document.getElementById('fin-'+id);if(f&&el)el.innerHTML=big(f)}}}}).catch(()=>{{}});
(function(){{const t=document.getElementById("ptrack"),c=[...t.children],d=[...document.querySelectorAll(".projects .pdots button")];const go=i=>{{i=(i+c.length)%c.length;t.scrollTo({{left:c[i].offsetLeft-t.offsetLeft,behavior:"smooth"}})}};const cur=()=>Math.round(t.scrollLeft/(c[0].offsetWidth+14));const upd=()=>d.forEach((b,i)=>b.classList.toggle("on",i==cur()));t.addEventListener("scroll",upd,{{passive:true}});upd();d.forEach((b,i)=>b.onclick=()=>go(i));document.querySelector(".projects .prev").onclick=()=>go(cur()-1);document.querySelector(".projects .next").onclick=()=>go(cur()+1)}})();
const rows=a=>'<ul class="plain">'+a.map(x=>'<li>'+x+'</li>').join('')+'</ul>';
Promise.resolve(REP).then(r=>{{
 if(r.updated&&new Date(r.updated)>new Date(BUILT))setUpd(r.updated);let h='';
 if(r.text)h+=`<p>${{r.text}}</p>`;if(r.items)h+=rows(r.items);if(r.groups)h+=r.groups.map(g=>`<details class="fold"><summary>${{g.title}} <span class="cnt">${{g.items.length}}</span></summary>${{rows(g.items)}}</details>`).join('');
 if(h){{document.getElementById('rtype').textContent='Morning Report'+(r.date?' · '+fmt(r.date):'');document.getElementById('rsum').textContent=r.summary||'';document.getElementById('rbody').innerHTML=h;document.getElementById('report').hidden=false}}}}).catch(()=>{{}});
</script>
'''+CHAT

# ---- Kit sync (Oct 17): later kit rollouts edited the pages directly; mirror them here so a rebuild never regresses them.
VIEWER=open('/workspace/security/pagelock/enc_file_viewer.js').read()  # Security's viewer, inlined verbatim (never copied into the repo)
def kit_sync(h,page):
    h=h.replace('deck-shelf.css?v=5','deck-shelf.css?v=ly12').replace('deck-shelf.js?v=5','deck-shelf.js?v=ly12')
    h=h.replace('mw-layout.css?v=ly8','mw-layout.css?v=ly14').replace('mw-layout.js?v=ly8','mw-layout.js?v=ly14')  # kit ly14: R106 header + loads kit/mw-back.js
    if page!='index': return h
    # routines-section.css/.js already ?v=5 in head()/ROUT (property pages skip this block)
    h=h.replace('\nfooter.mw-footer{text-align:left;padding-bottom:16px}.week-wrap{margin-top:0}','.week-wrap{margin-top:0}').replace('.mw-footer-bar a{min-height:44px;padding:0}.week-wrap h2','.week-wrap h2',1)
    h=h.replace('mw-layout.js?v=ly14" defer></script></head><body>','mw-layout.js?v=ly14" defer></script><link rel="stylesheet" href="https://webermanapps.github.io/style-swipe/kit/projects.css?v=op8">\n</head><body><section id="mw-projects" data-mw-projects="projects.json" aria-label="Document Center"><p class="op-empty">Loading documents</p></section>\n')
    h=h.replace('</body></html>\n','<!-- R100 Document Center: kit projects.js/.css pinned ?v=op8 (Security condition 8) + Security enc_file_viewer.js (inlined verbatim, per ops/team-sync/handoffs/encrypted-files.md) -->\n<script id="mw-enc-viewer">\n'+VIEWER+'\n</script>\n<script src="https://webermanapps.github.io/style-swipe/kit/projects.js?v=op10" defer></script>\n</body></html>\n')
    return h
open(D+'/index.html','w').write(kit_sync(idx,'index'))
for p in PROPS:
    tl='<ul class="todo">'+''.join(todo_li(t,'Open') for t in p['todo'])+'</ul>'
    dl='<ul class="docs">'+''.join(f'<li><span class="{"ok" if ok else "no"}">{"On File" if ok else "Missing"}</span><span>{t}</span></li>' for ok,t in p['docs'])+'</ul>'
    pg=head(f"{p['name']} | Prop Command Center")+NAV("Prop",'<a class="mw-hover homelink" id="mwBack" href="./" style="display:inline-flex;align-items:center;min-height:44px">← Back</a>')+CCH(p['name'],f"{p['addr']} · {p['line']}")+f'''
<div class="mw-sections">
<section class="mw-section" id="fin-sec" aria-label="Financial Details"><h2>Financial Details</h2><div id="fin"><p class="muted">Loading numbers</p></div></section>
<section class="mw-section" id="items-sec" aria-label="Open Items"><h2>Open Items</h2>{tl}</section>
<section class="mw-section" id="docs-sec" aria-label="Documents Status"><h2>Documents Status</h2>{dl}</section>
</div>
<footer class="mw-footer">{FOOT_BAR}</footer>
</main>
<script>
{DATA}
{SHARE}
/* R104 (Max Oct 17): Back returns to wherever you came from. history.back() when there is history and the referrer is
   same-origin; else a same-origin referrer or ?from= (same-origin only, no open redirects); else ./ (the real href). */
(function(){{const b=document.getElementById('mwBack');if(!b)return;
 b.addEventListener('click',e=>{{if(window.mwBack&&window.mwBack.VERSION){{e.preventDefault();e.stopImmediatePropagation();window.mwBack('./');}}}});  /* kit mw-back.js (loaded by mw-layout ly14) wins when present */
 const same=u=>{{try{{const x=new URL(u,location.href);return x.origin===location.origin&&x.href!==location.href?x.href:null}}catch(e){{return null}}}};
 b.addEventListener('click',e=>{{const ref=document.referrer&&same(document.referrer);
  if(history.length>1&&ref){{e.preventDefault();history.back();return}}
  const to=ref||same(new URLSearchParams(location.search).get('from')||'');if(to){{e.preventDefault();location.href=to}}}})}})();
const ID="{p['id']}";
Promise.resolve(FIN).then(F=>{{const f=F.properties[ID],el=document.getElementById('fin');
 const exp=Math.min(100,Math.round(f.known_total/f.rent*100)),cf=100-exp,anyEst=f.expenses.some(x=>x.est);
 el.innerHTML=big(f)+`<div class="split" role="img" aria-label="Of ${{usd(f.rent)}} rent, known expenses ${{usd(f.known_total)}}, cash flow ${{usd(f.cash_flow)}}"><i class="ex" style="width:${{exp}}%"></i><i class="cf" style="width:${{cf}}%"></i></div>
 <div class="splitkey"><span><i class="ex"></i>Expenses ${{usd(f.known_total)}}${{star(anyEst)}}</span><span><i class="cf"></i>Cash Flow ${{usd(f.cash_flow)}}${{star(f.cash_flow_est)}}</span></div>
 <table class="ft"><thead><tr><th>Monthly</th><th>Amount</th><th>Source</th></tr></thead><tbody>
 <tr><td>Rent</td><td>${{usd(f.rent)}}</td><td>Lease</td></tr>
 ${{f.expenses.map(x=>`<tr><td>${{x.label}}<small class="src">${{x.source}}${{x.as_of?' · '+fmt(x.as_of):''}}</small></td><td>${{usd(x.amount)}}${{star(x.est)}}</td><td>${{x.source}}${{x.as_of?' · '+fmt(x.as_of):''}}</td></tr>`).join('')}}
 <tr class="tot"><td>Known Expenses</td><td>${{usd(f.known_total)}}${{star(anyEst)}}</td><td></td></tr>
 <tr class="tot"><td>Cash Flow</td><td>${{usd(f.cash_flow)}}${{star(f.cash_flow_est)}}</td><td>Rent minus known expenses</td></tr></tbody></table>
 <h3 class="caps">Annual</h3><table class="ft"><tbody>
 <tr><td>Rent</td><td>${{usd(f.rent*12)}}</td><td>Monthly × 12</td></tr>
 <tr><td>Known Expenses</td><td>${{usd(+(f.known_total*12).toFixed(2))}}${{star(1)}}</td><td>Monthly × 12</td></tr>
 <tr class="tot"><td>Cash Flow</td><td>${{usd(+(f.cash_flow*12).toFixed(2))}}${{star(1)}}</td><td>Monthly × 12</td></tr></tbody></table>
 <h3 class="caps">Last Rent</h3><p class="fp">${{f.last_rent.label}}, ${{fmt(f.last_rent.date)}}${{star(f.last_rent.est)}}: ${{f.last_rent.detail}}</p>
 ${{f.extra.map(x=>`<p class="fp"><b>${{x.label}}:</b> ${{x.value}} <span class="pill">${{x.note}}</span></p>`).join('')}}
 ${{f.notes.map(n=>`<p class="fp muted">${{n}}</p>`).join('')}}
 <p class="legend">* Estimated or waiting for records</p>`}}).catch(()=>{{}});
</script>
'''+CHAT
    open(D+'/'+p['id']+'.html','w').write(kit_sync(pg,p['id']))
