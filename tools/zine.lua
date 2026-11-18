-- pandoc filter for the zine (make.sh). It turns the issue's Markdown
-- (pandoc's own markdown, so fenced divs, bracketed spans and attributes
-- work) into the blocks the stylesheets expect. Nothing here sets a size or
-- a colour: that is style/*.css, so the letter and half-letter editions come
-- from the same HTML.
--
-- 1. Sections. Every level-1 heading starts a section (pandoc's
--    --section-divs puts the heading's attributes on the <section>, so
--    kicker="The story" becomes data-kicker, which the CSS prints above the
--    title). The first paragraph after the heading becomes the lede; the
--    rest of the section, up to the next level-1 heading or a page-level
--    block (.plate, .dark, .contents), is wrapped in <div class="body">,
--    which the letter edition sets in two columns.
--
-- 2. Figures. An image alone in a paragraph is a figure; its record="..."
--    attribute (the holding institution's record: collection, call number,
--    rights) is printed under the caption in the record style. Start the
--    caption with **bold** for the lead-in, as the magazine does.
--
-- 3. Film strips and contact sheets. In a ::: strip or ::: contact div,
--    each image becomes a framed frame; its alt text is the small label under
--    it (strip) or nothing (contact). ::: {.contact cols=8} sets the columns.
--
-- 4. Page-level blocks (.plate, .dark, .contents) are never put inside a
--    section's two-column body: they take a page of their own.

local PAGE_LEVEL = { plate = true, dark = true, contents = true }

local function has_class(b, names)
  if b.t ~= "Div" then return false end
  for _, c in ipairs(b.classes) do
    if names[c] then return true end
  end
  return false
end

-- 2. figure records
local function record_of(img)
  local r = img.attributes["record"]
  img.attributes["record"] = nil
  return r
end

local function figure(img, caption_inlines, record)
  local cap = pandoc.List()
  if caption_inlines and #caption_inlines > 0 then
    cap:insert(pandoc.Span(caption_inlines, pandoc.Attr("", { "caption" })))
  end
  if record and record ~= "" then
    cap:insert(pandoc.Span({ pandoc.Str(record) }, pandoc.Attr("", { "record" })))
  end
  local classes = { "fig" }
  for _, c in ipairs(img.classes) do table.insert(classes, c) end
  local blocks = { pandoc.Plain({ img }) }
  if #cap > 0 then
    table.insert(blocks, pandoc.Div({ pandoc.Plain(cap) }, pandoc.Attr("", { "figcap" })))
  end
  return pandoc.Div(blocks, pandoc.Attr("", classes))
end

-- pandoc 3 makes a Figure block of a lone image
function Figure(fig)
  local img
  fig:walk({ Image = function(i) img = img or i end })
  if not img then return nil end
  local record = record_of(img)
  local cap = pandoc.utils.blocks_to_inlines(fig.caption.long)
  img.caption = {}
  return figure(img, cap, record)
end

-- 3. strips and contact sheets
local function frames(div, labelled)
  local out = pandoc.List()
  div:walk({
    Image = function(img)
      local label = pandoc.utils.stringify(img.caption)
      img.caption = {}
      record_of(img)
      local inner = { pandoc.Plain({ img }) }
      if labelled and label ~= "" then
        table.insert(inner, pandoc.Div({ pandoc.Plain({ pandoc.Str(label) }) }, pandoc.Attr("", { "label" })))
      end
      out:insert(pandoc.Div(inner, pandoc.Attr("", { "frame" })))
    end,
  })
  return out
end

function Div(div)
  if div.classes:includes("strip") or div.classes:includes("contact") then
    local labelled = div.classes:includes("strip")
    local fr = frames(div, labelled)
    -- keep a heading, intro text or caption written inside the div
    local keep = pandoc.List()
    for _, b in ipairs(div.content) do
      local only_images = b.t == "Figure"
      if b.t == "Para" or b.t == "Plain" then
        only_images = true
        for _, i in ipairs(b.content) do
          if i.t ~= "Image" and i.t ~= "Space" and i.t ~= "SoftBreak" and i.t ~= "LineBreak" then
            only_images = false
          end
        end
      end
      if not only_images then keep:insert(b) end
    end
    -- a strip is one row: as many columns as frames (up to 6) unless cols says
    local cols = div.attributes["cols"] or (labelled and tostring(math.min(#fr, 6))) or nil
    local grid = pandoc.Div(fr, pandoc.Attr("", { "frames" }))
    if cols then grid.attributes["style"] = "--cols:" .. cols end
    div.attributes["cols"] = nil
    local content = pandoc.List({ grid })
    content:extend(keep)
    div.content = content
    return div
  end
end

-- 1. sections: lede and body
function Pandoc(doc)
  local out, i, blocks = pandoc.Blocks({}), 1, doc.blocks
  while i <= #blocks do
    local b = blocks[i]
    out:insert(b)
    i = i + 1
    if b.t == "Header" and b.level == 1 then
      if blocks[i] and blocks[i].t == "Para" then
        out:insert(pandoc.Div({ blocks[i] }, pandoc.Attr("", { "lede" })))
        i = i + 1
      end
      local body = pandoc.Blocks({})
      while i <= #blocks and not (blocks[i].t == "Header" and blocks[i].level == 1)
            and not has_class(blocks[i], PAGE_LEVEL) do
        body:insert(blocks[i])
        i = i + 1
      end
      if #body > 0 then out:insert(pandoc.Div(body, pandoc.Attr("", { "body" }))) end
    end
  end
  doc.blocks = out
  return doc
end

return {
  { Figure = Figure },
  { Div = Div },
  { Pandoc = Pandoc },
}
