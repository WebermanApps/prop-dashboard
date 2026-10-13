# Prop Dashboard
Static site, hosted on GitHub Pages: repo WebermanApps/prop-dashboard -> https://webermanapps.github.io/prop-dashboard/
- Properties: edit the PROPS array in index.html (one object per property; id = URL hash, e.g. #mellow-wood). A third property = one new object; tabs, dots, panels build themselves.
- Update bar: edit report.json (type "Morning Report" by 5:00 AM ICT, "Evening Report" from 6:00 PM ICT; items = lines).
- Redeploy: git add -A && git commit -m Update && git push (gh is authenticated). Pages rebuilds in ~1 min.
- Check before publish: python3 check.py https://webermanapps.github.io/prop-dashboard/ screens  (393x852 phone with swipe test, 1470x956 @2x, 2560x1440)
- Rules: no tenant names, money, account/loan/phone numbers. Nicknames only.
- URL for Apps Home lives in /workspace/ops/apps-home/agents.d/prop.json (url field only).
