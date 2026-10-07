# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [1.2.1] - 2026-10-07

### Fixed
- `templates/deck.html` / `templates/proposal.html` 加自适应缩放：100% 缩放即可看全页（屏幕窄时整体缩小，打印自动还原 1920）——不再要手动缩到 80%

## [1.2.0] - 2026-10-07

### Added
- `templates/deck.html` — 通用可编辑 deck 骨架（3 页占位：封面/三卡/CTA），配 `scripts/inject_editor.py` = 点开即编辑 + 网页里导 PDF
- 社区健康文件：CONTRIBUTING / CODE_OF_CONDUCT / SECURITY / CHANGELOG
- `.github/`：bug / feature issue 表单 + PR 模板（红线自查 checkbox）
- 质量门：`scripts/validate_skills.py`（零依赖按 Agent Skills 规范校验）+ GitHub Action
- README 徽章行 + `assets/social-preview.png`（1280×640）

### Notes
- 规范化框架来自 [jdevalk/skills](https://github.com/jdevalk/skills) 的 github-repo 6 类审计（致谢）

## [1.1.0] - 2026-10-07

### Added
- 🇬🇧 英文版全套：`SKILL.en.md`、模板×3 EN、`knowledge/field-notes.en.md`
- ⭐ 提案工具链进仓：
  - `templates/proposal.html` — GOSIM 实战设计系统 + 8 页占位骨架（已渲染验收）
  - `scripts/inject_editor.py` + `scripts/proposal-editor-layer.html` — 就地编辑层（改字/裁剪换图/链接体检/导 PDF，幂等）
  - `scripts/export_pdf.sh` — headless 导出 PDF + 逐页验收图
- GitHub 仓库 About 描述（中英）
- frontmatter description 按 Agent Skills 规范重写（Use-when 触发式 + 关键词）

## [1.0.0] - 2026-10-07

### Added
- 首个公开版：`conference-pitch` skill 六站流程（GOSIM Shenzhen 2026 实战背书）
- 模板×3（口径表 / 邮件正文 / 发信清单）
- `knowledge/判据库.md` 18 条（踩坑 + 谈判结构）
- 中英 README + 管线 SVG + CC BY-NC 4.0
