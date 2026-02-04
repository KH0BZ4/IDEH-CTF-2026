import base64
import csv

# We need to extend the known plaintext attack.
# Bytes 0-7: Signature (89 50 4E 47 0D 0A 1A 0A)
# Bytes 8-11: Chunk Length (00 00 00 0D)
# Bytes 12-15: Chunk Type (49 48 44 52 "IHDR")
# Bytes 16-19: Width (?)
# Bytes 20-23: Height (?)
# Bytes 24: Bit Depth (08?)
# Bytes 25: Color Type (02 Truecolor? 06 Truecolor+Alpha? 03 Indexed?)
# Bytes 26: Comp (00)
# Bytes 27: Filter (00)
# Bytes 28: Interlace (00)

known_pt = bytearray(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A') # 0-7
known_pt.extend(b'\x00\x00\x00\x0D') # 8-11
known_pt.extend(b'\x49\x48\x44\x52') # 12-15

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    # Get all binary data
    encrypted_data = bytearray()
    for i in range(31, len(rows)):
        try:
            encrypted_data.extend(base64.b64decode(rows[i]['Data']))
        except:
            pass

print(f"Total encrypted: {len(encrypted_data)}")

# Recover key stream
key_stream = bytearray()
for i in range(min(len(known_pt), len(encrypted_data))):
    k = encrypted_data[i] ^ known_pt[i]
    key_stream.append(k)

print(f"Recovered Key (Hex): {key_stream.hex()}")
print(f"Recovered Key (Ascii): {key_stream}")

# Let's analyze the key stream pattern
# 58 5b f3 78 45 0c 75 5f ...
# If we can guess the Width/Height, we can get more.
# 1626 bytes -> Small image. Maybe 50x50? Or 500x50?
# Common widths: 00 00 01 00 (256), 00 00 00 00 ...

# Let's look at the key stream we have so far (16 bytes).
# Key[0-7]: 58 5b f3 78 45 0c 75 5f
# Key[8-11]: ?
# Key[12-15]: ?

