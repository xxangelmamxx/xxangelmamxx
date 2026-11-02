#!/usr/bin/env python3
"""Adds a finale to the generated snake. Run: python3 assets/snake_finale.py dist site

When the last block is eaten, commits ripple out from it until the board is
full, LEVEL UP! sweeps across, then everything wipes clean and the loop resets.
snk has no hook for this, so it's layered onto the finished SVGs.
"""
import random
import re
import sys
from pathlib import Path

EXTRA_MS = 2000  # extra time added to the loop so the finale can breathe
RIPPLE_MS = 1300  # how long the commits take to fill the board
TEXT_MS = 800  # how long LEVEL UP! takes to sweep across
WIPE_MS = 700  # how long the board takes to clear before the reset
TEXT = "LEVEL UP!"

GLYPHS = {
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "V": ["#...#", "#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "!": ["#", "#", "#", "#", "#", ".", "#"],
    " ": ["..", "..", "..", "..", "..", "..", ".."],
}


def text_cells():
    """Returns the {(col, row)} cells that spell TEXT, centred on the 53-week board."""
    cols, x = [], 0
    for ch in TEXT:
        rows = GLYPHS[ch]
        cols += [(x + dx, y) for y, r in enumerate(rows) for dx, c in enumerate(r) if c == "#"]
        x += len(rows[0]) + 1
    offset = (53 - (x - 1)) // 2
    return {(c + offset, r) for c, r in cols}


def reveal(name, start, end, total):
    """Keyframes for a layer that switches on at start and off at end (ms)."""
    a, b = start * 100 / total, end * 100 / total
    return (
        f"@keyframes {name}{{0%,{a:.2f}%{{opacity:0}}{a + 0.05:.2f}%,{b:.2f}%{{opacity:1}}"
        f"{b + 0.05:.2f}%,100%{{opacity:0}}}}.{name}{{animation-name:{name}}}"
    )


def finale(svg):
    style = svg[svg.index("<style>") + 7 : svg.index("</style>")]
    duration = int(re.search(r"(\d+)ms", style).group(1))

    # each block's own keyframes start at the moment it gets eaten
    eaten = {n: float(p) for n, p in re.findall(r"@keyframes (c\w+)\{([\d.]+)%", style)}
    if not eaten:
        return svg
    last = max(eaten, key=eaten.get)
    x, y = map(int, re.search(rf'class="c {last}" x="(\d+)" y="(\d+)"', svg).groups())

    total = duration + EXTRA_MS
    scale = duration / total
    start = eaten[last] * duration / 100

    def stretch(m):
        p = float(m.group(1))
        return f"{p * scale:.2f}%,100%" if p == 100 else f"{p * scale:.2f}%"

    style = re.sub(r"([\d.]+)%(?=[,{])", stretch, style)
    style = style.replace(f"{duration}ms", f"{total}ms")

    cells = [tuple(map(int, c)) for c in re.findall(r'<rect class="c[^"]*" x="(\d+)" y="(\d+)"', svg)]
    grid = lambda v: (v - 2) // 16
    word = text_cells()
    span = range(min(c for c, _ in word) - 1, max(c for c, _ in word) + 2)
    wipe = total - WIPE_MS - 200

    reach = max(((cx - x) ** 2 + (cy - y) ** 2) ** 0.5 for cx, cy in cells) or 1
    rng = random.Random(53)
    css = [
        ".f{animation:none linear %dms infinite;opacity:0}" % total,
        ".l1{fill:var(--c1)}.l2{fill:var(--c2)}.l3{fill:var(--c3)}.l4{fill:var(--c4)}.w{fill:var(--cs)}",
        ".t{animation:tw 1.3s ease-in-out infinite}@keyframes tw{50%{opacity:.5}}",
    ]
    layers, words = {}, {}
    for cx, cy in cells:
        col, row = grid(cx), grid(cy)
        ring = int(((cx - x) ** 2 + (cy - y) ** 2) ** 0.5 / reach * 35)
        # stay calm behind the word so it reads, sparkle everywhere else
        look = 'class="l1"' if col in span else (
            f'class="t l{rng.choice((1, 2, 2, 3, 3, 4))}" style="animation-delay:-{rng.uniform(0, 1.3):.2f}s"'
        )
        layers.setdefault(ring, []).append(f'<rect {look} x="{cx}" y="{cy}" width="12" height="12" rx="2"/>')
        if (col, row) in word:
            words.setdefault(col, []).append(f'<rect class="w" x="{cx}" y="{cy}" width="12" height="12" rx="2"/>')

    out = []
    for ring, rects in sorted(layers.items()):
        on = start + RIPPLE_MS * ring / 35
        off = wipe + WIPE_MS * ring / 35
        css.append(reveal(f"r{ring}", on, off, total))
        out.append(f'<g class="f r{ring}">{"".join(rects)}</g>')
    for col, rects in sorted(words.items()):
        on = start + RIPPLE_MS + TEXT_MS * col / 53
        css.append(reveal(f"w{col}", on, wipe, total))
        out.append(f'<g class="f w{col}">{"".join(rects)}</g>')

    style += "".join(css) + "@media (prefers-reduced-motion:reduce){.f{display:none}}"
    head, tail = svg[: svg.index("<style>") + 7], svg[svg.index("</style>") :]
    tail = tail.replace('<rect class="u', "".join(out) + '<rect class="u', 1)
    return head + style + tail


def main(src, dst):
    Path(dst).mkdir(exist_ok=True)
    for file in Path(src).glob("*.svg"):
        (Path(dst) / file.name).write_text(finale(file.read_text()))


if __name__ == "__main__":
    main(*sys.argv[1:3])
