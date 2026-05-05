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
