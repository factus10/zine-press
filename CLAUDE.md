# Zine press: notes for Claude

Read README.md (usage, the block table) and STYLE.md (the design system and
the content model) before changing anything.

- One source, two editions. Never put a size, column count or colour in an
  issue's Markdown. Edition differences live in style/letter.css and
  style/half.css; shared rules in style/base.css; covers in style/cover.css.
- Accent colour (#8e3424) is for data and annotation only (.ann, .data,
  notes, charts) plus the masthead. Don't use it for headings or links.
- Captions: the editor's words, then record="…" from the holding
  institution, verbatim. Never invent a record, a call number, a date or an
  attribution. If one is missing, the sources page ("What we could not
  verify") says so.
- After any change, build the specimen (`./make.sh issues/00-specimen`), look
  at every page of both editions (pdftoppm), and check that book.py reports
  0 padding pages for the issue you're working on, or say how many.
- Fonts: static instances only (Chrome embeds a variable font as Type 3,
  which print-on-demand printers can reject). `pdffonts` on the print
  interior must show no Type 3 fonts.
- The pipeline mirrors tspico-firmware-build tools/manual-pdf; keep the two
  recognisably alike so a fix in one can be carried to the other.
