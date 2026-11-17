#!/usr/bin/env python3
"""Builds the Cut Cut Cut website into docs/ (plain files, no server needed; GitHub Pages can serve docs/).

    python3 build.py

Only the Python standard library is used. What it reads:
  content/site.json        name, tagline, navigation, base URL
  content/pages/*.html     the fixed pages (first line: <!-- title | description | optional body class -->)
  content/posts/*.md       dev log posts (front matter between --- lines, then a small Markdown, see md())
  content/timeline.json    the dated timeline
  content/cast.json        the people of the tower
  content/media.json       the video shelf and the gallery
  static/                  style.css, site.js (copied as they are)
Media (docs/media) is made by tools/prep-media.sh and tools/prep-images.py and is not touched here.
"""
import hashlib, html, json, os, re, shutil, datetime
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
C = ROOT / "content"
SITE = json.loads((C / "site.json").read_text())
MONTHS = "January February March April May June July August September October November December".split()


def esc(s): return html.escape(str(s), quote=True)


def stamp(name):
    """A short fingerprint of a static file, added to its address (style.css?v=...), so browsers fetch the new one
    when it changes instead of showing new pages with an old cached stylesheet."""
    return hashlib.sha1((ROOT / "static" / name).read_bytes()).hexdigest()[:8]
DAY_ONE = datetime.date(2026, 11, 13)  # the first night of the project


def nice_date(d):
    """The site counts in days of work, not calendar dates: 2026-11-13 is "Day 1"."""
    y, m, dd = (int(x) for x in d.split("-"))
    return f"Day {(datetime.date(y, m, dd) - DAY_ONE).days + 1}"


# ---------------------------------------------------------------- media blocks
def video(name, caption="", portrait=False, root=""):
    cls = "video portrait" if portrait else "video"
    cap = f"<figcaption>{inline(caption, root)}</figcaption>" if caption else ""
    return (f'<figure class="{cls}"><video controls preload="none" playsinline poster="{root}media/video/{name}.jpg">'
            f'<source src="{root}media/video/{name}.mp4" type="video/mp4"></video>{cap}</figure>')


def image(name, caption="", root="", cls="shot"):
    ext = "png" if name == "logo" else "jpg"
    cap = f"<figcaption>{inline(caption, root)}</figcaption>" if caption else ""
    return (f'<figure class="{cls}"><a class="zoom" href="{root}media/img/{name}.{ext}"><img loading="lazy" src="{root}media/img/{name}.{ext}" '
            f'alt="{esc(re.sub("<[^>]+>", "", caption) or name)}"></a>{cap}</figure>')


def gallery(names, root=""):
    return '<div class="gallery">' + "".join(image(n, "", root, "tile") for n in names) + "</div>"


# ---------------------------------------------------------------- a small Markdown
def inline(s, root=""):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<em>\1</em>", s)
    def link(m):
        url = m.group(2)
        if not re.match(r"^(https?:|mailto:|#)", url): url = root + url
        return f'<a href="{url}">{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)


def md(text, root=""):
    """Headings (## and ###), paragraphs, - lists, > quotes, **bold**, *italic*, `code`, [links](url), and three blocks:
         ::video name | caption            (add "| portrait" for a vertical video)
         ::img name | caption
         ::gallery name name name"""
    out, para, items, quote = [], [], [], []
    def flush():
        nonlocal para, items, quote
        if para: out.append("<p>" + inline(" ".join(para), root) + "</p>"); para = []
        if items: out.append("<ul>" + "".join(f"<li>{inline(i, root)}</li>" for i in items) + "</ul>"); items = []
        if quote: out.append("<blockquote><p>" + inline(" ".join(quote), root) + "</p></blockquote>"); quote = []
    for line in text.strip().split("\n"):
        s = line.strip()
        if not s: flush(); continue
        if s.startswith("::"):
            flush()
            kind, _, rest = s[2:].partition(" ")
            parts = [p.strip() for p in rest.split("|")]
            if kind == "video": out.append(video(parts[0], parts[1] if len(parts) > 1 else "", "portrait" in parts[2:], root))
            elif kind == "img": out.append(image(parts[0], parts[1] if len(parts) > 1 else "", root))
            elif kind == "gallery": out.append(gallery(rest.split(), root))
            continue
        if s.startswith("### "): flush(); out.append(f"<h3>{inline(s[4:], root)}</h3>"); continue
        if s.startswith("## "): flush(); out.append(f"<h2>{inline(s[3:], root)}</h2>"); continue
        if s.startswith("- "):
            if para or quote: flush()
            items.append(s[2:]); continue
        if s.startswith("> "):
            if para or items: flush()
            quote.append(s[2:]); continue
        if items or quote: flush()
        para.append(s)
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------- posts
def load_posts():
    posts = []
    for f in sorted((C / "posts").glob("*.md")):
        raw = f.read_text()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m: raise SystemExit(f"{f.name}: missing front matter")
        meta = {}
        for line in m.group(1).split("\n"):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        for need in ("title", "date", "summary"):
            if need not in meta: raise SystemExit(f"{f.name}: front matter needs '{need}'")
        meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", f.stem)
        meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        meta["body"] = m.group(2)
        meta["sort"] = meta["date"] + " " + meta.get("time", "12:00")
        posts.append(meta)
    return sorted(posts, key=lambda p: p["sort"], reverse=True)


def post_card(p, root):
    cover = p.get("cover")
    is_video = cover and (OUT / "media" / "video" / f"{cover}.jpg").exists()
    src = f"{root}media/video/{cover}.jpg" if is_video else f"{root}media/img/{cover}.jpg"
    thumb = f'<div class="thumb{" play" if is_video else ""}"><img loading="lazy" src="{src}" alt=""></div>' if cover else ""
    tags = "".join(f"<span>{esc(t)}</span>" for t in p["tags"][:3])
    return (f'<a class="card" href="{root}devlog/{p["slug"]}.html">{thumb}<div class="card-body"><time datetime="{p["date"]}">{nice_date(p["date"])}</time>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p><div class="tags">{tags}</div></div></a>')


# ---------------------------------------------------------------- page shell
def layout(title, description, body, root="", page="", body_class="", og=None):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{root}{n["href"]}"{cur if n["id"] == page else ""}>{esc(n["label"])}</a>' for n in SITE["nav"])
    full = f"{title} · {SITE['name']}" if title else f"{SITE['name']}: {SITE['tagline']}"
    og_img = SITE["url"].rstrip("/") + "/" + (og or "media/img/social.jpg")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}media/img/icon-48.png">
<link rel="apple-touch-icon" href="{root}media/img/icon-180.png">
<link rel="alternate" type="application/rss+xml" title="{esc(SITE['name'])} dev log" href="{root}feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css?v={stamp("style.css")}">
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="{root}index.html" aria-label="{esc(SITE['name'])} home"><img src="{root}media/img/logo.png" alt="{esc(SITE['name'])}"></a>
  <button class="menu" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <nav class="nav">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="foot-in">
    <img src="{root}media/img/logo.png" alt="" class="foot-logo">
    <p>{esc(SITE['name'])}: {esc(SITE['tagline'])}. An isometric sword game for iPhone, in development.</p>
    <nav>{nav}<a href="{root}feed.xml">RSS</a></nav>
    <p class="small">The residents prefer the term "undying". Rin does not. &copy; {datetime.date.today().year} {esc(SITE['owner'])}. Game art and footage are work in progress.</p>
  </div>
</footer>
<div class="lightbox" hidden><button aria-label="Close">&times;</button><img alt=""></div>
<script src="{root}site.js?v={stamp("site.js")}" defer></script>
</body>
</html>
"""


def write(path, text):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


# ---------------------------------------------------------------- blocks pages can ask for:  {{name}}
def blocks(root, posts):
    cast = json.loads((C / "cast.json").read_text())
    timeline = json.loads((C / "timeline.json").read_text())
    media = json.loads((C / "media.json").read_text())
    def cast_grid(people):
        return '<div class="cast">' + "".join(
            f'<article class="person"><a class="zoom" href="{root}media/img/cast-{p["img"]}.jpg"><img loading="lazy" src="{root}media/img/cast-{p["img"]}.jpg" alt="{esc(p["name"])}"></a>'
            f'<div><span class="floor">{esc(p["where"])}</span><h3>{esc(p["name"])}</h3><p class="role">{esc(p["role"])}</p><p>{inline(p["text"], root)}</p></div></article>' for p in people) + "</div>"
    def tl(items):
        rows = []
        for day in items:
            ev = "".join(f'<li><div><strong>{inline(e["title"], root)}</strong>'
                         + (f'<p>{inline(e["text"], root)}</p>' if e.get("text") else "")
                         + (f'<a class="more" href="{root}{e["link"]}">{esc(e.get("link_text", "Read the post"))}</a>' if e.get("link") else "") + "</div></li>" for e in day["events"])
            rows.append(f'<section class="day"><header><h2>{nice_date(day["date"])}</h2><span class="stamp">{esc(day["label"])}</span><p>{inline(day["summary"], root)}</p></header><ol>{ev}</ol></section>')
        return '<div class="timeline">' + "".join(rows) + "</div>"
    def shelf(vs):
        return '<div class="shelf">' + "".join(
            f'<article class="{"wide " if v.get("wide") else ""}{"tall " if v.get("portrait") else ""}reel">{video(v["name"], "", v.get("portrait", False), root)}'
            f'<div><time>{nice_date(v["date"])}</time><h3>{esc(v["title"])}</h3><p>{inline(v["text"], root)}</p></div></article>' for v in vs) + "</div>"
    b = {
        "latest_posts": '<div class="cards">' + "".join(post_card(p, root) for p in posts[:3]) + "</div>",
        "all_posts": '<div class="cards">' + "".join(post_card(p, root) for p in posts) + "</div>",
        "cast_main": cast_grid([p for p in cast if p.get("group") == "main"]),
        "cast_guardians": cast_grid([p for p in cast if p.get("group") == "guardian"]),
        "cast_expedition": cast_grid([p for p in cast if p.get("group") == "expedition"]),
        "timeline": tl(timeline),
        "timeline_short": tl(timeline[-2:]),
        "post_count": str(len(posts)),
    }
    # the rotating reel of real play: one silent video element that site.js feeds the clips to, one after another
    clips = media.get("reel", [])
    if clips:
        dots = "".join(f'<button type="button" data-i="{i}" aria-label="{esc(c["label"])}"></button>' for i, c in enumerate(clips))
        data = esc(json.dumps([{"src": f'{root}media/reel/{c["name"]}.mp4', "poster": f'{root}media/reel/{c["name"]}.jpg', "label": c["label"]} for c in clips]))
        b["reel"] = (f'<div class="reel-player" data-clips="{data}"><div class="reel-screen"><video muted playsinline preload="metadata" poster="{root}media/reel/{clips[0]["name"]}.jpg" '
                     f'src="{root}media/reel/{clips[0]["name"]}.mp4"></video><span class="reel-live">Development footage</span></div>'
                     f'<div class="reel-bar"><button type="button" class="reel-prev" aria-label="Previous clip">&lsaquo;</button><p class="reel-label">{esc(clips[0]["label"])}</p>'
                     f'<div class="reel-dots">{dots}</div><button type="button" class="reel-next" aria-label="Next clip">&rsaquo;</button></div></div>')
    for key, vs in media["shelves"].items(): b["shelf_" + key] = shelf(vs)
    for key, names in media["galleries"].items(): b["gallery_" + key] = gallery(names, root)
    return b


def fill(text, root, posts):
    b = blocks(root, posts)
    text = re.sub(r"\{\{video ([\w-]+)(?: \| ([^}|]*))?( \| portrait)?\}\}", lambda m: video(m.group(1), m.group(2) or "", bool(m.group(3)), root), text)
    text = re.sub(r"\{\{img ([\w-]+)(?: \| ([^}]*))?\}\}", lambda m: image(m.group(1), m.group(2) or "", root), text)
    def rep(m):
        if m.group(1) not in b: raise SystemExit(f"unknown block {{{{{m.group(1)}}}}}")
        return b[m.group(1)]
    return re.sub(r"\{\{(\w+)\}\}", rep, text).replace("{root}", root)


def main():
    OUT.mkdir(exist_ok=True)
    for f in (ROOT / "static").iterdir(): shutil.copy(f, OUT / f.name)
    (OUT / ".nojekyll").write_text("")
    posts = load_posts()
    # fixed pages
    for f in sorted((C / "pages").glob("*.html")):
        raw = f.read_text()
        head, _, body = raw.partition("\n")
        m = re.match(r"<!--\s*(.*?)\s*-->", head)
        if not m: raise SystemExit(f"{f.name}: first line must be <!-- title | description | body class -->")
        parts = [p.strip() for p in m.group(1).split("|")] + ["", ""]
        name = f.stem
        root = "../" if name == "devlog" else ""
        path = "devlog/index.html" if name == "devlog" else f"{name}.html"
        write(path, layout(parts[0], parts[1], fill(body, root, posts), root, name, parts[2]))
    # posts
    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        tags = "".join(f"<span>{esc(t)}</span>" for t in p["tags"])
        nav = '<nav class="post-nav">' + (f'<a class="older" href="{older["slug"]}.html"><span>Earlier</span>{esc(older["title"])}</a>' if older else "<span></span>") \
            + (f'<a class="newer" href="{newer["slug"]}.html"><span>Later</span>{esc(newer["title"])}</a>' if newer else "<span></span>") + "</nav>"
        body = (f'<article class="post"><header class="post-head"><a class="back" href="index.html">Dev log</a>'
                f'<h1>{esc(p["title"])}</h1><p class="lede">{esc(p["summary"])}</p>'
                f'<div class="meta"><time datetime="{p["date"]}">{nice_date(p["date"])}</time><div class="tags">{tags}</div></div></header>'
                f'<div class="prose">{md(p["body"], "../")}</div>{nav}</article>')
        cover = p.get("cover")
        og = None
        if cover: og = f"media/video/{cover}.jpg" if (OUT / "media" / "video" / f"{cover}.jpg").exists() else f"media/img/{cover}.jpg"
        write(f"devlog/{p['slug']}.html", layout(p["title"], p["summary"], body, "../", "devlog", "page-post", og))
    # feed and sitemap
    base = SITE["url"].rstrip("/")
    items = "".join(f"<item><title>{esc(p['title'])}</title><link>{base}/devlog/{p['slug']}.html</link><guid>{base}/devlog/{p['slug']}.html</guid>"
                    f"<pubDate>{datetime.datetime.strptime(p['sort'], '%Y-%m-%d %H:%M').strftime('%a, %d %b %Y %H:%M:00 +0700')}</pubDate><description>{esc(p['summary'])}</description></item>" for p in posts)
    write("feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(SITE["name"])} dev log</title><link>{base}/</link>'
                      f'<description>{esc(SITE["tagline"])}</description>{items}</channel></rss>')
    urls = [f"{base}/{f.stem}.html" for f in (C / "pages").glob("*.html") if f.stem not in ("devlog", "404")] + [f"{base}/devlog/"] + [f"{base}/devlog/{p['slug']}.html" for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>")
    # every local link and media file a page points at must exist
    missing = set()
    for f in OUT.rglob("*.html"):
        for m in re.finditer(r'(?:href|src|poster)="([^"#]+)"', f.read_text()):
            u = m.group(1)
            if re.match(r"^(https?:|mailto:|data:)", u): continue
            if not (f.parent / u.split("?")[0]).resolve().exists(): missing.add(f"{f.relative_to(OUT)} -> {u}")
    print(f"built {len(posts)} posts, {len(list(OUT.rglob('*.html')))} pages")
    if missing: print("MISSING:\n  " + "\n  ".join(sorted(missing)))


if __name__ == "__main__":
    main()
