# Key analysis
key_bytes = bytes.fromhex("585bf378450c755fe6d608565cab79f2")
# Length 16.

# Let's check for repetition.
# Is Key[0] == Key[8]?
# 58 vs e6. No.
# Is Key[0] == Key[16]? (We don't have 16 yet).

# Let's check if the coordinate string matches this 16 byte sequence.
# String: "QQECZZVRGYNNMUXOOCPPWPCBBNET"
# Chars:
# 0: Q (51)
# 1: Q (51)
# 2: E (45)
# ...

# Key[i] ^ String[i] = ?
# 0: 58 ^ 51 = 09
# 1: 5b ^ 51 = 0a
# 2: f3 ^ 45 = b6
# 3: 78 ^ 43 ('C') = 3b
# 4: 45 ^ 5a ('Z') = 1f
# 5: 0c ^ 5a ('Z') = 56
# 6: 75 ^ 56 ('V') = 23
# 7: 5f ^ 52 ('R') = 0d

# 09 0a b6 3b 1f 56 23 0d. No obvious pattern.

# Let's try decryption with the 16 bytes REPEATED.
import csv
import base64

key = bytes.fromhex("585bf378450c755fe6d608565cab79f2")

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
    decrypted.append(encrypted_data[i] ^ key[i % len(key)])

with open('flag_16bytecheck.png', 'wb') as f:
    f.write(decrypted)

print("Saved flag_16bytecheck.png")
