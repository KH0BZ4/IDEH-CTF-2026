import base64
import csv

# Derived from first 8 bytes ^ PNG Signature
key = [0x58, 0x5b, 0xf3, 0x78, 0x45, 0x0c, 0x75, 0x5f]

encrypted_data = bytearray()

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    # Binary blocks start at index 31 (Row 32)
    # But let's verification scan:
    # "YTBi..." is text (Row 1-31)
    # "0Qu9..." is binary? (Row 32)
    
    start_index = 31
    for i in range(start_index, len(rows)):
        payload = rows[i]['Data']
        try:
            block = base64.b64decode(payload)
            encrypted_data.extend(block)
        except:
            print(f"Failed to decode row {i}")

print(f"Total encrypted bytes: {len(encrypted_data)}")

# Decrypt
decrypted_data = bytearray()
for i in range(len(encrypted_data)):
    k = key[i % len(key)]
    decrypted_data.append(encrypted_data[i] ^ k)

# Save
with open('flag_attempt.png', 'wb') as f:
    f.write(decrypted_data)

print("Saved flag_attempt.png")
