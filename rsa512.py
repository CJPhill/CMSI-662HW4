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
