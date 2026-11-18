# Zine press

One Markdown file per issue. One build gives two editions:

| Edition | Files | For |
|---|---|---|
| **Letter** (8.5 × 11 in) | `NN-slug-letter.pdf` | reading on screen |
| | `NN-slug-letter-print-interior.pdf` | print on demand (0.125 in bleed; TrimBox/BleedBox set; page count a multiple of 4) |
| | `NN-slug-letter-print-cover.pdf` | the cover sheet: back, spine, front, with bleed |
| **Half letter** (5.5 × 8.5 in) | `NN-slug-half-letter.pdf` | reading on screen |
| | `NN-slug-half-saddle-stitch-letter.pdf` | home printing: two up on letter, double-sided, flip on the short edge, fold, staple |

The look is decoded from *Serie Archivo No. 01* (Métrica, 2026): see [STYLE.md](STYLE.md). The pipeline is the one the TS-Pico manual uses (tspico-firmware-build `tools/manual-pdf`): pandoc with a Lua filter, then CSS paged media printed by headless Chrome, then pypdf for the contents, covers, booklet and print files.

## Make an issue

```sh
cp -R issues/00-specimen issues/01-your-slug     # start from the specimen
$EDITOR issues/01-your-slug/issue.md             # front matter + text
./make.sh issues/01-your-slug                     # → build/01-your-slug/
EDITION=letter ./make.sh issues/01-your-slug      # one edition only
SPINE=0.11 EDITION=letter ./make.sh issues/…      # perfect-bound: spine width in inches
KEEP=1 ./make.sh issues/…                         # keep the HTML to debug a layout
```

The build reports how many blank pages it added to reach a multiple of 4. Blank pages in a magazine look like mistakes, so fill or cut until it says 0.

Pushing to GitHub runs the same build (`.github/workflows/build.yml`) for every issue folder that changed and uploads the PDFs as an artifact, kept 7 days.

## Needs

- pandoc 3 or later
- Google Chrome or Chromium (set `CHROME` if it isn't found)
- Python 3 with `pypdf`, `PyYAML` and `fontTools`
- Pillow, only for `tools/placeholders.py`

On a Mac: `brew install pandoc` and `pip3 install pypdf pyyaml fonttools pillow`.

## Writing an issue

The front matter sets the cover and the folios:

```yaml
series: Field Archive        # masthead and folios
number: 1
year: 2026
publisher: Andertone         # small, under the masthead
editor: David Anderson
cover_line: Possibly Related # big white italic on the cover
deck: The short line under it, in tracked capitals
cover: img/cover.jpg
cover_focus: 50% 40%         # which part of the picture to keep when it's cropped
back: |
  Back-cover text. Blank line between paragraphs.
colophon: |
  Fonts, printing, credits.
```

The blocks are listed below. The specimen issue (`issues/00-specimen`) uses every one of them.

| Write | Get |
|---|---|
| `# Title {kicker="The story"}` | new page; kicker, title; the next paragraph is the lede; the rest is the body (two columns in letter, one in half) |
| `![**Lead-in.** Caption.](img/x.jpg){record="Holder, call no."}` | figure; the record goes under the caption in grey italic |
| `{.wide}` on an image | spans both columns (letter) |
| `{.color}` on an image | keeps its colour (pictures print in black and white by default) |
| `::: {.pull by="Name, 1964"}` | pull quote |
| `::: plate` … `:::` (before a `#`) | a page that is one picture, with a caption and an optional pull quote |
| `::: strip` with images | a film strip; each image's alt text is its label |
| `::: dark` with `[72]{.numeral}` and `::: {.contact cols=8}` | a black page with a contact sheet |
| `[words]{.ann n=1}` + `::: notes` with a numbered list | annotation in the accent colour, with its key |
| `[3.38 mm]{.data}` | a measured value in the accent colour |
| pipe table + `Table: caption` | data table |
| `::: {.letter by="Name"}` | editor's letter, placed on the contents page |
| `# What we could not verify {kicker="Sources"}` + `::: unverified` | the closing sources page |

Pictures: black-and-white source files, at least 300 ppi at their printed size. That is about 2,600 px wide for a letter plate with bleed, and 1,300 px for a half-column figure.

`tools/placeholders.py DIR name:WxH …` makes grey stand-ins for drafts. Each one is marked PLACEHOLDER so it can't reach print unnoticed.
