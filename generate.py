import sys
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
README = Path(__file__).parent / "README.md"


def load_category(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_duplicates(categories: list[tuple[Path, dict]]) -> bool:
    seen: dict[str, tuple[str, str]] = {}  # url -> (source_file, name)
    duplicates = []

    for cat_file, cat in categories:
        for item in cat.get("items", []):
            url = (item.get("url") or "").rstrip("/")
            if not url:
                continue
            if url in seen:
                prev_file, prev_name = seen[url]
                duplicates.append({
                    "url": url,
                    "name": item["name"],
                    "file": cat_file.name,
                    "existing_in": prev_file,
                    "existing_name": prev_name,
                })
            else:
                seen[url] = (cat_file.name, item["name"])

    if duplicates:
        print("\n⚠️  Duplikasi ditemukan:")
        for d in duplicates:
            print(f"  {d['url']}")
            print(f"    → Sudah ada di {d['existing_in']} sebagai \"{d['existing_name']}\"")
            print(f"    → Duplikat di {d['file']} sebagai \"{d['name']}\"")
            print()
        print("Hapus entry yang duplikat sebelum generate.")
        return True

    return False


def render_notes(notes) -> str:
    if not notes:
        return "-"
    if isinstance(notes, str):
        return notes
    parts = []
    for note in notes:
        text = note.get("text", "")
        author = note.get("author")
        if author:
            avatar = f"![{author}](https://github.com/{author}.png?size=20)"
            parts.append(f"{text} {avatar}")
        else:
            parts.append(text)
    return "<br>".join(parts) if parts else "-"


def render_table(items: list[dict]) -> str:
    lines = ["| Status | Nama | Catatan |", "|:------:|:-----|:--------|"]
    for item in items:
        checkbox = "✅" if item.get("tried") else "⬜"
        name = f"[{item['name']}]({item['url']})"
        notes = render_notes(item.get("notes"))
        lines.append(f"| {checkbox} | {name} | {notes} |")
    return "\n".join(lines)


def main():
    cat_files = sorted(DATA_DIR.glob("*.yaml"))
    categories = [(f, load_category(f)) for f in cat_files]

    if check_duplicates(categories):
        sys.exit(1)

    parts = [
        "# Developer Tools List",
        "",
        "Kami **tidak terikat** dengan provider/service apapun dan kami tidak menerima keuntungan sepeserpun dalam bentuk apapun.",
        "",
    ]

    nav_links = []

    for cat_file, cat in categories:
        title = cat["title"]
        anchor = title.lower().replace(" ", "-").replace("/", "")
        nav_links.append(f"- [{title}](#{anchor})")

        parts.append(f"## {title}")
        if cat.get("note"):
            parts.append(f"> {cat['note']}")
            parts.append("")
        parts.append(render_table(cat["items"]))
        parts.append("")

    # Table of contents
    toc = "\n".join(nav_links)
    parts.insert(4, "### Daftar Kategori")
    parts.insert(5, toc)
    parts.insert(6, "")

    README.write_text("\n".join(parts) + "\n")
    print(f"✅ Generated {README} from {len(categories)} categories.")


if __name__ == "__main__":
    main()
