# MD-to-PDF

A simple Python script that converts a Markdown file into a PDF.

It converts your Markdown to HTML (with support for tables, fenced code
blocks, and other common extensions), applies clean default styling, and
renders the result as a PDF — no external system tools (like wkhtmltopdf or
LaTeX) required.

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt`:
  - [markdown](https://pypi.org/project/Markdown/) — Markdown → HTML conversion
  - [xhtml2pdf](https://pypi.org/project/xhtml2pdf/) — HTML → PDF rendering

## Installation

```bash
git clone https://github.com/siddhu2395/MD-to-PDF.git
cd MD-to-PDF
pip install -r requirements.txt
```

> Tip: use a virtual environment to keep dependencies isolated:
>
> ```bash
> python -m venv .venv
> source .venv/bin/activate   # On Windows: .venv\Scripts\activate
> pip install -r requirements.txt
> ```

## Usage

Convert a Markdown file (the PDF is written next to it with the same name):

```bash
python md_to_pdf.py notes.md
# -> PDF created: notes.pdf
```

Specify a custom output path:

```bash
python md_to_pdf.py notes.md output/my-document.pdf
```

Show help:

```bash
python md_to_pdf.py --help
```

### Page footer

Every page gets a footer with **Confidential** on the bottom-left and
**Sidwala Labs** on the bottom-right. You can customize or disable it:

```bash
# Custom footer text
python md_to_pdf.py notes.md --footer-left "Internal Use Only" --footer-right "Acme Corp"

# No footer at all
python md_to_pdf.py notes.md --no-footer
```

## Supported Markdown features

- Headings, paragraphs, **bold** / _italic_ text
- Bullet and numbered lists
- Links
- Inline code and fenced code blocks
- Blockquotes
- Tables

## Example

Given `sample.md`:

```markdown
# My Document

Some **bold** text and a list:

- item one
- item two
```

Run:

```bash
python md_to_pdf.py sample.md
```

This produces `sample.pdf` in the same directory.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'markdown'` (or `xhtml2pdf`)** —
  run `pip install -r requirements.txt` in the environment you're using.
- **Input file not found** — check the path you passed; relative paths are
  resolved from your current working directory.
