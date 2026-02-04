from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import csv
import base64

# Key candidate
candidate_pass = "QQECZZVRGYNNMUXOOCPPWPCBBNET"

# The Data from the duplicate row (Row 30/31) could be IV?
# Hex: a0b524c5d28d530c2425320504ef32af2b29d08776969a0e16 (25 bytes)
# Take first 16 bytes.
iv_hex = "a0b524c5d28d530c2425320504ef32af"
iv = binascii.unhexlify(iv_hex)

# For key, maybe we need to pad to 32 bytes (AES-256) or 16 bytes (AES-128)?
# Or maybe use first 16/32 chars?
# Candidate pass is 28 chars.
# Let's try to pad with 0 or repeat?
keys = [
    candidate_pass.encode('utf-8').ljust(32, b'\0'),
    candidate_pass.encode('utf-8')[:16],
    candidate_pass.encode('utf-8')[:24], # AES-192
    ("IDEH{" + candidate_pass + "}").encode('utf-8')[:32],
    # Maybe use the SHA256 of the password?
]

# Read binary data (Row 32+)
binary_data = bytearray()
with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 31: # Row 32 is index 31
             try:
                 data = base64.b64decode(row['Data'])
                 # Skip if it is the duplicate row (Row 31, index 30 was K39..., Row 32 index 31 is BVSI...)
                 # Wait, Row 30 (index 29) & Row 31 (index 30) were the duplicates.
                 # Row 32 (index 31) is the first binary row (BVSI...).
                 binary_data.extend(data)
             except:
                 pass

print(f"Binary data len: {len(binary_data)}")

for key in keys:
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(binary_data)
        print(f"Key: {key}, Decrypted start: {decrypted[:20].hex()}")
        if decrypted[:4] == b'\x89PNG':
            print("FOUND PNG!")
            with open('flag.png', 'wb') as f:
                f.write(decrypted)
        elif decrypted[:2] == b'PK':
             print("FOUND ZIP!")
    except Exception as e:
        print(f"Error with key {key}: {e}")

# Try SHA256 of key
from Crypto.Hash import SHA256
h = SHA256.new()
h.update(candidate_pass.encode('utf-8'))
key_hash = h.digest()
try:
    cipher = AES.new(key_hash, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(binary_data)
    print(f"Key (SHA256): {key_hash.hex()}, Decrypted start: {decrypted[:20].hex()}")
    if decrypted[:4] == b'\x89PNG':
         with open('flag.png', 'wb') as f:
                f.write(decrypted)
         print("FOUND PNG with SHA256 key!")
except Exception as e:
    print(e)
