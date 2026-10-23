"""かなの書き順のデータ(assets/kana/kana-strokes.json)を KanjiVG から作る(UX15・2026-10-23)。

使い方(app フォルダで・ネットにつながっているとき):
  python -I tools/make_kana_strokes.py [raw-export.json] [--commit <KanjiVG のコミット>]
  - 既定の raw-export.json は content/raw/raw-export.json(教材マスターの書き出し)。kana_chars の char と
    kana_words の kana に出てくるかなを集め、小さい字(ゃゅょっ など)と ー を足した分だけを取りに行く(要るものだけ)
  - 元:KanjiVG(https://github.com/KanjiVG/kanjivg)の kanji/<5桁の16進>.svg。版は下の COMMIT に固定する
    (作り直しても同じになる。版を上げるときは --commit で指定し、JSON の commit と報告に記録する)
  - SVG からは「画の線(path の d)」と「画の番号の位置(StrokeNumbers の text)」だけを正規表現で取り出す
    (取りに行った SVG は信用しない入力として扱う:XML としては読まない・実行しない)
  - ライセンス:KanjiVG は Ulrich Apel の著作物で CC BY-SA 3.0(README.md・COPYING で確認・2026-10-23)。
    取り出した JSON は改変物なので、同じ CC BY-SA 3.0 で配る(JSON の license・attribution・changes に書く。
    アプリのライセンスの画面にも名前と出どころを出す=src/licenses/kana-assets.ts)
  - 取りに行った SVG は content/raw/kanjivg/<commit>/ に置く(.gitignore 済みの作業フォルダ)
  - 書き出しの安全策(AGENTS.md 原則6):1字でも取れなければ終了コード1で止め、今の JSON は書き換えない。
    raw-export.json が無いときも終了コード2で止める(小さい字だけの JSON で今のものを上書きしない)。書くときは一時ファイル → 置き換え
"""
import json
import pathlib
import re
import sys
import urllib.request

APP = pathlib.Path(__file__).resolve().parent.parent
OUT = APP / "assets" / "kana" / "kana-strokes.json"
CACHE = APP / "content" / "raw" / "kanjivg"
REPO = "https://github.com/KanjiVG/kanjivg"
# 2026-10-23 に確かめた master の先頭(2026-09-29 のコミット)
COMMIT = "70a0b7ae0c18ceb5cb358274b029cce0234a43bc"
RAW_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/{commit}/kanji/{code}.svg"

# 単語にだけ出る字もあるので、小さい字とのばす音は必ず入れる
ALWAYS = "ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮー"
KANA = re.compile(r"[ぁ-ゖァ-ヺー]")
PATH = re.compile(r'<path\s+id="kvg:[0-9a-f]{5}-s(\d+)"[^>]*?\sd="([^"]+)"')
NUMBER = re.compile(r'<text\s+transform="matrix\(1 0 0 1 ([\d.\-]+) ([\d.\-]+)\)">(\d+)</text>')
SAFE_D = re.compile(r"^[MmCcSsLlHhVvZzQqTtAa0-9.,\-\s]+$")


def wanted_chars(raw_path: pathlib.Path) -> list[str]:
    chars = set(ALWAYS)
    sheets = json.loads(raw_path.read_text(encoding="utf-8")).get("sheets", {})
    for row in sheets.get("kana_chars", []):
        chars.update(KANA.findall(str(row.get("char", ""))))
    for row in sheets.get("kana_words", []):
        chars.update(KANA.findall(str(row.get("kana", ""))))
    return sorted(chars)


def fetch(code: str, commit: str) -> str:
    cache = CACHE / commit / f"{code}.svg"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    url = RAW_URL.format(commit=commit, code=code)
    with urllib.request.urlopen(url, timeout=30) as response:
        body = response.read(200_000).decode("utf-8")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(body, encoding="utf-8")
    return body


def parse(svg: str) -> dict:
    strokes = sorted(((int(n), d) for n, d in PATH.findall(svg)), key=lambda pair: pair[0])
    if not strokes or [n for n, _ in strokes] != list(range(1, len(strokes) + 1)):
        raise ValueError("画の番号が 1 から順にそろっていません")
    for _, d in strokes:
        if not SAFE_D.match(d):
            raise ValueError("path の d に想定外の文字があります")
    numbers = sorted(((int(n), float(x), float(y)) for x, y, n in NUMBER.findall(svg)), key=lambda entry: entry[0])
    positions = [[round(x, 2), round(y, 2)] for _, x, y in numbers] if len(numbers) == len(strokes) else []
    return {"strokes": [d for _, d in strokes], "numbers": positions}


def main(argv: list[str]) -> int:
    commit = COMMIT
    args = list(argv)
    if "--commit" in args:
        at = args.index("--commit")
        commit = args[at + 1]
        del args[at : at + 2]
    raw_path = pathlib.Path(args[0]) if args else APP / "content" / "raw" / "raw-export.json"
    if not raw_path.exists():
        print(f"{raw_path} がありません。要る字が分からないので、今の JSON には触らずに止めます", file=sys.stderr)
        return 2
    chars = wanted_chars(raw_path)
    result: dict[str, dict] = {}
    missing: list[str] = []
    for char in chars:
        code = f"{ord(char):05x}"
        try:
            result[char] = parse(fetch(code, commit))
        except Exception as error:  # 無い字・形の崩れた SVG(全部見てから、まとめて報告する)
            missing.append(f"{char}({code}): {error}")
    if missing:
        print("取れなかった字があるので、何も書き換えずに止めます:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 1
    data = {
        "source": "KanjiVG",
        "url": REPO,
        "commit": commit,
        "license": "CC BY-SA 3.0",
        "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0/",
        "attribution": "KanjiVG is copyright Ulrich Apel and released under the Creative Commons Attribution-Share Alike 3.0 licence.",
        "changes": "Only the stroke paths (path d) and stroke-number positions were extracted from the kana SVG files and stored as JSON. This JSON is distributed under the same licence (CC BY-SA 3.0).",
        "viewBox": 109,
        "chars": result,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    temp = OUT.with_suffix(".json.tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    temp.replace(OUT)
    print(f"{len(result)}字を書き出しました: {OUT}(KanjiVG {commit[:7]})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
