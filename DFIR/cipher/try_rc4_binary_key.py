import base64
import csv

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = bytearray()

    # KSA
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    
    return out

# Get binary data
encrypted_data = bytearray()
with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    for i in range(31, len(rows)):
        try:
            encrypted_data.extend(base64.b64decode(rows[i]['Data']))
        except:
            pass

key_str = "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"
key_bytes = key_str.encode()

decrypted = rc4(key_bytes, encrypted_data)

# Check for PNG signature
print(f"Key: {key_str}")
print(f"Decrypted start: {decrypted[:8].hex()}")
if decrypted.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
    print("MATCH!")
    with open('flag_rc4_binary.png', 'wb') as f:
        f.write(decrypted)
else:
    print("No match.")
