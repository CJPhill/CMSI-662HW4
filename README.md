# CMSI 662 — Homework #4

**Author:** CJ Phillips
**Course:** CMSI 662 — Secure Software Development
**Due:** April 14, 2026

This repository contains the source code, paper, and submission PDFs for Homework #4.

## Submission PDFs

| File | Description |
|------|-------------|
| [`paper.pdf`](paper.pdf) | Research paper: *Secure Software Development in Python* |
| [`solutions.pdf`](solutions.pdf) | Solutions to the five cryptography exercises, with affidavit |

## Cryptography Exercises (Source)

| File | Exercise | Language |
|------|----------|----------|
| [`exercise1.md`](exercise1.md) | 1. Codes vs. Ciphers | Markdown |
| [`vigenere-autokey.mjs`](vigenere-autokey.mjs) | 2. Auto-Key Vigenère with ciphertext extension | Node.js |
| [`aes256cbc.mjs`](aes256cbc.mjs) | 3. AES-256-CBC CLI application | Node.js |
| [`rsa512.py`](rsa512.py) | 4. RSA-512 encrypt / decrypt | Python |
| [`sha384.mjs`](sha384.mjs) | 5. SHA-384 digest | Node.js |

## Running the Exercises

Requires Node.js (v18+) and Python (3.8+).

```bash
# Exercise 2 — Auto-Key Vigenère
node vigenere-autokey.mjs

# Exercise 3 — AES-256-CBC
node aes256cbc.mjs -e "How are things today?" thisisa_32_byte_long_key_I_think dog1234567890123
node aes256cbc.mjs -d <hex-ciphertext> thisisa_32_byte_long_key_I_think dog1234567890123

# Exercise 4 — RSA-512
python rsa512.py

# Exercise 5 — SHA-384
node sha384.mjs
```

## Other Files

- [`secure-python-paper.md`](secure-python-paper.md) — Markdown source of the paper
- [`build_pdfs.py`](build_pdfs.py) — Builds `paper.pdf` and `solutions.pdf` from Markdown (requires `reportlab`)
- `out_*.txt` — Captured outputs from running each exercise
- `solutions-source.md` — Generated Markdown source for `solutions.pdf`