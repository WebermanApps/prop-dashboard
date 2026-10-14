# Prop Dashboard
Static site, hosted on GitHub Pages: repo WebermanApps/prop-dashboard -> https://webermanapps.github.io/prop-dashboard/
- Properties: edit the PROPS array in index.html (one object per property; id = URL hash, e.g. #mellow-wood). Each property is its own card (agent-dashboards-09 A One Card Each). A third property = one new object; tabs, dots, panels build themselves.
- Top of page: sticky shared top bar (Apps Home, Prop, Updated time, Share icon) > title > **Open a New Deck launcher** (R66, unfinished decks pinned with it) > Apps row > report as ONE line that expands > collapsed "Notifications" dropdown (max 2) > Mellow Wood | Wickfield switcher (sticky under the bar). No Overall Status section.
- Panels: stat strip (Status, Decisions, Due Soon, Latest), then condensed rows (2-line clamp, tap to expand, dates right-aligned, first 5 then See All). Decisions with a due date: ["text","YYYY-MM-DD"].
- Routines (R65): week strip (agent-dashboards-16 A) + shared kit `routines-section.js?v=2` / `.css?v=2` driven by `routines.json` (schema `/workspace/ops/brand/routines-section.md`). Custom groups (e.g. One-Time) are allowed.
- Deck launcher (R66): `launcher.json` + shared kit `deck-launcher.js?v=1`. Categories are Prop-specific. Every deck is exactly 20 cards. Request sends `{type:'deck-request',agent:'prop',...}` via MWSubmit to `ops/submit/inbox/prop`. Ready decks live under `deck/` (e.g. `deck/?d=prop-q1`).
- **Refill after submit:** after any Prop deck submission, build a fresh 20-card deck in the same categories (skipped cards reworded per R64) and set it as `ready` in `launcher.json`. Answered/noted cards disappear; only unanswered remain.
- Updated time = later of BUILT (index.html, bump on each edit) and report.json "updated".
- Morning/Evening Report runs: first read MORNING-NOTES.md and PENDING.md in this folder if present (local only, gitignored), fold them in, then delete them.
- Routines edit report.json only:
  {"type": "Morning Report" | "Evening Report" | "Fresh Start", "date": "YYYY-MM-DD",
   "notifications": [ {"text": "full line", "short": "summary-line text", "due": "YYYY-MM-DD" (optional)} ],   <- MAX 2, most important first; [] hides the dropdown
   optional "summary": "one-line text for the collapsed report bar" (default: group counts), "updated": ISO time,
   optional "text" / "items": [...] / "groups": [{"title","items"}]  <- report text shown small inside the dropdown under the notifications}
  Summary line = "Notifications · N" + first item's "short".
- Redeploy: git add -A && git commit -m Update && git push (gh is authenticated). Pages rebuilds in ~1 min.
- Check before publish: python3 check.py https://webermanapps.github.io/prop-dashboard/ screens  (393x852 phone w/ swipe test, 1100x800, 1470x956 @2x, TV 1920x1080, 2560x1440; also checks light bg under dark-mode, no emoji, Share not fixed)
- Rules: no tenant names, money, account/loan/phone numbers. Nicknames only.
- URL for Apps Home lives in /workspace/ops/apps-home/agents.d/prop.json (url field only).
- Layout: below 1100px = swipe carousel; 1100px+ = both panels side by side (tabs jump/highlight only).
