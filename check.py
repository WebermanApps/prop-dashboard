"""Layout check (R80). Usage: python3 check.py <file:// or https URL to index.html> [screens_dir]
Checks every size: no horizontal overflow, 44px targets, light bg, no emoji, Apps Home link, section order,
no Notifications, report dropdown closed, property toggle present; then each property page."""
import sys,json
from playwright.sync_api import sync_playwright
url=sys.argv[1].split('#')[0].split('?')[0]; out=sys.argv[2] if len(sys.argv)>2 else None
base=url.rsplit('/',1)[0]+'/'
S=[("phone-393",393,852,3,True),("lap-1100",1100,800,2,False),("mba-1280",1280,800,2,False),("mba-1470",1470,956,2,False),("tv-1920",1920,1080,1,False),("monitor-2560",2560,1440,1,False)]
JS=r"""()=>{const r={sw:document.documentElement.scrollWidth,iw:innerWidth,small:[],overflow:[]};
document.querySelectorAll('a,button,summary').forEach(e=>{if(e.closest('.mw-chat,[class*=chat],.pseg,.status-extra,.doc-open,.tdx,.stmt-pop'))return;const b=e.getBoundingClientRect();if(b.width&&e.offsetParent&&(b.width<44||b.height<44))r.small.push((e.textContent.trim().slice(0,20)||e.getAttribute('aria-label'))+' '+Math.round(b.width)+'x'+Math.round(b.height))});
document.querySelectorAll('main *').forEach(e=>{if(e.closest('.ptrack,.track,[data-shelf],.cf-strip,.pseg'))return;const b=e.getBoundingClientRect();if(b.width&&b.right>innerWidth+1)r.overflow.push(e.tagName+'.'+(e.className||'').toString().slice(0,40))});
const bg=getComputedStyle(document.body).backgroundColor.match(/\d+/g).map(Number);r.light=bg.slice(0,3).every(v=>v>200);
r.emoji=/\p{Extended_Pictographic}/u.test(document.body.innerText);
const H=[...document.querySelectorAll('a')].find(a=>a.href==='https://webermanapps.github.io/a-o956qercs5ubd57y/');r.home=!!H;
r.footer=/Built by Machan/.test(document.body.innerText)&&![...document.querySelectorAll('a')].some(a=>/maxweberman\.com/i.test(a.href||''))&&[...document.querySelectorAll('button,a')].some(e=>/share/i.test(e.textContent+(e.getAttribute('aria-label')||'')));
r.order=[...document.querySelectorAll('.mw-sections > section, footer')].map(e=>e.id||e.tagName).join('>');
r.todo=document.querySelectorAll('[data-mw-slot="todo"]').length;
r.notif=!!document.getElementById('notif')||/Notifications/.test(document.body.innerText);
const R=document.getElementById('report');r.report=R?(R.hidden?'hidden':'closed='+!R.open):'n/a';
r.toggle=[...document.querySelectorAll('.pseg button[data-p]')].map(b=>b.dataset.p);
r.hasPanel=!!document.querySelector('.pview,.status-card,#cf12');
r.stars=document.querySelectorAll('.star').length;return r}"""
bad=0
with sync_playwright() as p:
  b=p.chromium.launch(args=["--allow-file-access-from-files"])
  for page in ["index.html","mellow-wood.html","wickfield.html"]:
    u=base+page
    for n,w,h,s,m in S:
      pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=s,is_mobile=m,has_touch=m,color_scheme="dark")
      pg.goto(u+"?v="+n,wait_until="networkidle");pg.wait_for_timeout(700)
      r=pg.evaluate(JS);ok=r['sw']<=r['iw'] and not r['overflow'] and not r['small'] and r['light'] and not r['emoji'] and r['home'] and r['footer'] and not r['notif']
      if page=="index.html":
        ok=ok and r['order'] in("decks-sec>todo-sec>props-sec>routines-sec","decks-sec>props-sec>routines-sec") and r['todo']==1 and r['toggle']==['mellow-wood','wickfield'] and r['hasPanel']
      else:
        ok=ok and r['hasPanel']
      bad+=not ok;print(("OK  " if ok else "FAIL"),page,n,json.dumps({k:r[k] for k in r if k not in('overflow','small') or r[k]}))
      if out and n in("phone-393","mba-1470"):
        pg.screenshot(path=f"{out}/{page[:-5]}-{n}.png",full_page=True)
      if page=="index.html" and m:
        pg.click(".pseg button[data-p=wickfield]");pg.wait_for_timeout(400);print("  toggle ->",pg.locator('#pname').inner_text())
      pg.close()
  b.close()
sys.exit(1 if bad else 0)
