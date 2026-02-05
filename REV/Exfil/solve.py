#!/usr/bin/env python3
from Crypto.Cipher import AES
import binascii

# SHA-256 of signing certificate
cert_sha256 = "c797e89761eadaba8c60dd66eabdfae32e532750b639dc3143a7f42a3091ccb3"
cert_hash = bytes.fromhex(cert_sha256)

# First 16 bytes as AES key
aes_key = cert_hash[:16]
print(f"AES Key: {aes_key.hex()}")

# Read the encrypted blob from R0.bin
with open("exfil_extracted/res/R0.bin", "rb") as f:
    blob = f.read()

print(f"Blob length: {len(blob)}")
print(f"Blob hex: {blob.hex()}")

# First 12 bytes are IV/nonce for GCM
iv = blob[:12]
ciphertext = blob[12:]

print(f"IV: {iv.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")

# Package name as AAD (Additional Authenticated Data)
package_name = "com.cit.ideh.exfil"
aad = package_name.encode('utf-8')

# AES-GCM decryption
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
cipher.update(aad)

try:
    # GCM tag is last 16 bytes of ciphertext
    plaintext = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
    print(f"\nDecrypted: {plaintext.decode('utf-8')}")
except Exception as e:
    print(f"Decryption error: {e}")
    # Try without verification
    cipher2 = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
    cipher2.update(aad)
    plaintext = cipher2.decrypt(ciphertext)
    print(f"Raw decrypt: {plaintext}")
