import { createHash } from "crypto"

const text = "Російський військовий корабель, іди нахуй"
const digest = createHash("sha384").update(text).digest("hex")
console.log(`Input:  ${text}`)
console.log(`SHA-384: ${digest}`)
