#!/usr/bin/env python3
"""Convert a Markdown file to a PDF.

Usage:
    python md_to_pdf.py input.md [output.pdf]
"""

import argparse
import re
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
table { border-collapse: collapse; width: 100%; margin-top: 8px; margin-bottom: 14px; }
th, td { border: 1px solid #999; padding: 4px 8px; }
th { background-color: #eee; }
a { color: #0366d6; }
"""

# Page layout with a reserved footer frame at the bottom of every page.
# The element whose id matches -pdf-frame-content is repeated on each page.
PAGE_CSS = """
@page {
    margin: 2cm;
    margin-bottom: 2.5cm;
    @frame footer_frame {
        -pdf-frame-content: footer_content;
        bottom: 1cm;
        margin-left: 2cm;
        margin-right: 2cm;
        height: 1cm;
    }
}
.footer-table { border-collapse: collapse; width: 100%; margin: 0; }
.footer-table td { border: none; padding: 0; font-size: 8.5pt; color: #888; }
"""

FOOTER_HTML = """
<div id="footer_content">
  <table class="footer-table"><tr>
    <td align="left">{left}</td>
    <td align="right">{right}</td>
  </tr></table>
</div>
"""


def fix_table_widths(html: str) -> str:
    """Give every table's columns explicit equal widths.

    xhtml2pdf sizes columns from the header cells, so an empty header cell
    (common in comparison tables) collapses its column to zero width and the
    cell text gets drawn overlapping the next column.
    """

    def fix_table(match: re.Match) -> str:
        table = match.group(0)
        header_row = re.search(r"<tr>.*?</tr>", table, flags=re.S)
        if not header_row:
            return table
        header_cells = re.findall(r"<th[^>]*>", header_row.group(0))
        if not header_cells:
            return table
        width = 100 / len(header_cells)
        fixed_row = re.sub(
            r"<th([^>]*)>",
            rf'<th\1 style="width:{width:.2f}%">',
            header_row.group(0),
        )
        return table.replace(header_row.group(0), fixed_row, 1)

    return re.sub(r"<table>.*?</table>", fix_table, html, flags=re.S)


def convert(
    input_path: Path,
    output_path: Path,
    footer_left: str = "Confidential",
    footer_right: str = "Sidwala Labs",
    footer: bool = True,
) -> None:
    """Read a Markdown file and write it out as a PDF."""
    md_text = input_path.read_text(encoding="utf-8")

    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "tables", "fenced_code", "sane_lists", "toc"],
    )
    html_body = fix_table_widths(html_body)

    css = CSS
    if footer:
        css += PAGE_CSS
        html_body += FOOTER_HTML.format(left=footer_left, right=footer_right)
    html = f"<html><head><style>{css}</style></head><body>{html_body}</body></html>"

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
    parser.add_argument(
        "--footer-left",
        default="Confidential",
        help='Text for the bottom-left of every page (default: "Confidential")',
    )
    parser.add_argument(
        "--footer-right",
        default="Sidwala Labs",
        help='Text for the bottom-right of every page (default: "Sidwala Labs")',
    )
    parser.add_argument(
        "--no-footer",
        action="store_true",
        help="Disable the page footer entirely",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        sys.exit(f"Error: input file not found: {input_path}")

    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")

    try:
        convert(
            input_path,
            output_path,
            footer_left=args.footer_left,
            footer_right=args.footer_right,
            footer=not args.no_footer,
        )
    except Exception as exc:
        sys.exit(f"Error: {exc}")

    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    main()
