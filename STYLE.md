# Style

The look is decoded from six spreads of *Serie Archivo No. 01: Possibly Related* (Métrica, 2026; A4, 48 pp, perfect-bound). The font names below are the closest free matches. They are not identifications: the shop page doesn't name its typefaces.

We borrow the system. Their name, masthead, mark and page designs stay theirs. The series name, publisher mark and covers here are our own.

## The system

| Element | Reference | Here |
|---|---|---|
| Masthead | condensed bold grotesque, caps, oxide red, set to the full measure | Barlow Condensed Bold, `--accent` #8e3424; book.py sizes it to fill the measure |
| Titles | large, light, humanist semi-slab serif | Merriweather Light, 40 pt letter / 25 pt half |
| Lede | the same serif at about 12–13 pt, ragged | 12.6 / 10.4 pt |
| Body | the same serif, justified, two columns | 8.8 pt / 1.5, two columns (letter); one column (half) |
| Kicker | ■ plus bold sans in tracked capitals, very small | Barlow Bold 5.6 pt, tracking .2em |
| Captions | small sans; bold lead-in; the institution's record in grey italic | Barlow 5.9 pt |
| Pull quote, cover line | the serif's italic | Merriweather Light Italic |
| Folios | page number at the outside, series · number inside, tracked caps | margin boxes in base.css |
| Accent | red, only for data and annotation | `.ann`, `.data`, `::: notes`, charts |
| Pictures | black and white, film-strip borders, full-bleed plates | grayscale filter; `.strip`; `.plate` |
| Rules | hairlines; one heavier rule over the editor's letter | 0.5 pt / 1.4 pt |
| Reversed page | black page with a giant numeral and a contact sheet | `::: dark`, `.numeral`, `.contact` |

## What makes it work (the content model)

The stylesheet carries maybe a third of the effect. The rest is editorial. An issue in this style:

1. **Is about documents.** Every picture is an object someone holds, and the issue looks at it closely.
2. **Captions carry the record.** The holder's own catalogue line (collection, call number, date, rights) sits under the editor's caption and is kept separate from it.
3. **Measures something.** At least one section counts, measures or maps, shown in the accent colour.
4. **Annotates instead of illustrating.** Outlined words and numbered callouts point at the specific thing.
5. **Ends with what it couldn't verify.** The sources page is part of the design, not small print.

Ordinary essays poured into this template give a clean editorial layout, not this magazine.

## Section kickers

Use one-to-two-word kickers, and reuse them from issue to issue so they become departments. The reference uses: The Document, The Story, Plates, Contact Sheet, Read Closely, Measured, Print Room, Score, Cabinet, Objects, Portfolio, Sources. Pick our own set and keep it stable.

## Rules

- Accent colour on data and annotation only. Never use it for decoration, headings or links.
- One picture per plate. A plate's caption is short. If it needs more words, write a section instead.
- No second typeface, no second accent, no drop shadows, no tints.
- Titles are sentence case. Kickers, labels and folios are tracked capitals.
- Every picture has a record line, or an entry on the sources page saying why not.
- Pictures print in black and white unless marked `{.color}`. Use colour only when colour is the subject: a print, a cover, a stamp.

## Two editions, one source

The Markdown never sets sizes. Letter keeps the reference's proportions: two columns, plates bleeding off the top and outside edges. Half letter is the zine: one column, and plates inside the margins, because home printers can't print to the edge. When a layout works in one edition and not the other, fix the CSS, not the Markdown.
