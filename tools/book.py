#!/usr/bin/env python3
"""Turn pandoc's HTML of one issue into the PDFs of one edition (run by make.sh).

    book.py WORKDIR ISSUEDIR EDITION OUTDIR

EDITION is letter or half. WORKDIR holds issue.html (pandoc's fragment,
--section-divs, tools/zine.lua) and the stylesheets; ISSUEDIR holds
issue.md, whose YAML front matter supplies the cover and the folios, and
the pictures (paths in the Markdown are relative to it). $CHROME is the
browser.

Writes into OUTDIR, with NAME = the issue folder's name:
  letter: NAME-letter.pdf                 cover, pages, back cover; 8.5 x 11 in,
                                          links and bookmarks live: for reading
          NAME-letter-print-interior.pdf  the pages with 0.125 in bleed and
                                          TrimBox/BleedBox set, a multiple of 4
                                          pages (saddle stitch): for Lulu etc.
          NAME-letter-print-cover.pdf     back | spine | front on one sheet with
                                          bleed; $SPINE (inches, default 0, the
                                          saddle-stitch case) widens the spine
                                          for a perfect-bound printing
  half:   NAME-half-letter.pdf            5.5 x 8.5 in, for reading
          NAME-half-saddle-stitch-letter.pdf
                                          the same as a booklet imposed two up
                                          on letter landscape: print double-
                                          sided, flip on the short edge, fold,
                                          staple on the fold

The contents page is built here: every level-1 section gets a line (page,
kicker, title). Chrome can't number pages into the text, so the pages are
printed twice: the first print says where each section starts (its named
destination), the second has those numbers in the contents, and is checked.
"""
import datetime, html, os, re, subprocess, sys
import pypdf
import yaml
from fontTools.ttLib import TTFont

work, issue_dir, edition, out_dir = sys.argv[1:5]
issue_dir = os.path.abspath(issue_dir)
out_dir = os.path.abspath(out_dir)
os.chdir(work)
NAME = os.path.basename(issue_dir.rstrip("/"))
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FONTS = os.path.join(REPO, "fonts")

EDITIONS = {   # trim (in), bleed (in), cover unit (in)
    "letter": dict(w=8.5, h=11.0, bleed=0.125, u=1.0),
    "half":   dict(w=5.5, h=8.5, bleed=0.0, u=5.5 / 8.5),
}
E = EDITIONS[edition]
W, H, B, U = E["w"], E["h"], E["bleed"], E["u"]
PT = 72


def die(msg):
    sys.exit("book.py: " + msg)


# --- the issue's front matter -------------------------------------------
src = open(os.path.join(issue_dir, "issue.md"), encoding="utf-8").read()
m = re.match(r"(?s)^---\n(.*?)\n(---|\.\.\.)\n", src)
if not m:
    die("issue.md has no YAML front matter (--- ... ---)")
meta = yaml.safe_load(m.group(1)) or {}
for key in ("series", "number", "cover_line", "cover"):
    if key not in meta:
        die("front matter needs '%s'" % key)
SERIES = str(meta["series"])
NO = "%02d" % int(meta["number"])
YEAR = str(meta.get("year", datetime.date.today().year))
PUBLISHER = str(meta.get("publisher", ""))
TITLE = "%s No. %s: %s" % (SERIES, NO, meta["cover_line"])


def esc(s):
    return html.escape(str(s), quote=True)


def css_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def fill(name, bleed):
    t = open(os.path.join(REPO, "style", name), encoding="utf-8").read()
    t = (t.replace("{{FONTS}}", "file://" + FONTS)
          .replace("{{SERIES}}", css_str(SERIES.upper()))
          .replace("{{NO}}", NO)
          .replace("{{BLEED}}", "%gin" % bleed))
    open(name, "w", encoding="utf-8").write(t)


for f in ("base.css", edition + ".css", "cover.css"):
    fill(f, B)


def chrome(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    subprocess.run([os.environ["CHROME"], "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--allow-file-access-from-files", "--no-pdf-header-footer",
                    "--print-to-pdf=" + dst, "file://" + os.path.abspath(src)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if not (os.path.exists(dst) and os.path.getsize(dst)):
        die("Chrome produced no " + dst)


def head(title, css, extra=""):
    links = "".join('<link rel="stylesheet" href="file://%s">' % os.path.abspath(c) for c in css)
    return ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><base href="file://%s/">%s'
            '<title>%s</title>%s</head>' % (esc(meta.get("lang", "en")), issue_dir, links, esc(title), extra))


# --- the pages ----------------------------------------------------------
body = open("issue.html", encoding="utf-8").read()
sections = []
for sm in re.finditer(r'<section id="([^"]+)" class="level1[^"]*"([^>]*)>\s*<h1([^>]*)>(.*?)</h1>', body, re.S):
    kick = re.search(r'data-kicker="([^"]*)"', sm.group(2) + sm.group(3))
    sections.append(dict(id=sm.group(1), kicker=html.unescape(kick.group(1)) if kick else "",
                         title=sm.group(4)))
if not sections:
    die("the issue has no level-1 headings (# Title)")

# The editor's letter goes on the contents page, under the contents.
letter = ""
lm = re.search(r'(?s)<div class="letter"[^>]*>.*?</div>\s*(?=<section|<div class="contents"|$)', body)
if lm:
    letter, body = lm.group(0), body.replace(lm.group(0), "", 1)


def contents(pages):
    rows = "".join(
        '<a href="#%s"><span class="pg">%s</span><span class="k">%s</span><span class="t">%s</span></a>'
        % (s["id"], pages.get(s["id"], "00"), esc(s["kicker"]), s["title"]) for s in sections)
    return ('<div class="contents"><div class="kicker">Contents</div>'
            '<nav class="toc">%s</nav>%s</div>' % (rows, letter))


def build(pages):
    b = re.sub(r'(?s)<div class="contents">.*?</div>', "", body)   # a placeholder is optional
    return (head(TITLE, ["base.css", edition + ".css"],
                 "")
            + "<body>" + contents(pages) + b + "</body></html>")


def starts_of(pdf):
    r = pypdf.PdfReader(pdf)
    d = {k.lstrip("/"): r.get_destination_page_number(v) + 1 for k, v in r.named_destinations.items()}
    missing = [s["id"] for s in sections if s["id"] not in d]
    if missing:
        die("no destination for %s" % missing)
    return {s["id"]: d[s["id"]] for s in sections}, r


open("book.html", "w", encoding="utf-8").write(build({}))
chrome("book.html", "pass1.pdf")
pages, _ = starts_of("pass1.pdf")
open("book.html", "w", encoding="utf-8").write(build(pages))
chrome("book.html", "body.pdf")
got, body_reader = starts_of("body.pdf")
if got != pages:
    die("the contents moved the sections: %s, then %s" % (pages, got))
n_body = len(body_reader.pages)
pw, ph = (W + 2 * B) * PT, (H + 2 * B) * PT
p0 = body_reader.pages[0]
if abs(float(p0.mediabox.width) - pw) > 1 or abs(float(p0.mediabox.height) - ph) > 1:
    die("pages are %.1f x %.1f pt, not %.1f x %.1f" % (float(p0.mediabox.width), float(p0.mediabox.height), pw, ph))


# --- the covers ----------------------------------------------------------
def mast_size(text, measure_in):
    """Masthead size (in) that fills the measure, from Barlow Condensed
    Bold's advance widths and kerning-free; capped so a short name doesn't
    get absurd."""
    f = TTFont(os.path.join(FONTS, "BarlowCondensed-Bold.ttf"))
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    adv = sum(hmtx[cmap.get(ord(c), cmap[ord(" ")])][0] for c in text.upper())
    return min(measure_in * upm / adv, 1.45 * U)


MAST = mast_size(SERIES, W - 1.2 * U)
vars_ = ("<style>:root{--pw:%.4fin;--ph:%.4fin;--u:%.4fin;--mast-size:%.4fin}@page{size:%.4fin %.4fin;margin:0}"
         "html,body{margin:0}</style>" % (W + 2 * B, H + 2 * B, U, MAST, W + 2 * B, H + 2 * B))
focus = meta.get("cover_focus", "50% 35%")
front = ('<body><div class="cover" style="--focus:%s"><div class="band"><div class="mast">%s</div>'
         '<div class="line"><span class="pub">%s%s</span><span class="no">No. %s &nbsp;·&nbsp; %s</span></div></div>'
         '<div class="photo"><img src="%s" alt=""></div>'
         '<div class="words"><div class="cl">%s</div>%s</div></div></body></html>'
         % (esc(focus), esc(SERIES), "<b></b>" if PUBLISHER else "", esc(PUBLISHER), NO, esc(YEAR),
            esc(meta["cover"]), esc(meta["cover_line"]),
            '<div class="deck">%s</div>' % esc(meta["deck"]) if meta.get("deck") else ""))
paras = lambda t: "".join("<p>%s</p>" % esc(p.strip()) for p in str(t or "").split("\n\n") if p.strip())
back = ('<body><div class="cover back"><div class="bk"><div class="mast">%s</div>'
        '<div class="blurb">%s</div></div><div class="colophon">%s</div></div></body></html>'
        % (esc(SERIES), paras(meta.get("back")),
           "<p><b>%s &nbsp;No. %s</b> &nbsp;·&nbsp; %s</p>%s" % (esc(SERIES), NO, esc(YEAR), paras(meta.get("colophon")))))
for name, doc in (("front", front), ("back", back)):
    open(name + ".html", "w", encoding="utf-8").write(head(TITLE, ["base.css", "cover.css"], vars_) + doc)
    chrome(name + ".html", name + ".pdf")
front_pg = pypdf.PdfReader("front.pdf").pages[0]
back_pg = pypdf.PdfReader("back.pdf").pages[0]
for nm, p in (("front cover", front_pg), ("back cover", back_pg)):
    if abs(float(p.mediabox.width) - pw) > 1 or abs(float(p.mediabox.height) - ph) > 1:
        die("%s is the wrong size" % nm)


# --- assembling ------------------------------------------------------------
pad = (-n_body) % 4                    # body + pad: a multiple of 4; with the four
blank = lambda w=pw, h=ph: pypdf.PageObject.create_blank_page(width=w, height=h)   # cover pages, still


def trim(page):
    """Crop a bleed-size page to its trim."""
    if B:
        box = pypdf.generic.RectangleObject([B * PT, B * PT, (B + W) * PT, (B + H) * PT])
        page.mediabox = box
        page.cropbox = box
    return page


def outline(w, offset):
    for s in sections:
        w.add_outline_item(re.sub(r"<[^>]+>", "", html.unescape(s["title"])), pages[s["id"]] - 1 + offset)


os.makedirs(out_dir, exist_ok=True)
info = {"/Title": TITLE, "/Author": str(meta.get("editor", PUBLISHER or SERIES))}

# For reading: front, the pages, back; at trim.
w = pypdf.PdfWriter()
w.append("body.pdf")
w.insert_page(front_pg, 0)
w.add_page(back_pg)
for p in w.pages:
    trim(p)
outline(w, 1)
w.add_metadata(info)
reading = os.path.join(out_dir, "%s-%s.pdf" % (NAME, "letter" if edition == "letter" else "half-letter"))
w.write(reading)
print(reading)

if edition == "letter":
    # Print interior: the pages and the padding, bleed kept, boxes set.
    w = pypdf.PdfWriter()
    w.append("body.pdf")
    for _ in range(pad):
        w.add_page(blank())
    tb = pypdf.generic.RectangleObject([B * PT, B * PT, (B + W) * PT, (B + H) * PT])
    for p in w.pages:
        p.trimbox = tb
        p.bleedbox = p.mediabox
    w.add_metadata(info)
    f = os.path.join(out_dir, NAME + "-letter-print-interior.pdf")
    w.write(f)
    print(f)
    # Print cover: back | spine | front, bleed all round. Each cover was
    # drawn with its own bleed, so the back loses its right bleed and the
    # front its left where they meet the spine.
    spine = float(os.environ.get("SPINE") or 0) * PT
    cw, ch = 2 * W * PT + 2 * B * PT + spine, ph
    sheet = blank(cw, ch)
    # the front's trim starts where the back's trim ends plus the spine;
    # its left bleed would run over the back, so the back goes on top,
    # cut at its own trim edge
    sheet.merge_transformed_page(front_pg, pypdf.Transformation().translate(W * PT + spine, 0))
    back_clip = pypdf.PdfReader("back.pdf").pages[0]
    back_clip.mediabox = pypdf.generic.RectangleObject([0, 0, (B + W) * PT, ph])
    back_clip.cropbox = back_clip.mediabox
    sheet.merge_transformed_page(back_clip, pypdf.Transformation())
    w = pypdf.PdfWriter()
    w.add_page(sheet)
    w.pages[0].trimbox = pypdf.generic.RectangleObject([B * PT, B * PT, cw - B * PT, ch - B * PT])
    w.add_metadata(dict(info, **{"/Title": TITLE + " (cover)"}))
    f = os.path.join(out_dir, NAME + "-letter-print-cover.pdf")
    w.write(f)
    print(f)
else:
    # Booklet: front, blank inside front, the pages, padding, blank inside
    # back, back; sheet k carries [n-1-2k | 2k] and, on the back, [2k+1 | n-2-2k].
    seq = [front_pg, blank()] + list(body_reader.pages) + [blank() for _ in range(pad)] + [blank(), back_pg]
    n = len(seq)
    assert n % 4 == 0
    w = pypdf.PdfWriter()
    for k in range(n // 4):
        for left, right in ((n - 1 - 2 * k, 2 * k), (2 * k + 1, n - 2 - 2 * k)):
            side = blank(2 * pw, ph)
            side.merge_transformed_page(seq[left], pypdf.Transformation())
            side.merge_transformed_page(seq[right], pypdf.Transformation().translate(pw, 0))
            w.add_page(side)
    w.add_metadata(dict(info, **{"/Title": TITLE + " (booklet: letter, saddle stitch)"}))
    f = os.path.join(out_dir, NAME + "-half-saddle-stitch-letter.pdf")
    w.write(f)
    print(f)

print("%s: %d pages, %d blank to make a multiple of 4%s; contents: %s" % (
    edition, n_body, pad, " (fill them or cut)" if pad else "",
    ", ".join("%s p%d" % (s["id"], pages[s["id"]]) for s in sections)), file=sys.stderr)
