import sys,json
from playwright.sync_api import sync_playwright
url=sys.argv[1].split('#')[0]; out=sys.argv[2] if len(sys.argv)>2 else None
S=[("phone-393",393,852,3,True),("mba-1470",1470,956,2,False),("tv-1920",1920,1080,1,False),("monitor-2560",2560,1440,1,False)]
js=r"""()=>{const r={sw:document.documentElement.scrollWidth,iw:innerWidth,small:[],overflow:[]};
document.querySelectorAll('a,button').forEach(e=>{const b=e.getBoundingClientRect();if(b.width&&getComputedStyle(e).visibility!='hidden'&&(b.width<44||b.height<44))r.small.push((e.textContent.trim().slice(0,20)||e.getAttribute('aria-label'))+' '+Math.round(b.width)+'x'+Math.round(b.height))});
document.querySelectorAll('main *').forEach(e=>{if(e.closest('.track'))return;const b=e.getBoundingClientRect();if(b.right>innerWidth+1)r.overflow.push(e.tagName+'.'+e.className)});
const bg=getComputedStyle(document.body).backgroundColor.match(/\d+/g).map(Number);r.light=bg.slice(0,3).every(v=>v>200);
r.emoji=/\p{Extended_Pictographic}/u.test(document.body.innerText);
const sh=document.getElementById('share'),sb=sh.getBoundingClientRect();r.shareFixed=['fixed','sticky'].includes(getComputedStyle(sh.parentElement).position);
r.minFont=Math.min(...[...document.querySelectorAll('main li,main p,main b,.tab')].filter(e=>e.offsetParent).map(e=>parseFloat(getComputedStyle(e).fontSize)));
r.report=document.getElementById('rtype').textContent;r.tab=[...document.querySelectorAll('.tab')].map(t=>t.getAttribute('aria-selected')).join(',');r.hash=location.hash;return r}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,w,h,s,m in S:
    pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=s,is_mobile=m,has_touch=m,color_scheme="dark")
    pg.goto(url+"?v="+n,wait_until="networkidle");pg.wait_for_timeout(600)
    print(n,json.dumps(pg.evaluate(js)))
    if m:
      # simulate a swipe: scroll the snap track like a finger drag, then check the tab follows
      pg.evaluate("()=>{const t=document.getElementById('track');t.style.scrollBehavior='auto';t.scrollLeft=t.clientWidth*0.7}");pg.wait_for_timeout(900)
      print(" swipe->",pg.evaluate("()=>[location.hash,document.querySelector('.tab[aria-selected=true]').textContent,document.getElementById('track').scrollLeft]"))
      pg.click(".tab >> nth=0");pg.wait_for_timeout(800);print(" tab->",pg.evaluate("location.hash"))
    else:
      pg.keyboard.press("ArrowRight");pg.wait_for_timeout(800);print(" key->",pg.evaluate("location.hash"));pg.keyboard.press("ArrowLeft");pg.wait_for_timeout(800)
    if out:
      for hs in (["mellow-wood","wickfield"] if m else [None]):
        if hs: pg.goto(url+"?v="+n+"#"+hs,wait_until="networkidle");pg.wait_for_timeout(700)
        pg.set_viewport_size({"width":w,"height":h});H=pg.evaluate("document.documentElement.scrollHeight")
        pg.set_viewport_size({"width":w,"height":max(h,H)});pg.wait_for_timeout(400)
        nm=f"{n}-{hs.split('-')[0]}" if hs else n
        pg.screenshot(path=f"{out}/{nm}.png",full_page=True)
  b.close()
