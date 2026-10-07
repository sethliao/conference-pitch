# Field Notes · Traps & Negotiation Structure

> Everything below comes from the real GOSIM Shenzhen 2026 run. Each rule cost either a re-run or a rework.
> 🇨🇳 中文版：[判据库.md](判据库.md)

## Research

1. **Sponsor names live in logo `alt` attributes, not in the page text** — parsing visible text concludes "0 sponsors". False.
2. **Splitting sponsor tiers by character offset is wrong** — single-blob rendering can put tens of thousands of chars between heading and logos. Use structural attributes (e.g. `data-filter-category`); ⚠️ never guess attribute names, read the DOM.
3. **HTTP 200 can be a 404 page** — a normal status code ≠ the page exists. Footer social icons get misread as sponsors; only trust imgs with sponsor styling classes.
4. **Find the person who can say yes > find the "right" person** — general inboxes sink; the organizer/co-host decision chain is shortest.

## Proposal

5. **Barter before pricing, pricing last** — first "what you get" (content on your official channels, fully licensed), then money. Order is the negotiation.
6. **⛔ Never say "all free"** — say "if a barter works, I'm happy to do it free". Keeps room, keeps dignity.
7. **One identity only** — stacked identities halve the credibility of each. Everything else demotes to "supporting evidence".
8. **Self-deprecating words go to zero** — one "just practicing" zeroes your pricing power. Grep before finalizing.
9. **Round your numbers** — "around 7.5K". Exact numbers look small and hand them a haggling anchor.
10. **Caption the cover photo "real shoot, I'm in it"** — in the AI era, real on-site photos must prove they're not generated.

## Engineering

11. **Exit code 0 ≠ layout intact** — after headless-Chrome PDF export, always inspect page renders (`pdftoppm -r 96 -png`).
12. **Never validate by "split pages into single HTMLs and screenshot"** — splitting breaks CSS inheritance; everything is a false alarm.
13. **Symlink the image library, never copy** — one canonical store; each proposal `ln -s` to it. Add once, available everywhere.
14. **⛔ Never bulk-import the photo pool** — hundreds of photos choke the workflow; import by collection.
15. **Archive old versions, mark "⛔ do not use"** — the send-checklist holds exactly two files: final PDF + final body.

## Sending

16. **Send from your personal mailbox** — first contact from an unfamiliar automation address goes to trash.
17. **Shorter email is better** — 4 paragraphs: intro / attachment / receipt request / off-ramp. Detail lives in the attachment.
18. **Always include the off-ramp** — "If it doesn't fit this time, no worries — I'll still be there." No bridges burned; there's always a next edition.
