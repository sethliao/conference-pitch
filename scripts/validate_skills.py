#!/usr/bin/env python3
"""validate_skills.py — 按 Agent Skills 规范校验 skills/*/SKILL.md（零依赖）

规则（agentskills.io / Anthropic best-practices）：
  - frontmatter 必须有 name 和 description
  - name：1-64 字符，小写字母/数字/连字符，且必须等于目录名
  - description：非空、≤1024 字符
  - 正文 ≤500 行（超出警告不失败）
退出码：0 全部通过；1 有失败项。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")

def check(skill_dir: Path) -> list[str]:
    errs = []
    f = skill_dir / "SKILL.md"
    if not f.exists():
        return [f"{skill_dir.name}: 缺 SKILL.md"]
    text = f.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return [f"{skill_dir.name}: 缺 YAML frontmatter"]
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)(?=^\w+:|\Z)", fm, re.M | re.S)
    if not name:
        errs.append(f"{skill_dir.name}: frontmatter 缺 name")
    else:
        n = name.group(1).strip().strip('"\'')
        if not NAME_RE.match(n):
            errs.append(f"{skill_dir.name}: name「{n}」不合规（小写/数字/连字符，≤64）")
        if n != skill_dir.name:
            errs.append(f"{skill_dir.name}: name「{n}」≠ 目录名")
    if not desc:
        errs.append(f"{skill_dir.name}: frontmatter 缺 description")
    else:
        d = " ".join(desc.group(1).split())
        if len(d) > 1024:
            errs.append(f"{skill_dir.name}: description 超长（{len(d)} > 1024）")
    body_lines = text[m.end():].count("\n")
    if body_lines > 500:
        print(f"  ⚠ {skill_dir.name}: 正文 {body_lines} 行 > 500（建议拆到 references/）")
    return errs

def main() -> int:
    skills_root = ROOT / "skills"
    dirs = [d for d in sorted(skills_root.iterdir()) if d.is_dir()] if skills_root.is_dir() else []
    if not dirs:
        print("没找到 skills/*/ —— 目录结构不对")
        return 1
    failed = False
    for d in dirs:
        errs = check(d)
        if errs:
            failed = True
            for e in errs:
                print(f"✗ {e}")
        else:
            print(f"✓ {d.name}")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
