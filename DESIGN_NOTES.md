# Design notes

## North star
Cursor (cursor.com, ref captured 21 Nov 2026): the product sits framed on top of a piece of art, and the headline stays small and calm. What I take: one framed "product" (here the account table) and one art plane behind the hero. What I leave: their warm cream background and the painting.

Second ref, Opal: the top-down view. A drone sees a solar site from above, so the hero art is a top-down plan of PV rows with a docked drone's patrol loop.

## Theses
- Visual: an engineer's site plan of a desert PV block, cool and precise, with one safety-yellow line (the drone path).
- Content: hero (what this is, for whom) / why Gulf solar / the 17 accounts / the 4-touch sequence / how I built it and what I left out.
- Interaction: one load moment (the patrol path draws itself once), country filter on the table, copy button on each first line.
- Imagery asset: inline SVG plan, hand-built from patterns (rows of panels, inverter pads, fence, dock, flight loop). No stock, no AI images.

## Tokens
- ground #E7EAE4 (sabkha grey, cool not cream), ink #17212B, pv #22406E, pv-2 #35609E, sand #CDB58A, signal #F0B323 (graphic only, never text), muted #56616B, rule #C6CCC3
- Type: Bricolage Grotesque (display, opsz, 700, tight tracking), Instrument Sans (text). Tabular numbers in the table.
- Layout: left aligned, 12-col max 1180px. Hero text left 5 cols, plan right 7 cols bleeding to the edge. Table full width, rows split by hairlines, not cards. Sequence is a real sequence, so numbered.

## Review against the brief
- First plan had a dark navy page with a yellow accent: too close to "near black + one bright accent". Moved to a light sabkha ground and kept yellow only on the drone path and focus ring.
- Dropped an idea for a stat strip ("23 GW / 17 accounts / 6 countries"): that is the stat-tile hero the user bans. The GW total lives in one sentence.
- No eyebrows, no all caps, no mono labels, no arrows on links.
