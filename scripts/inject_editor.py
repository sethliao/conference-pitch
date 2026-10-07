#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「提案就地编辑器 v2」注入（或升级）到任意提案 HTML。

用法：
    python3 scripts/inject_editor.py <目标 html> [<目标 html2> ...]

幂等：重复跑只会替换 EDITOR-CSS / EDITOR-JS 标记之间的内容，
      且会先清掉 v1 遗留的编辑器 CSS/JS，不碰任何正文内容与样式。
依赖：scripts/proposal-editor-layer.html（与本脚本同目录，编辑层单一真源）。
图库：向上最多 4 级找 img-lib/{used,pool,gdrive}/，找到就把图库清单内嵌进提案；
      找不到也能正常注入（只是没有图库侧边栏）。
"""
import re, sys, pathlib, json, os

BUILD = pathlib.Path(__file__).parent
LAYER = BUILD / 'proposal-editor-layer.html'

def load_layer():
    raw = LAYER.read_text(encoding='utf-8')
    css = re.search(r'<!-- EDITOR-CSS:BEGIN -->(.*?)<!-- EDITOR-CSS:END -->', raw, re.S).group(1).strip()
    js = re.search(r'<!-- EDITOR-JS:BEGIN -->(.*?)<!-- EDITOR-JS:END -->', raw, re.S).group(1).strip()
    # 带标记写入 → 下次可精准移除，保证幂等
    css_block = '<!-- EDITOR-CSS:BEGIN -->\n' + css + '\n<!-- EDITOR-CSS:END -->'
    js_block = '<!-- EDITOR-JS:BEGIN -->\n' + js + '\n<!-- EDITOR-JS:END -->'
    return css_block, js_block

CSS_BLOCK, JS_BLOCK = load_layer()
CSS, JS = CSS_BLOCK, JS_BLOCK          # 生成器也引用同一份（单一真源）

# v1 遗留：CSS 从「就地编辑工具条」注释到 </style>；JS 整段
RE_CSS_V1 = re.compile(r'/\*\s*═+\s*就地编辑工具条[\s\S]*?</style>')
RE_JS_V1 = re.compile(r'<script>\s*/\*\s*═+\s*就地编辑 \+ 导出[\s\S]*?</script>')
# v2 自身：优先按标记移除，其次按 data-proposal-editor 属性兜底（兼容早期未写标记的注入）
RE_CSS_NEW = re.compile(r'<!-- EDITOR-CSS:BEGIN -->[\s\S]*?<!-- EDITOR-CSS:END -->')
RE_JS_NEW = re.compile(r'<!-- EDITOR-JS:BEGIN -->[\s\S]*?<!-- EDITOR-JS:END -->')
RE_CSS_ATTR = re.compile(r'<style data-proposal-editor>[\s\S]*?</style>')
RE_JS_ATTR = re.compile(r'<script data-proposal-editor>[\s\S]*?</script>')

# ── 精选图库清单：扫 img-lib，按「相对提案目录」的路径嵌成 JSON ──────────
# ⚠️ file:// 下 fetch 会被 CORS 拦死，所以不能读外部 json —— 只能内嵌
RE_LIB = re.compile(r'<!-- PE-LIB:BEGIN -->[\s\S]*?<!-- PE-LIB:END -->')
SOURCES = [('used', '提案用图'), ('pool', '自有精选'), ('gdrive', 'Drive 导入')]

def jpeg_size(path):
    """不依赖 Pillow 读 JPEG 尺寸；读不到返回 (0,0)"""
    try:
        with open(path, 'rb') as f:
            f.read(2)
            while True:
                b = f.read(1)
                if not b: return 0, 0
                if b != b'\xff': continue
                while b == b'\xff': b = f.read(1)
                if b in (b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc5', b'\xc6', b'\xc7',
                         b'\xc9', b'\xca', b'\xcb', b'\xcd', b'\xce', b'\xcf'):
                    f.read(3)
                    h, w = int.from_bytes(f.read(2), 'big'), int.from_bytes(f.read(2), 'big')
                    return w, h
                ln = int.from_bytes(f.read(2), 'big')
                f.read(ln - 2)
    except Exception:
        return 0, 0

def category_of(name, source):
    """分类来自既有标注：文件名前缀（`04-黑客松-…` / `09-creality-…` / `22-参考A-帧-…`）
       gdrive 组前缀是日期噪音（`00-0322_DIP`），统一归 'Drive'"""
    import os
    if source == 'gdrive': return 'Drive'
    stem = os.path.splitext(name)[0]
    m = re.match(r'^\d+-([^-]+)', stem)
    if m: return m.group(1)
    if source == 'used':
        return stem.split('-')[0] if '-' in stem else '其他'
    return 'Drive'

def build_lib_block(proposal_path: pathlib.Path) -> str:
    """返回要嵌进提案的图库 JSON 块；找不到 img-lib 就返回空块"""
    proposal_path = pathlib.Path(proposal_path).resolve()
    root = proposal_path.parent if proposal_path.is_file() else proposal_path
    lib = None
    for d in [root] + list(root.parents)[:4]:
        if (d / 'img-lib').is_dir(): lib = d / 'img-lib'; break
    if not lib: return ''
    items = []
    for sub, _label in SOURCES:
        folder = lib / sub
        if not folder.is_dir(): continue
        for f in sorted(folder.iterdir()):
            if f.name.startswith('.') or f.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
                continue
            rel = os.path.relpath(f, proposal_path.parent if proposal_path.is_file() else proposal_path)
            w, h = jpeg_size(f)
            items.append({'p': rel.replace('\\', '/'), 'n': f.name,
                          'c': category_of(f.name, sub), 's': sub, 'w': w, 'h': h})
    if not items: return ''
    body = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
    return ('<!-- PE-LIB:BEGIN -->\n<script id="pe-lib" type="application/json">'
            + body + '</script>\n<!-- PE-LIB:END -->')

def inject(path: pathlib.Path, with_lib: bool = True) -> str:
    raw = path.read_text(encoding='utf-8')
    orig = raw

    # 1) 清旧（标记 → 属性 → v1，三条兜底全清一遍）
    raw = RE_CSS_NEW.sub('', raw)
    raw = RE_JS_NEW.sub('', raw)
    raw = RE_LIB.sub('', raw)
    raw = RE_CSS_ATTR.sub('', raw)
    raw = RE_JS_ATTR.sub('', raw)
    raw = RE_CSS_V1.sub('</style>', raw)
    raw = RE_JS_V1.sub('', raw)

    # 2) 规范化：清掉 </head> / </body> 前堆积的空行（否则每次注入都多一行 → 不幂等）
    raw = re.sub(r'\n{2,}(?=</head>)', '\n', raw)
    raw = re.sub(r'\n{2,}(?=</body>)', '\n', raw)

    # 3) 装新
    if '</head>' not in raw or '</body>' not in raw:
        return f'✗ {path.name}：找不到 </head> / </body>，跳过'
    raw = raw.replace('</head>', CSS_BLOCK + '\n</head>', 1)
    lib = build_lib_block(path) if with_lib else ''
    if lib: raw = raw.replace('</head>', lib + '\n</head>', 1)
    raw = raw.replace('</body>', JS_BLOCK + '\n</body>', 1)

    if raw == orig:
        return f'· {path.name}：无变化'
    path.write_text(raw, encoding='utf-8')
    delta = len(raw) - len(orig)
    return f'✓ {path.name}：编辑器 v2 已注入（{len(raw):,} bytes，{delta:+,}）'

def main():
    args = sys.argv[1:]
    wb = BUILD.parent
    if args and args[0] == '--all':
        targets = []
        for p in sorted(wb.rglob('index.html')):
            if '_check' in p.name or p.parent.name == 'runs':
                continue
            if p.parent == wb:            # Workbench 根的工作台页
                continue
            txt = p.read_text(encoding='utf-8', errors='ignore')
            if 'section class="page' in txt or 'class="page cover"' in txt:
                targets.append(p)
        for p in sorted(wb.rglob('*修改版*.html')):
            targets.append(p)
    else:
        targets = [pathlib.Path(a) for a in args]

    if not targets:
        print(__doc__)
        return
    for t in targets:
        print(inject(t))

if __name__ == '__main__':
    main()
