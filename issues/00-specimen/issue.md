---
series: Field Archive
number: 0
year: 2026
publisher: Andertone
editor: David Anderson
cover_line: Every block, once
deck: A specimen issue of the zine template, with placeholder pictures
cover: img/cover.jpg
cover_focus: 50% 40%
back: |
  This specimen shows every block the template has, so a new issue can start from a copy of it.

  The pictures are placeholders. Replace them, and the words, before printing.
colophon: |
  Set in Merriweather and Barlow (SIL Open Font License). Built with pandoc, Chrome and pypdf.
---

::: {.letter by="The editor"}
Each issue of this zine is a single Markdown file and a folder of pictures. One build makes two editions from it: a letter-size magazine with bleed, for a print-on-demand printer, and a half-letter booklet you can print on a home printer, fold and staple.

The look borrows a system rather than a style. Every section opens with a small kicker in tracked capitals, a large light title and a lede. Pictures are black and white. Every caption ends with the record of the place that holds the picture. One accent colour marks what was measured or annotated, and nothing else.

That system only works if the content earns it. The template can set a record under a caption, but it can't find the record for you. Where the record is missing, the last page of the issue says so.

There is no rush.
:::

::: {.plate}
![**A plate is a page that is a picture.** It runs to the top and outside edges of the letter edition and stops at the margins of the half-letter one.](img/plate.jpg){record="Placeholder. A real plate carries its record here: holder, collection, call number, rights."}

::: {.pull by="The template, on plates"}
"Put the picture first and let the words wait their turn."
:::
:::

# How a page is made {kicker="The method"}

A section starts with a level-one heading, which always opens a new page. The heading's kicker attribute becomes the small line above it, and the paragraph right after the heading becomes the lede, set large and ragged.

Everything after the lede is the body. In the letter edition the body runs in two justified columns; in the half-letter edition it runs in one. Nothing in the Markdown changes between them: only the stylesheet does, which is why the source never sets a size, a column or a colour.

Write figures as ordinary Markdown images, alone in their paragraph. Start the caption with a bold lead-in, then say what the reader is looking at. Add the holder's record as an attribute, and the template sets it under the caption in grey italic, apart from your own words.

![**A figure in the body.** It takes the column's width, and the caption sits under it in small sans.](img/fig-a.jpg){record="Placeholder record. Collection, item number, date, rights statement."}

### A small heading

Third-level headings are set as tracked capitals, like the kicker, for breaking a long section into parts without competing with the title. Second-level headings are serif, for a turn in the argument rather than a new topic.

Pull quotes are a fenced div with a by attribute. They work best where the voice changes: the subject speaking, a source quoted at length, a line worth stopping on.

::: {.pull by="Name, year"}
"A pull quote is set in italic, a size between the lede and the title."
:::

Keep the body plain. The design has room for a picture, a caption, a record, a quote and a table, and that is all. When a page needs something else, that's usually a sign it wants to be a plate or a strip instead.

# The caption next door {kicker="Read closely"}

Annotation has its own colour. Mark words in the text with a bracketed span and a number, and the template outlines them and numbers them in the accent, so the reader can match them to a key.

In a record, the title of an item sometimes [lives in square brackets]{.ann n=1}, which in many catalogues means the cataloguer supplied it rather than finding it on the object. The record may also [name a second item]{.ann n=2} that the first one was filed with. Those two marks are the kind of thing this zine is for: the place where the record says more than it seems to.

::: notes
1. Square brackets: the title was supplied, not found.
2. The related item, which the caption was borrowed from.
:::

![**Frame two, the one it is named after.** A second figure, to show two captions on one page.](img/fig-b.jpg){record="Placeholder record."}

Measured values take the accent too: write [3.38 mm]{.data} and the number prints in oxide red, matching the marks on the pictures and the dots on the charts. Use it for numbers you measured yourself, not for every number in the text.

# Measured {kicker="Data"}

Tables are written as Markdown pipe tables. The template sets them in small sans with tracked heads and hairline rules, and lines up the numbers.

| Frame | Photographer | Page | mm |
|:------|:-------------|-----:|---:|
| A-001 | Name | 4 | 3.38 |
| A-002 | Name | 6 | 3.41 |
| A-003 | Name | 9 | 3.36 |
| B-001 | Name | 12 | 4.02 |
| B-002 | Name | 14 | 3.97 |

Table: A table's caption sits under it, in grey.

A chart is a picture: draw it in whatever you like, in black and the accent, export it as SVG or PNG, and place it as a figure with the {.wide} class so it spans both columns in the letter edition.

::: strip
![A-001 · kept](img/strip-1.jpg)
![A-002 · rejected](img/strip-2.jpg)
![A-003 · kept](img/strip-3.jpg)
![A-004 · rejected](img/strip-4.jpg)

**A film strip.** Each image gets a black frame and the label under it is the image's alt text.
:::

::: dark
[24]{.numeral}

Every frame of a set, on a black page: a contact sheet. The number is set in the condensed face of the masthead, and the grid takes as many columns as the cols attribute asks for.

::: {.contact cols=6}
![](img/c1.jpg)
![](img/c2.jpg)
![](img/c3.jpg)
![](img/c4.jpg)
![](img/c5.jpg)
![](img/c6.jpg)
![](img/c7.jpg)
![](img/c8.jpg)
![](img/c9.jpg)
![](img/c10.jpg)
![](img/c11.jpg)
![](img/c12.jpg)
![](img/c13.jpg)
![](img/c14.jpg)
![](img/c15.jpg)
![](img/c16.jpg)
![](img/c17.jpg)
![](img/c18.jpg)
![](img/c19.jpg)
![](img/c20.jpg)
![](img/c21.jpg)
![](img/c22.jpg)
![](img/c23.jpg)
![](img/c24.jpg)

Placeholder record line for the set: collection, the call numbers of every frame, in order.
:::
:::

# What we could not verify {kicker="Sources"}

The last section of every issue lists what the issue could not confirm, and where every picture and quotation came from. It's the page that lets the rest of the issue be specific.

::: unverified
- **Cover.** Placeholder picture. Record: holder, collection, call number, rights.
- **Page 2, plate.** Placeholder picture.
- **Unverified.** Anything a caption states that the holder's record does not support goes here, with what was checked.
:::
