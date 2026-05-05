# CMSI 662 — Homework #4 Solutions

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

A **code** operates at the level of words or phrases, replacing entire meaningful units with substitute words, numbers, or symbols according to a **codebook**. For example, a codebook might map "attack at dawn" to "7291" or "bridge" to "FALCON." Both parties must possess the same codebook to communicate. Codes are linguistically dependent—they work on semantic units—and their security relies on keeping the codebook secret.

A **cipher**, by contrast, operates at the level of individual characters (or bits/bytes), transforming them systematically using a **mathematical algorithm** and a **key**. For example, a Caesar cipher shifts each letter by a fixed number of positions in the alphabet. Ciphers are language-independent and can encrypt any data, not just predefined words. Their security relies on the secrecy of the key, not the algorithm (Kerckhoffs's principle).

In summary: codes substitute meaning-level units via lookup; ciphers transform individual symbols via algorithm and key.

---

## Exercise 2 — Auto-Key Vigenère with Ciphertext Extension (10 pts)

The Auto-Key Vigenère cipher example from the course notes uses the keyphrase "QUARK" followed by the **plaintext** to extend the key. This exercise repeats the encryption but extends the key with the **ciphertext** instead.

**Plaintext:** `TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR`
**Keyphrase:** `QUARK`

For position `i ≥ 5`, the key character is `K[i] = C[i − 5]` (the ciphertext produced 5 positions earlier).

### Source: `vigenere-autokey.mjs`

```
const plaintext = "TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR"
const keyphrase = "QUARK"

function charToNum(c) {
  return c.charCodeAt(0) - 65
}

function numToChar(n) {
  return String.fromCharCode((n % 26 + 26) % 26 + 65)
}

function encryptAutoKey(plaintext, keyphrase, useCiphertext) {
  const key = []
  const ciphertext = []

  for (let i = 0; i < plaintext.length; i++) {
    let k
    if (i < keyphrase.length) {
      k = keyphrase[i]
    } else if (useCiphertext) {
      k = ciphertext[i - keyphrase.length]
    } else {
      k = plaintext[i - keyphrase.length]
    }
    key.push(k)
    const c = numToChar(charToNum(plaintext[i]) + charToNum(k))
    ciphertext.push(c)
  }

  return { key: key.join(""), ciphertext: ciphertext.join("") }
}

function printTable(label, plaintext, key, ciphertext) {
  console.log(`\n=== ${label} ===\n`)
  console.log("Pos | P | K | C")
  console.log("----|---|---|---")
  for (let i = 0; i < plaintext.length; i++) {
    console.log(
      `${String(i).padStart(3)} | ${plaintext[i]} | ${key[i]} | ${ciphertext[i]}`
    )
  }
  console.log(`\nKey:        ${key}`)
  console.log(`Plaintext:  ${plaintext}`)
  console.log(`Ciphertext: ${ciphertext}`)
}

// Original: plaintext-extended auto-key
const original = encryptAutoKey(plaintext, keyphrase, false)
printTable("Plaintext-Extended Auto-Key Vigenère", plaintext, original.key, original.ciphertext)

// Variant: ciphertext-extended auto-key
const variant = encryptAutoKey(plaintext, keyphrase, true)
printTable("Ciphertext-Extended Auto-Key Vigenère", plaintext, variant.key, variant.ciphertext)

```

### Output

```

=== Plaintext-Extended Auto-Key Vigenère ===

Pos | P | K | C
----|---|---|---
  0 | T | Q | J
  1 | A | U | U
  2 | K | A | K
  3 | E | R | V
  4 | A | K | K
  5 | C | T | V
  6 | O | A | O
  7 | P | K | Z
  8 | Y | E | C
  9 | O | A | O
 10 | F | C | H
 11 | Y | O | M
 12 | O | P | D
 13 | U | Y | S
 14 | R | O | F
 15 | P | F | U
 16 | O | Y | M
 17 | L | O | Z
 18 | I | U | C
 19 | C | R | T
 20 | Y | P | N
 21 | T | O | H
 22 | O | L | Z
 23 | N | I | V
 24 | O | C | Q
 25 | R | Y | P
 26 | M | T | F
 27 | A | O | O
 28 | W | N | J
 29 | I | O | W
 30 | L | R | C
 31 | C | M | O
 32 | O | A | O
 33 | X | W | T
 34 | O | I | W
 35 | N | L | Y
 36 | T | C | V
 37 | H | O | V
 38 | E | X | B
 39 | T | O | H
 40 | H | N | U
 41 | I | T | B
 42 | R | H | Y
 43 | D | E | H
 44 | F | T | Y
 45 | L | H | S
 46 | O | I | W
 47 | O | R | F
 48 | R | D | U

Key:        QUARKTAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRD
Plaintext:  TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR
Ciphertext: JUKVKVOZCOHMDSFUMZCTNHZVQPFOJWCOOTWYVVBHUBYHYSWFU

=== Ciphertext-Extended Auto-Key Vigenère ===

Pos | P | K | C
----|---|---|---
  0 | T | Q | J
  1 | A | U | U
  2 | K | A | K
  3 | E | R | V
  4 | A | K | K
  5 | C | J | L
  6 | O | U | I
  7 | P | K | Z
  8 | Y | V | T
  9 | O | K | Y
 10 | F | L | Q
 11 | Y | I | G
 12 | O | Z | N
 13 | U | T | N
 14 | R | Y | P
 15 | P | Q | F
 16 | O | G | U
 17 | L | N | Y
 18 | I | N | V
 19 | C | P | R
 20 | Y | F | D
 21 | T | U | N
 22 | O | Y | M
 23 | N | V | I
 24 | O | R | F
 25 | R | D | U
 26 | M | N | Z
 27 | A | M | M
 28 | W | I | E
 29 | I | F | N
 30 | L | U | F
 31 | C | Z | B
 32 | O | M | A
 33 | X | E | B
 34 | O | N | B
 35 | N | F | S
 36 | T | B | U
 37 | H | A | H
 38 | E | B | F
 39 | T | B | U
 40 | H | S | Z
 41 | I | U | C
 42 | R | H | Y
 43 | D | F | I
 44 | F | U | Z
 45 | L | Z | K
 46 | O | C | Q
 47 | O | Y | M
 48 | R | I | Z

Key:        QUARKJUKVKLIZTYQGNNPFUYVRDNMIFUZMENFBABBSUHFUZCYI
Plaintext:  TAKEACOPYOFYOURPOLICYTONORMAWILCOXONTHETHIRDFLOOR
Ciphertext: JUKVKLIZTYQGNNPFUYVRDNMIFUZMENFBABBSUHFUZCYIZKQMZ

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
import { createCipheriv, createDecipheriv } from "crypto"

const [mode, data, key, iv] = process.argv.slice(2)

if (!mode || !data || !key || !iv) {
  console.error("Usage: node aes256cbc.mjs [-e|-d] [data] [key] [iv]")
  process.exit(1)
}

const keyBuf = Buffer.from(key, "utf8")
const ivBuf = Buffer.from(iv, "utf8")

if (keyBuf.length !== 32) {
  console.error(`Key must be exactly 32 bytes (got ${keyBuf.length})`)
  process.exit(1)
}
if (ivBuf.length !== 16) {
  console.error(`IV must be exactly 16 bytes (got ${ivBuf.length})`)
  process.exit(1)
}

if (mode === "-e") {
  const cipher = createCipheriv("aes-256-cbc", keyBuf, ivBuf)
  const encrypted = cipher.update(data, "utf8", "hex") + cipher.final("hex")
  console.log(encrypted)
} else if (mode === "-d") {
  const decipher = createDecipheriv("aes-256-cbc", keyBuf, ivBuf)
  const decrypted = decipher.update(data, "hex", "utf8") + decipher.final("utf8")
  console.log(decrypted)
} else {
  console.error("Mode must be -e (encrypt) or -d (decrypt)")
  process.exit(1)
}

```

### Test Run — Encryption

Command:
```
node aes256cbc.mjs -e "How are things today?" thisisa_32_byte_long_key_I_think dog1234567890123
```

Output:
```
bd0886644bd5afa1857f50c582fc9c68e0e26be128eea3b009059e483ce5c238
```

### Test Run — Decryption (Round-Trip Verification)

Command:
```
node aes256cbc.mjs -d bd0886644bd5afa1857f50c582fc9c68e0e26be128eea3b009059e483ce5c238 thisisa_32_byte_long_key_I_think dog1234567890123
```

Output:
```
How are things today?
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
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

p = 100392089237316158323570985008687907853269981005640569039457584007913129640081
q = 90392089237316158323570985008687907853269981005640569039457584007913129640041
e = 65537
BLOCK_SIZE = 60

# Step 1: Compute N and phi(N)
N = p * q
phi = (p - 1) * (q - 1)

# Step 2: Compute private exponent d
d = pow(e, -1, phi)

print("=== RSA-512 Parameters ===")
print(f"p = {p}")
print(f"q = {q}")
print(f"e = {e}")
print(f"N = {N}")
print(f"d = {d}")

# Step 3: Encode message
message = "Scaramouche, Scaramouche, will you do the Fandango? 💃🏽"
message_bytes = message.encode("utf-8")
print(f"\nMessage: {message}")
print(f"Message bytes ({len(message_bytes)} bytes): {message_bytes.hex()}")

# Step 4: Split into blocks and encrypt
blocks = [message_bytes[i:i + BLOCK_SIZE] for i in range(0, len(message_bytes), BLOCK_SIZE)]
ciphertext_blocks = []

print(f"\n=== Encryption ({len(blocks)} block(s)) ===")
for i, block in enumerate(blocks):
    m = int.from_bytes(block, "big")
    c = pow(m, e, N)
    ciphertext_blocks.append(c)
    print(f"Block {i}: {hex(c)}")

# Step 5: Decrypt and verify
print("\n=== Decryption ===")
decrypted_bytes = b""
for i, c in enumerate(ciphertext_blocks):
    m = pow(c, d, N)
    block_bytes = m.to_bytes(BLOCK_SIZE, "big")
    decrypted_bytes += block_bytes
    print(f"Block {i}: {block_bytes.hex()}")

decrypted_message = decrypted_bytes.decode("utf-8")
print(f"\nDecrypted: {decrypted_message}")
print(f"Match: {decrypted_message == message}")

```

### Output

```
=== RSA-512 Parameters ===
p = 100392089237316158323570985008687907853269981005640569039457584007913129640081
q = 90392089237316158323570985008687907853269981005640569039457584007913129640041
e = 65537
N = 9074650689060089248199307400991055468098862103321403389047443270291029585149437412899788230307477461518354291801534660904940424431810965948411931416083321
d = 3440604854078842449902442746842634638010902628184540510109569714515334896803156693630578151012041316815494692897384029619755303913249828307540510260406273

Message: Scaramouche, Scaramouche, will you do the Fandango? 💃🏽
Message bytes (60 bytes): 53636172616d6f756368652c2053636172616d6f756368652c2077696c6c20796f7520646f207468652046616e64616e676f3f20f09f9283f09f8fbd

=== Encryption (1 block(s)) ===
Block 0: 0x1510726ec4756e595c4b5ce1f3a1974798a34369eb8f43f7462d4093f30973994849a5b63d6b28e33c2200bfea7f7005bd7642e74302832b739be60d966a926b

=== Decryption ===
Block 0: 53636172616d6f756368652c2053636172616d6f756368652c2077696c6c20796f7520646f207468652046616e64616e676f3f20f09f9283f09f8fbd

Decrypted: Scaramouche, Scaramouche, will you do the Fandango? 💃🏽
Match: True

```

The message UTF-8 encodes to exactly 60 bytes (the dancer + skin-tone modifier are 8 UTF-8 bytes). It fits in a single RSA block, since N is a 512-bit modulus. The decrypted block matches the original byte-for-byte, confirming correctness.

---

## Exercise 5 — SHA-384 Digest (5 pts)

### Source: `sha384.mjs`

```
import { createHash } from "crypto"

const text = "Російський військовий корабель, іди нахуй"
const digest = createHash("sha384").update(text).digest("hex")
console.log(`Input:  ${text}`)
console.log(`SHA-384: ${digest}`)

```

### Output

```
Input:  Російський військовий корабель, іди нахуй
SHA-384: c358ff602ada470dfb85fad41bd1fe277d587ace98d09c7eb70f48ef1048b76a2ec1103f67d54871cd18046cbd6fe816

```

**Digest:** `c358ff602ada470dfb85fad41bd1fe277d587ace98d09c7eb70f48ef1048b76a2ec1103f67d54871cd18046cbd6fe816`
