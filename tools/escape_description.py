"""apps.odoo.com reads static/description/index.html as Latin-1: every non-ASCII character becomes an HTML entity.

Usage: python tools/escape_description.py
"""

from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "aiparsy_connector" / "static" / "description" / "index.html"


def main():
    text = PAGE.read_text(encoding="utf-8")
    escaped = "".join(ch if ord(ch) < 128 else f"&#{ord(ch)};" for ch in text)
    PAGE.write_text(escaped, encoding="ascii", newline="\n")
    print(PAGE, "non-ASCII left:", sum(1 for ch in escaped if ord(ch) >= 128))


if __name__ == "__main__":
    main()
