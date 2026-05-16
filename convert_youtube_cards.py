from pathlib import Path
import re
import html

pattern = re.compile(
    r'''<div class="video-card">\s*'''
    r'''<a href="https://www\.youtube\.com/watch\?v=([^"&]+)[^"]*" target="_blank">\s*'''
    r'''<img src="[^"]*" alt="([^"]*)">\s*'''
    r'''</a>\s*'''
    r'''<h3>(.*?)</h3>\s*'''
    r'''</div>''',
    re.S,
)

def convert_file(path: Path):
    text = path.read_text(encoding="utf-8")

    def repl(m):
        video_id = m.group(1)
        title = html.unescape(m.group(3).strip())
        title = re.sub(r"\s+", " ", title)
        title = title.replace('"', "&quot;")
        return f'{{{{< youtubelite id="{video_id}" title="{title}" >}}}}'

    new_text, count = pattern.subn(repl, text)

    if count == 0:
        print(f"SKIP: {path} 変換対象なし")
        return

    backup = path.with_suffix(path.suffix + ".bak")
    backup.write_text(text, encoding="utf-8")
    path.write_text(new_text, encoding="utf-8")

    print(f"OK: {path}  {count}件変換 / backup: {backup}")

# content/categories 以下の md をまとめて変換
for path in Path("content/categories").glob("*.md"):
    convert_file(path)
