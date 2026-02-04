# The 16 byte key produced "invalid" dimensions/bitdepth (negative numbers).
# This means bytes 16-24 (Width, Height, BitDepth) were NOT decrypted correctly with the repeating key.
# This implies the key is longer than 16 bytes.
# Or not repeating.

# But we only Recovered the key for bytes 0-15 (Signature + Length + Type).
# Length (0-3), Type (4-7) relative to chunk start. (Bytes 8-15 absolute).
# Bytes 0-7 absolute (Sig) used Key[0-7].
# Bytes 8-15 absolute (Len+Type) used Key[8-15].

# We need bytes 16-31.
# Bytes 16-19: Width. 
# Bytes 20-23: Height.
# Bytes 24: BitDepth.
# Bytes 25: ColorType.
# Bytes 26: Comp.
# Bytes 27: Filter.
# Bytes 28: Interlace.
# Bytes 29-32: CRC.

# If we assume meaningful Width/Height, we can guess the key.
# Common Widths:
# 500 (0x00 00 01 F4).
# 100 (0x00 00 00 64).
# 800 (0x00 00 03 20).
# Usually Start 00 00 ...

# Let's extract Encrypted Bytes 16-31.
import base64
import csv

encrypted_data = bytearray()
with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    for i in range(31,len(rows)):
        try:
            encrypted_data.extend(base64.b64decode(rows[i]['Data']))
        except:
            pass

enc_16_31 = encrypted_data[16:32]
print(f"Encrypted 16-31: {enc_16_31.hex()}")

# Assume Width starts with 00 00
# Key[16] = Enc[16] ^ 00 = Enc[16].
# Key[17] = Enc[17] ^ 00 = Enc[17].
# Assume Height starts with 00 00
# Key[20] = Enc[20] ^ 00 = Enc[20].
# Key[21] = Enc[21] ^ 00 = Enc[21].

# This gives use Key 16, 17, 20, 21.
# Let's check if they match Key 0, 1?
# Or Key 0, 1, 4, 5?
