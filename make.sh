#!/bin/sh
# Build one issue of the zine as PDFs.
#
# Usage: [EDITION=letter|half|both] [SPINE=in] ./make.sh issues/NN-slug [OUTDIR]
#        (OUTDIR defaults to build/NN-slug)
#
#   letter  NN-slug-letter.pdf                  8.5 x 11 in, for reading
#           NN-slug-letter-print-interior.pdf   with 0.125 in bleed, for print on demand
#           NN-slug-letter-print-cover.pdf      back | spine | front, with bleed
#   half    NN-slug-half-letter.pdf             5.5 x 8.5 in, for reading
#           NN-slug-half-saddle-stitch-letter.pdf
#                                               booklet, two up on letter, to print at home
#
# Both editions come from the same issue.md; only the stylesheet differs
# (style/letter.css, style/half.css). The pipeline is the TS-Pico manual's
# (tspico-firmware-build tools/manual-pdf): pandoc with a Lua filter makes
# HTML, Chrome prints it with CSS paged media, book.py (pypdf) makes the
# contents, covers, booklet and print files.
#
# Needs pandoc 3 or later, Google Chrome or Chromium (set CHROME if it isn't
# found), Python 3 with pypdf, PyYAML and fontTools. The fonts are in fonts/.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -n "$1" ] || { echo "usage: $0 issues/NN-slug [OUTDIR]" >&2; exit 1; }
ISSUE="$(cd "$1" && pwd)"
[ -f "$ISSUE/issue.md" ] || { echo "$ISSUE/issue.md not found" >&2; exit 1; }
NAME="$(basename "$ISSUE")"
OUT="${2:-$HERE/build/$NAME}"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
EDITION="${EDITION:-both}"

if [ -z "$CHROME" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           google-chrome google-chrome-stable chromium chromium-browser; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then CHROME="$c"; break; fi
  done
fi
[ -n "$CHROME" ] || { echo "Chrome or Chromium not found; set CHROME" >&2; exit 1; }
export CHROME

case "$EDITION" in both) EDITIONS="letter half" ;; letter|half) EDITIONS="$EDITION" ;;
  *) echo "EDITION must be letter, half or both" >&2; exit 1 ;; esac

for ed in $EDITIONS; do
  WORK="$(mktemp -d)"
  pandoc "$ISSUE/issue.md" -f markdown -t html5 --section-divs \
         --lua-filter "$HERE/tools/zine.lua" -o "$WORK/issue.html"
  python3 "$HERE/tools/book.py" "$WORK" "$ISSUE" "$ed" "$OUT"
  if [ -n "$KEEP" ]; then echo "kept $WORK" >&2; else rm -rf "$WORK"; fi
done
