# Kana stroke-order data (My Japanese)

`kana-strokes.json` contains the stroke paths of the hiragana and katakana used in the kana course of the app **My Japanese** (Language for Work).

## Source and licence

- Derived from **KanjiVG** — copyright © Ulrich Apel, https://kanjivg.tagaini.net/ / https://github.com/KanjiVG/kanjivg
- Source commit: `70a0b7ae0c18ceb5cb358274b029cce0234a43bc` (files `kanji/<hex>.svg`)
- Licence: **Creative Commons Attribution-Share Alike 3.0** — https://creativecommons.org/licenses/by-sa/3.0/
- `kana-strokes.json` is a modified work: only the stroke paths (`d` attributes, in stroke order) of the kana were extracted and combined into one JSON file. It is released under the same licence (CC BY-SA 3.0).
- `make_kana_strokes.py` is the script used to make the file.

You may share and adapt this data under the terms of CC BY-SA 3.0 (give appropriate credit to KanjiVG / Ulrich Apel, indicate changes, and share alike).
