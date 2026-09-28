"""Check every indexed approved visual has matching PNG, SVG, and HTML."""

import re
from pathlib import Path
from xml.etree import ElementTree

root = Path(__file__).resolve().parents[1]
references = [root / "references/approved-ppt-examples.md", root / "references/title-styles.md"]
linked = set()
for reference in references:
    for path in re.findall(r"\]\((\.\./assets/[^)]+\.(?:png|svg|html))\)", reference.read_text()):
        if "/brand-ppt/" in path or "/title-styles/" in path:
            linked.add((reference.parent / path).resolve())

stems = {path.with_suffix("") for path in linked}
assert stems, "No approved visual assets linked"
for stem in stems:
    files = {ext: stem.with_suffix(ext) for ext in (".png", ".svg", ".html")}
    assert all(path in linked and path.is_file() for path in files.values()), stem
    assert files[".png"].read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), stem
    svg = files[".svg"].read_text()
    ElementTree.fromstring(svg)
    assert svg in files[".html"].read_text(), stem

print(f"Verified {len(stems)} approved PNG/SVG/HTML sets")
