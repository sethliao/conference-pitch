# conference-pitch

> From spotting a conference you want to work with, to sending the proposal and email — there's a pile of admin work in between. This skill turns that pile into a pipeline.

**[中文 README](README.md)**

![pipeline](assets/pipeline.svg)

## Proven in production (real numbers, not demo data)

**1 real conference** (GOSIM Shenzhen 2026) full cycle → **6 stations** → **8-page proposal PDF** (1920×1080, with pricing page + barter offer) → **9 locked messaging decisions** → **4-paragraph email** → **1 send-checklist** → **3 hard-won scraping lessons**.

## What you get

| Your situation | You get |
|---|---|
| Found a conference you want to partner with, no idea where to start | Phase 0 research checklist: contact channels / hard facts / **decision chain (who can say yes)** / sponsor tiers (who pays real money) |
| Writing every proposal from scratch | 8-page skeleton + 9-item messaging table; swap conferences by swapping one data block |
| Don't know how to name a price | Pricing page structure + **barter-before-pricing** negotiation order (never say "all free") |
| Long emails nobody reads | 4-paragraph email template + send-checklist (only two files: PDF + body) |
| Conference websites fighting your scraper | 3 field-tested scraping rules (sponsor names live in logo `alt` attributes; visible text gives you zero) |

## Install

```bash
npx -y skills add sethliao/conference-pitch -g --all
```

## Quick start

Tell your agent: **"Next conference is <name>."**

Then follow [docs/从第一个大会开始.md](docs/从第一个大会开始.md) (CN): research → lock your messaging (10 min, the most valuable step) → pick photos → generate proposal → review → **you hit send yourself**.

## The philosophy

- **Productize the admin work; keep taste and the send button human.**
- **Barter before pricing, pricing last.** Order is the negotiation.
- **One identity only.** Stacked identities halve the credibility of each.
- **Honest, never self-deprecating.** One "just practicing" kills your pricing power — grep it out before finalizing.

More field notes → [knowledge/判据库.md](knowledge/判据库.md) · [field-notes.en.md](knowledge/field-notes.en.md) (18 rules, all from real runs)

## Repo layout

```
skills/conference-pitch/   main skill (6-station pipeline + red lines · CN & EN)
  templates/               proposal.html (8-page skeleton + design system) · messaging table · email · send-checklist (CN & EN)
scripts/                   inject_editor.py (in-place editor: edit text / swap images / export PDF)
                           proposal-editor-layer.html (editor source) · export_pdf.sh (export + per-page visual check)
docs/                      scenario quickstart
knowledge/                 18 field notes (CN & EN · traps + negotiation structure)
assets/                    pipeline diagram
```

⭐ **The proposal is a toolchain, not just a document**: start from `templates/proposal.html` → fill content → `scripts/inject_editor.py` injects the in-place editor (edit text, crop/swap images, link health-check, export PDF in the browser) → `scripts/export_pdf.sh` exports PDF + per-page renders for visual acceptance.

## Author

**Zhipeng "Seth" Liao** — 3D & AI content creator, one-person studio practitioner.

- GitHub: [@sethliao](https://github.com/sethliao)
- Related: [one-person-studio](https://github.com/sethliao/one-person-studio)

## License

[CC BY-NC 4.0](LICENSE) — free for non-commercial use; contact the author for commercial licensing.
