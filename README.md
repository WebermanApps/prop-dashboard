# Prop Dashboard
Static site, hosted on GitHub Pages: repo WebermanApps/prop-dashboard -> https://webermanapps.github.io/prop-dashboard/
- Properties: edit the PROPS array in index.html (one object per property; id = URL hash, e.g. #mellow-wood). A third property = one new object; tabs, dots, panels build themselves.
- Update bar: routines edit report.json only. {"type": "Morning Report" or "Evening Report", "date": "YYYY-MM-DD", optional "text", optional "items": [...], optional "groups": [{"title": "Mellow Wood", "items": [...]}]}. Label switches automatically from type.
- Redeploy: git add -A && git commit -m Update && git push (gh is authenticated). Pages rebuilds in ~1 min.
- Check before publish: python3 check.py https://webermanapps.github.io/prop-dashboard/ screens  (393x852 phone w/ swipe test, 1470x956 @2x, TV 1920x1080, 2560x1440; also checks light bg under dark-mode, no emoji, Share not fixed)
- Rules: no tenant names, money, account/loan/phone numbers. Nicknames only.
- URL for Apps Home lives in /workspace/ops/apps-home/agents.d/prop.json (url field only).
