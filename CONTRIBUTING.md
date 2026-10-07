# Contributing

感谢你想让这个 skill 变得更好。

## 报坑 / 提建议

- **Skill 没触发 / 触发错了** → 开 [Bug report](../../issues/new?template=bug_report.yml)，附上你说的话和 agent 的反应
- **流程建议**（哪一站不清楚、哪个模板不好用）→ 开 [Feature request](../../issues/new?template=feature_request.yml)
- **跑通了你自己的大会** → 也欢迎开 issue 晒一下，实战反馈是最值钱的贡献

## 改代码 / 改文档

1. Fork + 开分支，小步提交
2. 改动涉及 skill 内容时，跑一遍校验：`python3 scripts/validate_skills.py`
3. **中英双语文件要同步改**（`SKILL.md` ↔ `SKILL.en.md`，`templates/*.md` ↔ `*.en.md`，`knowledge/*`）
4. PR 里写清：改了什么、为什么、怎么验证的

## 红线（改了也不会合）

- ⛔ 引入任何真实个人信息（邮箱/电话/内部路径）
- ⛔ 把「本人过目后才发」的红线改松——这条是仓库存在的意义
- ⛔ 没有实战依据的「最佳实践」注水（判据库的每一条都来自真实跑通）

## License

提交即同意你的贡献以 [CC BY-NC 4.0](LICENSE) 发布。
