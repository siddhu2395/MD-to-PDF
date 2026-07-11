#!/usr/bin/env python3
"""Convert a Markdown file to a PDF.

Usage:
    python md_to_pdf.py input.md [output.pdf]
"""

import argparse
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

# Basic styling so the PDF looks clean and readable.
CSS = """
body { font-family: Helvetica, sans-serif; font-size: 11pt; line-height: 1.5; }
h1, h2, h3, h4 { font-family: Helvetica, sans-serif; color: #222; }
h1 { font-size: 22pt; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
h2 { font-size: 17pt; border-bottom: 1px solid #eee; padding-bottom: 3px; }
h3 { font-size: 14pt; }
code { font-family: Courier, monospace; font-size: 10pt; background-color: #f5f5f5; }
pre { font-family: Courier, monospace; font-size: 9.5pt; background-color: #f5f5f5;
      padding: 8px; border: 1px solid #ddd; }
blockquote { color: #555; margin-left: 16px; padding-left: 8px;
             border-left: 3px solid #ccc; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #999; padding: 4px 8px; }
th { background-color: #eee; }
a { color: #0366d6; }
"""


def convert(input_path: Path, output_path: Path) -> None:
    """Read a Markdown file and write it out as a PDF."""
    md_text = input_path.read_text(encoding="utf-8")

    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "tables", "fenced_code", "sane_lists", "toc"],
    )
    html = f"<html><head><style>{CSS}</style></head><body>{html_body}</body></html>"

    with open(output_path, "wb") as pdf_file:
        result = pisa.CreatePDF(html, dest=pdf_file, encoding="utf-8")

    if result.err:
        raise RuntimeError(f"PDF generation failed with {result.err} error(s)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to a PDF."
    )
    parser.add_argument("input", help="Path to the Markdown file (e.g. notes.md)")
    parser.add_argument(
        "output",
        nargs="?",
        help="Path for the PDF output (default: same name with .pdf extension)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        sys.exit(f"Error: input file not found: {input_path}")

    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")

    try:
        convert(input_path, output_path)
    except Exception as exc:
        sys.exit(f"Error: {exc}")

    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    main()
