import sys,json
from playwright.sync_api import sync_playwright
url=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else None
S=[("phone-390",390,844,3,True),("mba-1470",1470,956,2,False),("mba-1280",1280,800,2,False),("monitor-2560",2560,1440,1,False)]
js="""()=>{const r={sw:document.documentElement.scrollWidth,iw:innerWidth,small:[],overflow:[]};
document.querySelectorAll('a,button').forEach(e=>{const b=e.getBoundingClientRect();if(b.width<44||b.height<44)r.small.push((e.id||e.textContent.trim().slice(0,20)||e.getAttribute('aria-label'))+' '+Math.round(b.width)+'x'+Math.round(b.height))});
document.querySelectorAll('h1,h2,h3,p,li,span,b').forEach(e=>{if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!='visible')r.overflow.push(e.textContent.slice(0,30))});
const m=document.querySelector('main').getBoundingClientRect();r.mainW=Math.round(m.width);r.h1=getComputedStyle(document.querySelector('h1')).fontSize;r.body=getComputedStyle(document.body).fontSize;return r}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for n,w,h,s,m in S:
    pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=s,is_mobile=m,has_touch=m)
    pg.goto(url+"?v="+n,wait_until="networkidle");pg.wait_for_timeout(500)
    print(n,json.dumps(pg.evaluate(js)))
    if out:
      H=pg.evaluate("document.documentElement.scrollHeight");pg.set_viewport_size({"width":w,"height":max(h,H)});pg.wait_for_timeout(300);pg.screenshot(path=f"{out}/{n}.png",full_page=True)
  b.close()
