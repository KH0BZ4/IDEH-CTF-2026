# XORCEPTIOn - Crypto

- CTF: IDEH CTF 2026
- Category: Crypto
- Author: Unknown
- Solver: W4ST3D
- Flag: `IDEH{X0R_M4G1C_K3Y_R3V34L5}`

---

## Challenge
> "XOR is simple, but can you see through the layers?"

**Files:**
- `challenge.bin`: Encrypted binary file

---

## Overview
As the name suggests, this challenge involves XOR encryption. The encrypted file is a PNG image XORed with a repeating key. Using known-plaintext attack with the PNG file signature, we can recover the key.

---

## Root Cause
The encryption uses a short repeating XOR key. Since PNG files have a known 8-byte magic header (`89 50 4E 47 0D 0A 1A 0A`), we can use this as a known-plaintext to recover the key.

---

## Exploitation Steps

### 1. Identify File Type
Analyzing the encrypted binary, we hypothesize it's a PNG based on the file size and context.

### 2. Known Plaintext Attack
Use the PNG magic bytes to recover the XOR key:
```python
file_bytes = bytes.fromhex("c4647a006449573e3447694e047c701569434b0134476ac74532344769aa6087")
png_header = bytes.fromhex("89504E470D0A1A0A")

key = []
for f, p in zip(file_bytes, png_header):
    key.append(f ^ p)

print(f"Key: {bytes(key)}")  # Reveals: M44GiC
```

### 3. Decrypt the Image
```python
def xor_data(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

key = b"M44GiC"

with open("challenge.bin", "rb") as f:
    encrypted_data = f.read()

decrypted_data = xor_data(encrypted_data, key)

# Verify PNG signature
png_sig = b"\x89PNG\r\n\x1a\n"
if decrypted_data.startswith(png_sig):
    print("Valid PNG signature found!")
    with open("output.png", "wb") as f:
        f.write(decrypted_data)
    print("Decrypted image saved to output.png")
```

### 4. Result
The decrypted PNG image contains the flag: `IDEH{X0R_M4G1C_K3Y_R3V34L5}`
