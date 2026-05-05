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
