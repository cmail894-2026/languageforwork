# Kana stroke-order data (My Japanese)

Stroke-order data used in the kana course and the stroke-order games of the app **My Japanese** (Language for Work).

## Files

| File | What it is | Licence |
|---|---|---|
| `kana-strokes.json` | Stroke paths of the hiragana and katakana, in stroke order | CC BY-SA 3.0 (derived from KanjiVG) |
| `kanji-strokes.json` | Stroke paths of 13 kanji used in the stroke-order quiz (万 上 中 九 右 女 左 必 書 母 生 田 車) | CC BY-SA 3.0 (derived from KanjiVG) |
| `kana-brush.json` | Brush-shaped strokes for the stroke-order animation: disks along the KanjiVG centre lines with stroke-end shapes (tome / hane / harai), timing, label and number positions | CC BY-SA 3.0 (derived from KanjiVG) |
| `kana-glyphs.json` | Kana glyph outlines aligned to the KanjiVG strokes. The `d` fields are outlines from the Klee One SemiBold font; the `m` and `n` fields are KanjiVG strokes and number positions | `d`: SIL Open Font License 1.1 (Klee One, Fontworks Inc. / The Klee Project Authors). `m`, `n`: CC BY-SA 3.0 (derived from KanjiVG) |
| `make_kana_strokes.py` | Script used to make `kana-strokes.json` | — |

Each JSON file also records its sources and licences in its `source` (or `license` / `attribution`) fields.

## KanjiVG

- Copyright © Ulrich Apel, https://kanjivg.tagaini.net/ / https://github.com/KanjiVG/kanjivg
- Source commit: `70a0b7ae0c18ceb5cb358274b029cce0234a43bc` (files `kanji/<hex>.svg`)
- Licence: **Creative Commons Attribution-Share Alike 3.0** — https://creativecommons.org/licenses/by-sa/3.0/
- Changes: the stroke paths (`d` attributes, in stroke order) were extracted. For `kana-brush.json`, stroke ends were extended or trimmed, closed loops kept, brush-width disks were placed along the centre lines, and stroke numbers were moved where they overlapped. For `kana-glyphs.json`, stroke ends were extended and the strokes and numbers of the dakuten / handakuten marks were moved to match the Klee One glyphs.

You may share and adapt the KanjiVG-derived data under the terms of CC BY-SA 3.0 (give appropriate credit to KanjiVG / Ulrich Apel, indicate changes, and share alike).

## Klee One

- Klee One SemiBold — Copyright 2020 The Klee Project Authors (https://github.com/fontworks-fonts/Klee)
- Licence: **SIL Open Font License 1.1** — https://openfontlicense.org
- The `d` outlines in `kana-glyphs.json` are taken from the font and remain under the SIL Open Font License 1.1.
