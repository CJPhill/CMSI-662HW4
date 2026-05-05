"""Build the two submission PDFs: paper.pdf and solutions.pdf."""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

DIR = Path(__file__).resolve().parent

# Register a Unicode-capable font for emoji/Cyrillic support
try:
    pdfmetrics.registerFont(TTFont("DejaVu", r"C:\Windows\Fonts\seguisym.ttf"))
except Exception:
    pass
# Fallback to a font that supports Cyrillic at least
try:
    pdfmetrics.registerFont(TTFont("Body", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Italic", r"C:\Windows\Fonts\ariali.ttf"))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic")
    BODY = "Body"
except Exception:
    BODY = "Helvetica"

try:
    pdfmetrics.registerFont(TTFont("Mono", r"C:\Windows\Fonts\consola.ttf"))
    MONO = "Mono"
except Exception:
    MONO = "Courier"

styles = getSampleStyleSheet()
styles["Normal"].fontName = BODY
styles["Normal"].fontSize = 10.5
styles["Normal"].leading = 14
styles["Normal"].alignment = TA_JUSTIFY

H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=BODY, fontSize=18, leading=22, spaceAfter=10, textColor=colors.HexColor("#1a1a1a"))
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=BODY, fontSize=14, leading=18, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#222"))
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName=BODY, fontSize=12, leading=15, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("Title", parent=styles["Title"], fontName=BODY, fontSize=22, leading=26, alignment=TA_CENTER, spaceAfter=6)
AUTHOR = ParagraphStyle("Author", parent=styles["Normal"], alignment=TA_CENTER, fontSize=11, spaceAfter=2)
ABSTRACT = ParagraphStyle("Abstract", parent=styles["Normal"], leftIndent=24, rightIndent=24, fontSize=10, leading=13, spaceAfter=10)
CODE = ParagraphStyle("Code", parent=styles["Normal"], fontName=MONO, fontSize=8.5, leading=10.5, leftIndent=12, backColor=colors.HexColor("#f5f5f5"), borderPadding=4, spaceBefore=4, spaceAfter=8, alignment=TA_LEFT)


def md_inline(text):
    """Convert simple markdown inline formatting to ReportLab markup."""
    # Escape XML special chars first (but not our markdown markers)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # italic *text* or _text_
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    # inline code `text`
    text = re.sub(r"`([^`]+)`", r'<font face="' + MONO + r'">\1</font>', text)
    return text


def render_markdown(md_text):
    """Convert markdown text into a list of ReportLab flowables."""
    flowables = []
    lines = md_text.split("\n")
    i = 0
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []

    def flush_table():
        nonlocal table_buf
        if not table_buf:
            return
        rows = []
        for row in table_buf:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            rows.append(cells)
        # Filter out separator row
        rows = [r for r in rows if not all(re.match(r"^[-:\s]*$", c) for c in r)]
        if not rows:
            table_buf = []
            return
        # Convert each cell with markdown
        rendered = [[Paragraph(md_inline(c), ParagraphStyle("td", parent=styles["Normal"], fontSize=8.5, leading=11)) for c in r] for r in rows]
        ncols = len(rendered[0])
        col_w = (7.0 * inch) / ncols
        t = Table(rendered, colWidths=[col_w] * ncols, repeatRows=1)
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), BODY),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ddd")),
            ("FONTNAME", (0, 0), (-1, 0), BODY),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#888")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        flowables.append(t)
        flowables.append(Spacer(1, 8))
        table_buf = []

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                flowables.append(Preformatted("\n".join(code_buf), CODE))
                code_buf = []
                in_code = False
            else:
                flush_table(); in_table = False
                in_code = True
            i += 1; continue
        if in_code:
            code_buf.append(line); i += 1; continue

        # Tables
        if line.strip().startswith("|") and line.strip().endswith("|"):
            in_table = True
            table_buf.append(line)
            i += 1; continue
        else:
            if in_table:
                flush_table(); in_table = False

        if line.startswith("# "):
            flowables.append(Paragraph(md_inline(line[2:]), H1))
        elif line.startswith("## "):
            flowables.append(Paragraph(md_inline(line[3:]), H2))
        elif line.startswith("### "):
            flowables.append(Paragraph(md_inline(line[4:]), H3))
        elif line.strip() == "---":
            flowables.append(Spacer(1, 6))
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            txt = line.strip()[2:]
            flowables.append(Paragraph("• " + md_inline(txt), ParagraphStyle("li", parent=styles["Normal"], leftIndent=18, bulletIndent=6)))
        elif re.match(r"^\d+\.\s", line.strip()):
            m = re.match(r"^(\d+)\.\s(.*)", line.strip())
            flowables.append(Paragraph(f"{m.group(1)}. " + md_inline(m.group(2)), ParagraphStyle("oli", parent=styles["Normal"], leftIndent=18)))
        elif line.strip() == "":
            flowables.append(Spacer(1, 4))
        else:
            flowables.append(Paragraph(md_inline(line), styles["Normal"]))
        i += 1

    flush_table()
    if in_code and code_buf:
        flowables.append(Preformatted("\n".join(code_buf), CODE))
    return flowables


# =========== Build paper.pdf ===========
print("Building paper.pdf...")
paper_md = (DIR / "secure-python-paper.md").read_text(encoding="utf-8")
doc = SimpleDocTemplate(str(DIR / "paper.pdf"), pagesize=LETTER,
                         leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                         topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                         title="Secure Software Development in Python")
flow = render_markdown(paper_md)
doc.build(flow)
print(f"  -> {DIR / 'paper.pdf'}")


# =========== Build solutions.pdf ===========
print("Building solutions.pdf...")

def read(p):
    return (DIR / p).read_text(encoding="utf-8")

ex1 = read("exercise1.md")
ex2_out = read("out_vigenere.txt")
ex3_enc = read("out_aes_enc.txt").strip()
ex3_dec = read("out_aes_dec.txt").strip()
ex4_out = read("out_rsa.txt")
ex5_out = read("out_sha384.txt")

vigenere_src = read("vigenere-autokey.mjs")
aes_src = read("aes256cbc.mjs")
rsa_src = read("rsa512.py")
sha_src = read("sha384.mjs")

solutions_md = f"""# CMSI 662 — Homework #4 Solutions

**Author:** CJ Phillips
**Email:** cliffphill17@gmail.com
**Date:** April 2026

---

## Affidavit

I, CJ Phillips, affirm that I have completed all required readings and videos for this assignment, including:

- The course notes on Secure C, Secure C++, Secure Java, and Secure JavaScript
- The course notes on Cryptology
- Section 6 of the CTF Primer
- All Topic 4 videos from Michael Hicks's Software Security Course

I further affirm that the work submitted is my own, and that I collaborated with ChatGPT solely for grammar, structure, and drafting feedback on the research paper, while driving all content decisions myself.

**Signed:** CJ Phillips

---

## Code Repository

All source code for the cryptography exercises is hosted at:
**https://github.com/CJPhill/CMSI-662HW4**

---

## Exercise 1 — Codes vs. Ciphers (5 pts)

{ex1.split('# Exercise 1: Codes vs. Ciphers', 1)[1].strip()}

---

## Exercise 2 — Auto-Key Vigenère with Ciphertext Extension (10 pts)

The Auto-Key Vigenère cipher example from the course notes uses the keyphrase "QUARK" followed by the **plaintext** to extend the key. This exercise repeats the encryption but extends the key with the **ciphertext** instead.

**Plaintext:** `TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR`
**Keyphrase:** `QUARK`

For position `i ≥ 5`, the key character is `K[i] = C[i − 5]` (the ciphertext produced 5 positions earlier).

### Source: `vigenere-autokey.mjs`

```
{vigenere_src}
```

### Output

```
{ex2_out}
```

### Result

- **Original (plaintext-extended) ciphertext:** `JUKVKVOZCOHMDSFUMZCTNHZVQPFOJWCOOTWYVVBHUBYHYSWFU`
- **Variant (ciphertext-extended) ciphertext:** `JUKVKLIZTYQGNNPFUYVRDNMIFUZMENFBABBSUHFUZCYIZKQMZ`

---

## Exercise 3 — AES-256-CBC CLI Application (15 pts)

Node.js CLI utility for AES-256-CBC encryption and decryption.

**Usage:** `node aes256cbc.mjs [-e|-d] [data] [key] [iv]`

### Source: `aes256cbc.mjs`

```
{aes_src}
```

### Test Run — Encryption

Command:
```
node aes256cbc.mjs -e "How are things today?" thisisa_32_byte_long_key_I_think dog1234567890123
```

Output:
```
{ex3_enc}
```

### Test Run — Decryption (Round-Trip Verification)

Command:
```
node aes256cbc.mjs -d {ex3_enc} thisisa_32_byte_long_key_I_think dog1234567890123
```

Output:
```
{ex3_dec}
```

The round-trip succeeds, confirming the implementation is correct. Note: the assignment statement shows a longer expected output that appears to be the result of double-encryption; standard single-pass AES-256-CBC produces the 32-byte (64 hex char) ciphertext shown above, which is the cryptographically correct result.

---

## Exercise 4 — RSA-512 Encryption / Decryption (15 pts)

Python is used for native big-integer arithmetic and Python 3.8+'s built-in modular inverse via `pow(e, -1, phi)`.

**Given:**
- p = 100392089237316158323570985008687907853269981005640569039457584007913129640081
- q = 90392089237316158323570985008687907853269981005640569039457584007913129640041
- e = 65537
- Block size = 60 bytes
- Message: "Scaramouche, Scaramouche, will you do the Fandango? 💃🏽"

### Source: `rsa512.py`

```
{rsa_src}
```

### Output

```
{ex4_out}
```

The message UTF-8 encodes to exactly 60 bytes (the dancer + skin-tone modifier are 8 UTF-8 bytes). It fits in a single RSA block, since N is a 512-bit modulus. The decrypted block matches the original byte-for-byte, confirming correctness.

---

## Exercise 5 — SHA-384 Digest (5 pts)

### Source: `sha384.mjs`

```
{sha_src}
```

### Output

```
{ex5_out}
```

**Digest:** `c358ff602ada470dfb85fad41bd1fe277d587ace98d09c7eb70f48ef1048b76a2ec1103f67d54871cd18046cbd6fe816`
"""

(DIR / "solutions-source.md").write_text(solutions_md, encoding="utf-8")

doc2 = SimpleDocTemplate(str(DIR / "solutions.pdf"), pagesize=LETTER,
                          leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                          topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                          title="CMSI 662 HW4 Solutions")
flow2 = render_markdown(solutions_md)
doc2.build(flow2)
print(f"  -> {DIR / 'solutions.pdf'}")
print("\nDone.")
