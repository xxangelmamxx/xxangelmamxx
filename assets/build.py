#!/usr/bin/env python3
"""Regenerates every animated SVG in this folder. Run: python3 assets/build.py

Edit the data near the top (STATS, QUESTS, CARDS) and re-run.
The SVGs are shown through <img>, so they stay pure SVG + CSS, with no JS.
"""
import base64
import random
from html import escape
from pathlib import Path

HERE = Path(__file__).parent

# ── edit me ──────────────────────────────────────────────────────────────────
STATS = [  # label, value out of 100 (the numbers are vibes, not science)
    ("CURIOSITY", 99, "#B5A4DB"),
    ("CHAOS", 87, "#D6A6BF"),
    ("CLEAN CODE", 74, "#9D8FC4"),
    ("DEBUGGING", 68, "#C8A9D6"),
    ("SLEEP", 12, "#7D709C"),
]

QUESTS = [
    ("Build interesting projects", "ACTIVE"),
    ("Get better at LeetCode", "ACTIVE"),
    ("Contribute to open source", "ACTIVE"),
    ("Learn better system design", "ACTIVE"),
    ("Stop opening new browser tabs", "FAILED"),
]

CARDS = [
    {
        "file": "card-shell",
        "kind": "MAIN QUEST",
        "title": "Mini-Shell",
        "lines": ["a bash-like shell written in C, with", "pipes, redirects, and parallel commands."],
        "stack": ["C", "POSIX", "Flex", "Bison"],
        "icon": "shell",
    },
    {
        "file": "card-terrain",
        "kind": "MAIN QUEST",
        "title": "Heightmap Terrain",
        "lines": ["a real-time 3D scene built from shaders,", "matrices, and image-based terrain."],
        "stack": ["Python", "ModernGL", "OpenGL"],
        "icon": "terrain",
    },
    {
        "file": "card-tracelens",
        "kind": "OPEN SOURCE / MERGED",
        "title": "TraceLens #34",
        "lines": ["made /reserve one real transaction, so", "concurrent requests can't race the lock."],
        "stack": ["PostgreSQL", "Concurrency"],
        "icon": "merge",
    },
    {
        "file": "card-boba",
        "kind": "MAIN QUEST",
        "title": "BobaLab",
        "lines": ["a build-your-own boba shop. the cup", "updates live. hot tea with ice? denied."],
        "stack": ["React", "Express", "PostgreSQL"],
        "icon": "boba",
    },
    {
        "file": "card-adulting",
        "kind": "MAIN QUEST",
        "title": "Adulting 101",
        "lines": ["finish real-life tasks, step by step,", "and watch your adulting level go up."],
        "stack": ["JavaScript", "Express", "PostgreSQL"],
        "icon": "stars",
    },
    {
        "file": "card-valorant",
        "kind": "LIVE DEMO",
        "title": "Valorant Lineups",
        "lines": ["build, edit, and save your own", "Valorant agent lineups."],
        "stack": ["React", "Supabase"],
        "icon": "crosshair",
    },
]
INVENTORY = [  # shelf name, items: (label, icon in assets/icons, +file for a logo that needs a dark tile, ~name from ICONS)
    ("LANGUAGES", [
        ("Python", "py"), ("JavaScript", "js"), ("C", "c"), ("C++", "cpp"), ("Java", "java"), ("C#", "cs"),
        ("HTML", "html"), ("CSS", "css"), ("R", "r"), ("Bash", "bash"), ("SQL", "~database"), ("VB.NET", "dotnet"),
    ]),
    ("FRONTEND + CREATIVE", [
        ("React", "react"), ("Three.js", "threejs"), ("Vite", "vite"), ("Phaser 3", "+phaser.png"),
        ("WebGL", "+webgl.svg"), ("OpenGL", "+opengl.svg"), ("PDF.js", "+pdfjs.svg"), ("Pygame", "+pygame.svg"),
    ]),
    ("BACKEND + DATABASES", [
        ("Node.js", "nodejs"), ("Express", "express"), ("Flask", "flask"), ("PostgreSQL", "postgres"),
        ("MySQL", "mysql"), ("Supabase", "supabase"), ("REST APIs", "~braces"), ("WebSockets", "+websocket.svg"), ("Colyseus", "+colyseus.svg"),
    ]),
    ("DATA + ML", [
        ("TensorFlow", "tensorflow"), ("PyTorch", "pytorch"), ("PySpark", "+spark.svg"), ("Pandas", "+pandas.svg"),
        ("NumPy", "+numpy.svg"), ("Spark MLlib", "+spark.svg"), ("Gymnasium", "+gymnasium.svg"),
    ]),
    ("DEV TOOLKIT", [
        ("Git", "git"), ("GitHub", "github"), ("Docker", "docker"), ("Linux", "linux"), ("GitLab CI", "gitlab"),
        ("Claude Code", "+claude.svg"), ("pthreads", "~spool"), ("Translation", "gcp"),
    ]),
]
# ─────────────────────────────────────────────────────────────────────────────

BG = "#171322"
PANEL = "#1F1A2E"
LINE = "#3A3150"
LILAC = "#B5A4DB"
PINK = "#D6A6BF"
PLUM = "#7D709C"
TEXT = "#E9E3F5"
MUTED = "#A99BBF"


# 16×16 pixel icons, only for concepts that have no logo of their own
PAL = {
    "w": "#F4F0FA", "l": LILAC, "p": PINK, "d": PLUM, "r": "#E5534B", "o": "#F0883E", "y": "#F2C94C",
    "g": "#57C785", "b": "#4F8FE6", "c": "#4FC3D9", "m": "#C65BCF", "s": "#8B8FA3", "k": "#0B0D14",
    "t": "#E3C79A", "u": "#A98559", "n": "#14111F",
}
ICONS = {
    "database": [
        "................", "....llllllll....", "..llwwwwwwwwll..", "..lwwwwwwwwwwl..", "..llwwwwwwwwll..",
        "..ddllllllllmm..", "..llddddddddll..", "..llllllllllll..", "..ddllllllllmm..", "..llddddddddll..",
        "..llllllllllll..", "..ddllllllllmm..", "..llddddddddll..", "..llllllllllll..", "....dddddddd....", "................",
    ],
    "braces": [
        "................", "....ppp..lll....", "...pp......ll...", "...pp......ll...", "...pp......ll...",
        "...pp......ll...", ".ppp..w.w...lll.", ".ppp..w.w...lll.", "...pp......ll...", "...pp......ll...",
        "...pp......ll...", "...pp......ll...", "....ppp..lll....", "................", "................", "................",
    ],
    "spool": [
        "................", "..uuuuuuuuuuuu..", "..tttttttttttt..", "....pppppppp....", "....llllllll....",
        "....pppppppp....", "....llllllll....", "....pppppppp....", "....llllllll....", "....pppppppp....",
        "....llllllll....", "..tttttttttttt..", "..uuuuuuuuuuuu..", "............p...", ".............ppp", "................",
    ],
}
for _name, _rows in ICONS.items():
    assert len(_rows) == 16 and all(len(r) == 16 for r in _rows), _name


def font(name, family):
    data = base64.b64encode((HERE / "fonts" / f"{name}.woff2").read_bytes()).decode()
    return f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{data}) format('woff2')}}"


FONTS = font("silkscreen", "Pixel") + font("spacemono", "Mono")
BASE_CSS = (
    FONTS
    + ".px{font-family:'Pixel',monospace}.mono{font-family:'Mono',monospace}"
    + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)

# 5×7 bitmap letters for the title
GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
}

# k = outline, l = lilac fur, p = pink, w = white
CAT_BODY = [
    "..k.......k.....",
    ".klk.....klk....",
    ".kllkkkkkllk....",
    ".kllllllllllk...",
    ".klwkllllkwlk...",
    ".kllllppllllk.kk",
    "..kllllllllkkkllk",
    "..kllllllllllkklk",
    "..kllllllllllk.kk",
]
CAT_LEGS_A = ["..kllkkkkllk.....", "..kk......kk....."]
CAT_LEGS_B = ["...kllk..kllk....", "....kk....kk....."]
CAT_SLEEP = [
    "....k.......k.......",
    "...klk.....klk......",
    "...kllkkkkkllk......",
    "..kllllllllllllkkk..",
    "..klkkkllkkkllllllk.",
    "..kllllppllllllllllk",
    "..kllllllllllllkkllk",
    "...kkkkkkkkkkkk..kk.",
]
STAR = ["..#..", ".###.", "#####", ".###.", "..#.."]
HEART = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
SWATCH = {"k": "#5A4C7C", "l": LILAC, "p": PINK, "w": "#FFFFFF", "#": PINK}


def pixels(rows, s, ox=0, oy=0, swatch=SWATCH):
    """Turns a sprite into one <path> per colour, so scaling never shows seams."""
    paths = {}
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            paths.setdefault(c, []).append(f"M{ox + x * s} {oy + y * s}h{run * s}v{s}h{-run * s}z")
            x += run
    return "".join(f'<path fill="{swatch[c]}" d="{"".join(d)}"/>' for c, d in paths.items())


def cat(s, ox=0, oy=0):
    """Walking cat: the legs swap between two frames via .fa/.fb."""
    body = pixels(CAT_BODY, s, ox, oy)
    legs_y = oy + len(CAT_BODY) * s
    return (
        body
        + f'<g class="fa">{pixels(CAT_LEGS_A, s, ox, legs_y)}</g>'
        + f'<g class="fb">{pixels(CAT_LEGS_B, s, ox, legs_y)}</g>'
    )


WALK_CSS = (
    ".fa{animation:fa .36s steps(1) infinite}.fb{animation:fb .36s steps(1) infinite}"
    "@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}"
)


def svg(name, w, h, css, body, title):
    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
        f"<style>{BASE_CSS}{css}</style>{body}</svg>"
    )
    (HERE / f"{name}.svg").write_text(out, encoding="utf-8")


def stars(rng, w, h, n, cls="tw"):
    out = []
    for _ in range(n):
        x, y = rng.randrange(0, w, 4), rng.randrange(0, h, 4)
        size = rng.choice([2, 2, 3, 4])
        color = rng.choice([LILAC, PINK, "#FFFFFF", PLUM])
        out.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" '
            f'style="animation-delay:-{rng.uniform(0, 4):.2f}s"/>'
        )
    return "".join(out)


def hills(rng, w, base, amp, step, color):
    """Stepped pixel terrain, in the spirit of the heightmap project."""
    d, x, y = [f"M0 {base + 120}V{base}"], 0, base
    while x < w:
        y = max(base - amp, min(base + amp // 2, y + rng.choice([-step, 0, 0, step])))
        d.append(f"V{y}H{x + step * 2}")
        x += step * 2
    d.append(f"V{base + 120}z")
    return f'<path fill="{color}" d="{"".join(d)}"/>'


def hero():
    rng = random.Random(19)
    W, H, S = 1200, 340, 15
    letters, x = [], 0
    for i, ch in enumerate("ABHA MAM"):
        if ch == " ":
            x += 3 * S
            continue
        t = i / 7
        color = "#%02X%02X%02X" % tuple(
            round(a + (b - a) * t) for a, b in zip((0xD6, 0xA6, 0xBF), (0xA0, 0x90, 0xD8))
        )
        shadow = pixels(GLYPHS[ch], S, x + 6, 6, {"#": "#3A2C57"})
        face = pixels(GLYPHS[ch], S, x, 0, {"#": color})
        letters.append(f'<g class="float" style="animation-delay:{i * 0.12:.2f}s">{shadow}{face}</g>')
        x += 6 * S
    title_w = x - S
    tx = (W - title_w) / 2
    css = (
        WALK_CSS
        + ".tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}"
        + ".float{animation:fl 2.6s ease-in-out infinite}@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}"
        + ".fill{animation:bar 7s steps(30) infinite}@keyframes bar{0%{transform:scaleX(0)}80%,100%{transform:scaleX(1)}}"
        + ".blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}"
        + ".walk{animation:walk 16s linear infinite}@keyframes walk{from{transform:translateX(-90px)}to{transform:translateX(1260px)}}"
        + ".scan{opacity:.05}"
    )
    body = (
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120E1C"/>'
        f'<stop offset=".65" stop-color="#231A38"/><stop offset="1" stop-color="#3A2A52"/></linearGradient>'
        f'<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000"/></pattern>'
        f'<clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>'
        f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#sky)"/>'
        + stars(rng, W, 250, 90)
        + hills(rng, W, 285, 34, 12, "#2C2342")
        + hills(rng, W, 312, 18, 12, "#1E1830")
        + f'<g transform="translate({tx} 46)">{"".join(letters)}</g>'
        + f'<g transform="translate({W / 2 - 200} 176)"><rect width="400" height="8" fill="{LINE}"/>'
        + f'<rect class="fill" width="400" height="8" fill="{LILAC}" style="transform-origin:0 0"/></g>'
        + f'<text class="px" x="{W / 2}" y="218" text-anchor="middle" font-size="20" fill="{MUTED}" letter-spacing="3">BUILD / EXPLORE / CREATE</text>'
        + f'<text class="px blink" x="{W / 2}" y="254" text-anchor="middle" font-size="15" fill="{PINK}" letter-spacing="2">- PRESS START -</text>'
        + f'<g class="walk"><g transform="translate(0 276)">{cat(3)}</g></g>'
        + f'<rect class="scan" width="{W}" height="{H}" fill="url(#sl)"/></g>'
    )
    svg("hero", W, H, css, body, "ABHA MAM: build, explore, create")


def character():
    W, H = 1000, 330
    bars = []
    for i, (label, val, color) in enumerate(STATS):
        y = 70 + i * 40
        bars.append(
            f'<text class="px" x="400" y="{y + 13}" font-size="15" fill="{TEXT}">{label}</text>'
            f'<rect x="560" y="{y}" width="340" height="16" fill="{BG}" stroke="{LINE}" stroke-width="2"/>'
            f'<rect class="grow" x="562" y="{y + 2}" width="{336 * val / 100:.0f}" height="12" fill="{color}" '
            f'style="animation-delay:{i * 0.18:.2f}s"/>'
            f'<text class="px" x="916" y="{y + 13}" font-size="15" fill="{MUTED}">{val}</text>'
        )
    y = 70 + len(STATS) * 40
    bars.append(
        f'<text class="px" x="400" y="{y + 13}" font-size="15" fill="{TEXT}">OPEN TABS</text>'
        f'<rect x="560" y="{y}" width="340" height="16" fill="{BG}" stroke="{PINK}" stroke-width="2"/>'
        f'<rect class="over" x="562" y="{y + 2}" width="336" height="12" fill="{PINK}"/>'
        f'<text class="px over" x="916" y="{y + 13}" font-size="15" fill="{PINK}">INF</text>'
    )
    info = [("PLAYER", "Abha Mam"), ("CLASS", "Creative Coder"), ("GUILD", "CS @ Penn State"), ("LEVEL", "always learning")]
    rows = "".join(
        f'<text class="px" x="44" y="{240 + i * 19}" font-size="12" fill="{PLUM}">{k}</text>'
        f'<text class="mono" x="118" y="{240 + i * 19}" font-size="14" fill="{TEXT}">{escape(v)}</text>'
        for i, (k, v) in enumerate(info)
    )
    css = (
        WALK_CSS.replace(".36s", ".7s")
        + ".grow{transform-box:fill-box;transform-origin:0 0;animation:grow 6s ease-out infinite}"
        + "@keyframes grow{0%{transform:scaleX(0)}22%,100%{transform:scaleX(1)}}"
        + ".over{animation:ov .9s steps(1) infinite}@keyframes ov{0%{opacity:1}50%{opacity:.45}}"
        + ".bob{animation:bob 1.4s steps(2) infinite}@keyframes bob{50%{transform:translateY(-6px)}}"
        + ".tw{animation:tw 3s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}"
    )
    rng = random.Random(4)
    body = (
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
        f'<rect x="28" y="28" width="330" height="186" rx="6" fill="{BG}" stroke="{LINE}" stroke-width="2"/>'
        f'<svg x="30" y="30" width="326" height="182">{stars(rng, 326, 182, 26)}</svg>'
        f'<g class="bob"><g transform="translate(112 62)">{cat(10)}</g></g>'
        f'<text class="px" x="400" y="44" font-size="15" fill="{LILAC}" letter-spacing="2">CHARACTER SHEET</text>'
        + "".join(bars)
        + rows
    )
    svg("character", W, H, css, body, "Character sheet: curiosity 99, chaos 87, clean code 74, debugging 68, sleep 12, open tabs infinite")


def divider(name, sprite, s, dur, reverse=False):
    W, H = 1200, 34
    frm, to = (1230, -50) if reverse else (-50, 1230)
    css = (
        WALK_CSS
        + f".go{{animation:go {dur}s linear infinite}}@keyframes go{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}"
    )
    gid = "g"
    if sprite == "cat":
        art = cat(s)
        y = 0
    else:
        art = pixels(sprite, s)
        y = 17 - len(sprite) * s // 2
    flip = ' transform="scale(-1 1)"' if reverse else ""
    body = (
        f'<defs><linearGradient id="{gid}"><stop offset="0" stop-color="{LILAC}"/><stop offset=".5" stop-color="{PINK}"/>'
        f'<stop offset="1" stop-color="{PLUM}"/></linearGradient></defs>'
        f'<rect y="28" width="{W}" height="3" fill="url(#{gid})"/>' if sprite == "cat" else
        f'<defs><linearGradient id="{gid}"><stop offset="0" stop-color="{LILAC}"/><stop offset=".5" stop-color="{PINK}"/>'
        f'<stop offset="1" stop-color="{PLUM}"/></linearGradient></defs>'
        f'<rect y="16" width="{W}" height="3" fill="url(#{gid})"/>'
    )
    body += f'<g class="go"><g transform="translate(0 {y})"><g{flip}>{art}</g></g></g>'
    svg(name, W, H, css, body, "")


def icon(kind):
    """Each icon is drawn inside a 100×100 box at the card's top right."""
    if kind == "shell":
        return (
            f'<rect x="4" y="14" width="92" height="72" rx="6" fill="{BG}" stroke="{LILAC}" stroke-width="3"/>'
            f'<text class="px" x="16" y="48" font-size="20" fill="{PINK}">$</text>'
            f'<rect class="blink" x="38" y="34" width="12" height="16" fill="{LILAC}"/>'
            f'<rect x="16" y="62" width="50" height="4" fill="{PLUM}"/>'
        )
    if kind == "terrain":
        rng = random.Random(7)
        bars = "".join(
            f'<rect class="wave" x="{4 + i * 12}" y="{44}" width="10" height="46" fill="{c}" '
            f'style="animation-delay:{i * 0.14:.2f}s;transform-origin:{9 + i * 12}px 90px"/>'
            for i, c in enumerate([PLUM, LILAC, PINK, LILAC, PLUM, LILAC, PINK, PLUM])
        )
        return bars
    if kind == "merge":
        return (
            f'<path d="M28 18V82M28 34C28 60 72 44 72 66" fill="none" stroke="{LILAC}" stroke-width="5"/>'
            f'<rect x="19" y="10" width="18" height="18" fill="{PINK}"/><rect x="19" y="74" width="18" height="18" fill="{LILAC}"/>'
            f'<rect class="pulse" x="63" y="60" width="18" height="18" fill="{PINK}"/>'
        )
    if kind == "boba":
        pearls = "".join(
            f'<rect class="rise" x="{x}" y="72" width="9" height="9" fill="#2B2038" style="animation-delay:{d}s"/>'
            for x, d in [(32, 0), (46, 0.5), (60, 1.0), (39, 1.5), (54, 0.8)]
        )
        return (
            f'<path d="M24 26H76L68 90H32z" fill="#E7C8B0" stroke="{TEXT}" stroke-width="3"/>{pearls}'
            f'<rect x="18" y="18" width="64" height="9" fill="{LILAC}"/><rect x="56" y="0" width="7" height="30" fill="{PINK}" transform="rotate(10 59 15)"/>'
        )
    if kind == "stars":
        art = []
        for i in range(5):
            cls = "star0" if i == 0 else f'star" style="animation-delay:{i * 0.7:.1f}s'
            art.append(f'<g transform="translate({i * 20} 40)"><g class="{cls}">{pixels(STAR, 3.4, swatch={"#": PINK})}</g></g>')
        return "".join(art)
    if kind == "crosshair":
        return (
            f'<g class="spin" style="transform-origin:50px 50px"><rect x="47" y="8" width="6" height="26" fill="{PINK}"/>'
            f'<rect x="47" y="66" width="6" height="26" fill="{PINK}"/><rect x="8" y="47" width="26" height="6" fill="{PINK}"/>'
            f'<rect x="66" y="47" width="26" height="6" fill="{PINK}"/></g>'
            f'<rect class="blink" x="46" y="46" width="8" height="8" fill="{LILAC}"/>'
        )
    return ""


def card(c):
    W, H = 440, 210
    chips, x = [], 24
    for s in c["stack"]:
        w = len(s) * 8.4 + 18
        chips.append(
            f'<rect x="{x}" y="164" width="{w:.0f}" height="24" rx="3" fill="{BG}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<text class="mono" x="{x + w / 2:.0f}" y="181" text-anchor="middle" font-size="13" fill="{LILAC}">{escape(s)}</text>'
        )
        x += w + 8
    lines = "".join(
        f'<text class="mono" x="24" y="{112 + i * 21}" font-size="14" fill="{MUTED}">{escape(t)}</text>'
        for i, t in enumerate(c["lines"])
    )
    css = (
        ".blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}"
        ".wave{animation:wv 1.7s ease-in-out infinite}@keyframes wv{0%,100%{transform:scaleY(.45)}50%{transform:scaleY(1)}}"
        ".pulse{animation:pl 1.4s steps(2) infinite}@keyframes pl{50%{opacity:.35}}"
        ".rise{animation:rs 2.4s ease-in-out infinite}@keyframes rs{0%,100%{transform:translateY(0)}50%{transform:translateY(-22px)}}"
        ".star{opacity:.15;animation:st 5s steps(1) infinite}@keyframes st{0%,20%{opacity:.15}21%,88%{opacity:1}89%{opacity:.15}}"
        ".spin{animation:sp 4s steps(8) infinite}@keyframes sp{to{transform:rotate(360deg)}}"
    )
    body = (
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
        f'<rect x="1" y="16" width="5" height="44" fill="{PINK}"/>'
        f'<text class="px" x="24" y="38" font-size="12" fill="{PINK}" letter-spacing="1.5">{escape(c["kind"])}</text>'
        f'<text class="px" x="24" y="70" font-size="24" fill="{TEXT}">{escape(c["title"])}</text>'
        f'{lines}{"".join(chips)}'
        f'<g transform="translate(344 16) scale(.72)">{icon(c["icon"])}</g>'
    )
    svg(c["file"], W, H, css, body, f'{c["title"]}: {" ".join(c["lines"])}')


def quests():
    W, H = 1000, 300
    rows = []
    for i, (name, status) in enumerate(QUESTS):
        y = 88 + i * 34
        failed = status == "FAILED"
        color = PINK if failed else LILAC
        rows.append(
            f'<g class="in" style="animation-delay:{i * 0.45:.2f}s">'
            f'<rect x="40" y="{y - 11}" width="11" height="11" fill="{"none" if failed else LILAC}" stroke="{color}" stroke-width="2"/>'
            f'<text class="mono" x="66" y="{y}" font-size="17" fill="{TEXT}">{escape(name)}</text>'
            f'<text class="px{" fail" if failed else ""}" x="958" y="{y}" text-anchor="end" font-size="16" fill="{color}">{status}</text></g>'
        )
    css = (
        ".in{animation:in 11s steps(1) infinite;opacity:0}@keyframes in{0%{opacity:1}96%{opacity:1}97%,100%{opacity:0}}"
        ".fail{animation:fl .7s steps(1) infinite}@keyframes fl{0%{opacity:1}50%{opacity:.3}}"
        ".blink{animation:bl 1.1s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}"
        "@media (prefers-reduced-motion:reduce){.in{opacity:1}}"
    )
    body = (
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
        f'<text class="px" x="40" y="44" font-size="16" fill="{LILAC}" letter-spacing="2">QUEST LOG</text>'
        f'<text class="px" x="958" y="44" text-anchor="end" font-size="16" fill="{LILAC}" letter-spacing="2">STATUS</text>'
        f'<rect x="40" y="56" width="920" height="2" fill="{LINE}"/>'
        + "".join(rows)
        + f'<rect x="40" y="252" width="920" height="2" fill="{LINE}"/>'
        f'<text class="px" x="40" y="280" font-size="14" fill="{MUTED}">CURRENT LEVEL: always learning</text>'
        f'<rect class="blink" x="330" y="268" width="9" height="13" fill="{PINK}"/>'
    )
    svg("quests", W, H, css, body, "Quest log: four active quests and one failed: stop opening new browser tabs")


def footer():
    rng = random.Random(23)
    W, H = 1200, 170
    css = (
        ".tw{animation:tw 3.2s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}"
        ".breathe{transform-box:fill-box;transform-origin:50% 100%;animation:br 3s ease-in-out infinite}@keyframes br{50%{transform:scaleY(.93)}}"
        ".z{animation:z 3.6s linear infinite;opacity:0}@keyframes z{0%{opacity:0;transform:translate(0,0)}25%{opacity:1}100%{opacity:0;transform:translate(26px,-46px)}}"
        ".blink{animation:bl 1.4s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:.25}}"
    )
    zs = "".join(
        f'<text class="px z" x="704" y="96" font-size="{13 + i * 4}" fill="{PINK}" style="animation-delay:{i * 1.2:.1f}s">z</text>'
        for i in range(3)
    )
    body = (
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120E1C"/>'
        f'<stop offset="1" stop-color="#3A2A52"/></linearGradient><clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>'
        f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#sky)"/>'
        + stars(rng, W, 110, 60)
        + hills(rng, W, 138, 12, 12, "#2C2342")
        + f'<text class="px blink" x="{W / 2}" y="54" text-anchor="middle" font-size="22" fill="{LILAC}" letter-spacing="3">GAME SAVED</text>'
        + f'<g class="breathe"><g transform="translate(540 88)">{pixels(CAT_SLEEP, 5)}</g></g>{zs}</g>'
    )
    svg("footer", W, H, css, body, "Game saved. A pixel cat sleeps on a hill.")


def inventory():
    W, PER_ROW, SLOT, PITCH_X, PITCH_Y, LEFT = 1000, 9, 54, 90, 86, 172
    TILE = [LILAC, PINK, "#9D8FC4", "#C8A9D6", PINK]
    shelves, y, total = [], 62, 0
    for s, (name, items) in enumerate(INVENTORY):
        rows = (len(items) + PER_ROW - 1) // PER_ROW
        words = name.split(" + ")
        head = "".join(
            f'<text class="px" x="32" y="{y + 38 + i * 19 - (len(words) - 1) * 9}" font-size="14" fill="{TEXT}">'
            f'{"+ " if i else ""}{escape(w)}</text>'
            for i, w in enumerate(words)
        ) if len(name) > 14 else f'<text class="px" x="32" y="{y + 38}" font-size="14" fill="{TEXT}">{escape(name)}</text>'
        shelves.append(
            f'<rect x="20" y="{y + 8}" width="4" height="{rows * PITCH_Y - 22}" fill="{TILE[s]}"/>{head}'
            f'<text class="mono" x="32" y="{y + 66}" font-size="11" fill="{PLUM}">{len(items)} items</text>'
        )
        for i, (label, art) in enumerate(items):
            x, sy = LEFT + (i % PER_ROW) * PITCH_X + 18, y + (i // PER_ROW) * PITCH_Y + 2
            slot = (
                f'<rect x="{x}" y="{sy}" width="{SLOT}" height="{SLOT}" rx="6" fill="{BG}" stroke="{LINE}" stroke-width="2"/>'
            )
            if art.startswith("~"):
                slot += (
                    f'<rect x="{x + 6}" y="{sy + 6}" width="42" height="42" rx="10" fill="#242938"/>'
                    f'<g shape-rendering="crispEdges">{pixels(ICONS[art[1:]], 2.5, x + 7, sy + 7, PAL)}</g>'
                )
            elif art.startswith("+"):
                file = art[1:]
                mime = "image/png" if file.endswith(".png") else "image/svg+xml"
                data = base64.b64encode((HERE / "icons" / file).read_bytes()).decode()
                slot += (
                    f'<rect x="{x + 6}" y="{sy + 6}" width="42" height="42" rx="10" fill="#242938"/>'
                    f'<image x="{x + 10}" y="{sy + 10}" width="34" height="34" href="data:{mime};base64,{data}"/>'
                )
            else:
                data = base64.b64encode((HERE / "icons" / f"{art}.svg").read_bytes()).decode()
                slot += f'<image x="{x + 6}" y="{sy + 6}" width="42" height="42" href="data:image/svg+xml;base64,{data}"/>'
            slot += (
                f'<text class="mono" x="{x + SLOT / 2}" y="{sy + SLOT + 16}" text-anchor="middle" font-size="11.5" fill="{MUTED}">{escape(label)}</text>'
            )
            shelves.append(slot)
            total += 1
        y += rows * PITCH_Y
        if s < len(INVENTORY) - 1:
            shelves.append(f'<rect x="20" y="{y - 6}" width="{W - 40}" height="2" fill="{LINE}" opacity=".6"/>')
            y += 8
    H = y + 34
    body = (
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
        f'<text class="px" x="32" y="38" font-size="16" fill="{LILAC}" letter-spacing="2">INVENTORY</text>'
        f'<text class="px" x="{W - 32}" y="38" text-anchor="end" font-size="13" fill="{MUTED}" letter-spacing="1">{total} ITEMS / WEIGHT: UNREASONABLE</text>'
        f'<rect x="20" y="50" width="{W - 40}" height="2" fill="{LINE}"/>'
        + "".join(shelves)
    )
    alt = "Inventory. " + " ".join(f'{n.title()}: {", ".join(l for l, _ in it)}.' for n, it in INVENTORY)
    svg("inventory", W, H, "", body, alt)


hero()
character()
divider("divider-cat", "cat", 2, 22)
divider("divider-star", STAR, 3, 26, reverse=True)
divider("divider-heart", HEART, 3, 24)
for c in CARDS:
    card(c)
quests()
inventory()
footer()
