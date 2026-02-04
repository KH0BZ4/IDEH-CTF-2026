import base64
import csv

key_str = "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"
key_bytes = key_str.encode()

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

decrypted = bytearray()
for i in range(len(encrypted_data)):
    decrypted.append(encrypted_data[i] ^ key_bytes[i % len(key_bytes)])

# Check for PNG signature
print(f"Decrypted start: {decrypted[:8].hex()}")
if decrypted.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
    print("MATCH!")
    with open('flag_xor_binary.png', 'wb') as f:
        f.write(decrypted)
else:
    print("No match.")
