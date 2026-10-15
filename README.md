# Prop Dashboard
Static site, hosted on GitHub Pages: repo WebermanApps/prop-dashboard -> https://webermanapps.github.io/prop-dashboard/
- Properties: edit the PROPS array in index.html (one object per property; id = URL hash, e.g. #mellow-wood). Each property is its own card (agent-dashboards-09 A One Card Each). A third property = one new object; tabs, dots, panels build themselves.
- Top of page: sticky shared top bar (Apps Home, Prop, Updated time, Share icon) > title > **Ready To Swipe shelf** (R66, shared kit `deck-shelf.js?v=2`, up to 5 decks incl. pinned unfinished) > report as ONE line that expands > collapsed "Notifications" dropdown (max 2) > Mellow Wood | Wickfield switcher (sticky under the bar). No Overall Status section.
- Panels: stat strip (Status, Decisions, Due Soon, Latest), then condensed rows (2-line clamp, tap to expand, dates right-aligned, first 5 then See All). Decisions with a due date: ["text","YYYY-MM-DD"].
- Routines (R65): week strip (agent-dashboards-16 A) + shared kit `routines-section.js?v=2` / `.css?v=2` driven by `routines.json` (schema `/workspace/ops/brand/routines-section.md`). Custom groups (e.g. One-Time) are allowed.
- Ready To Swipe shelf (R66, Oct 14 19:55): `<section data-shelf="shelf.json">` at the very top + shared kit `deck-shelf.js?v=2` / `.css?v=2` (+ `submit.js`). `shelf.json` holds 3-5 ready 20-card decks (agent `prop`), `pinned` unfinished decks count toward the 5-deck cap. Decks never appear anywhere lower on the page (no Apps-row deck chips). Banks: `style-swipe/banks/prop-{properties,tenant-lease,maintenance,paperwork,dashboard}.json`, built by `/workspace/ops/prop/shelf/make_banks.py`.
- **Refill after submit (every Prop deck submission):** after the results are saved (and `carry_over.py record` run), run `cd /workspace/style-swipe && python3 tools/ready_shelf.py refill <deck_id> --shelf /workspace/ops/prop/dashboard/shelf.json --agent prop` (keeps the slot, logs it in `done`, skipped cards reworded/dropped per R64), then commit + push style-swipe and this repo. If a bank runs low, add pairs in make_banks.py and rerun it. Answered/noted cards disappear; only unanswered remain.
- Updated time = later of BUILT (index.html, bump on each edit) and report.json "updated".
- Morning Report run (Evening Report retired Oct 14, Max 20:00): first read MORNING-NOTES.md and PENDING.md in this folder if present (local only, gitignored), fold them in, then delete them.
- Routines edit report.json only:
  {"type": "Morning Report" (only; due by 5:00 AM ICT), "date": "YYYY-MM-DD",
   "notifications": [ {"text": "full line", "short": "summary-line text", "due": "YYYY-MM-DD" (optional)} ],   <- MAX 2, most important first; [] hides the dropdown
   optional "summary": "one-line text for the collapsed report bar" (default: group counts), "updated": ISO time,
   optional "text" / "items": [...] / "groups": [{"title","items"}]  <- report text shown small inside the dropdown under the notifications}
  Summary line = "Notifications · N" + first item's "short".
- Redeploy: git add -A && git commit -m Update && git push (gh is authenticated). Pages rebuilds in ~1 min.
- Check before publish: python3 check.py https://webermanapps.github.io/prop-dashboard/ screens  (393x852 phone w/ swipe test, 1100x800, 1470x956 @2x, TV 1920x1080, 2560x1440; also checks light bg under dark-mode, no emoji, Share not fixed)
- Rules: no tenant names, money, account/loan/phone numbers. Nicknames only.
- URL for Apps Home lives in /workspace/ops/apps-home/agents.d/prop.json (url field only).
- Layout: below 1100px = swipe carousel; 1100px+ = both panels side by side (tabs jump/highlight only).
- Money (Max approved public figures Oct 15): edit finance.json only (rent, last_rent, expenses with est:true for a star, known_total, cash_flow). Never add investor share, tenant names, or account/loan numbers. finance-inventory.md is local research and is gitignored (it has names and account numbers).
