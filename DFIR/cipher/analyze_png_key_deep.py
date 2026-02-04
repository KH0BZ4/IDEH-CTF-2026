import pandas as pd
import base64

# Standard PNG Signature
png_sig = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

# Load Data
df = pd.read_csv('logs.csv')

# Binary starts at index 31 (Row 32)
data_rows = df.iloc[31:].reset_index(drop=True)

print(f"Total binary rows: {len(data_rows)}")

print("\nAnalysis of first 8 bytes:")
print(f"IDX | Log_ID | Lat | Lon | EncByte | SigByte | KeyByte | KeyChar")

recovered_key = []

for i in range(8):
    row = data_rows.iloc[i]
    b64_data = row['Data']
    encrypted_bytes = base64.b64decode(b64_data)
    
    # We assume 1 byte per row contributes to the stream?
    # No, the rows contain blocks of data.
    # The previous `recover_key.py` took the FIRST byte of the FIRST row?
    # No, let's check `recover_key.py` logic.
    
    # Wait, `recover_key.py` isn't in my recent memory, let me check the file content if possible or just assume standard stream behavior.
    # If the file is 1626 bytes and we have ~40 rows. 1626/40 = 40 bytes per row.
    # So the *first row* contains the *entire* signature (8 bytes).
    # So the key `58 5b ...` is derived entirely from the *first row* (Row 32).
    
    # Aha! The key changes *within* the row?
    # Or is it a repeating key?
    # If it's a repeating key, then `Key[0..7]` applies to `Data[0..7]`.
    # Does `Key[8]` continue the pattern?
    
    pass

# Let's extract the first row's full data and analyze it against the signature key.
row0 = data_rows.iloc[0]
data0 = base64.b64decode(row0['Data'])
print(f"Row 0 (Index 31) derived key (first 8 bytes):")
key_segment = []
for i in range(8):
    k = data0[i] ^ png_sig[i]
    key_segment.append(k)
    print(f"Byte {i}: Data={hex(data0[i])} ^ Sig={hex(png_sig[i])} = Key={hex(k)} ('{chr(k) if 32<=k<127 else '.'}')")

print(f"\nKey Segment (Hex): {bytes(key_segment).hex()}")

# Now let's look at the Log_ID for this row.
log_id = row0['Log_ID']
print(f"Log_ID: {log_id}")

# Log_ID is "CT_LOG_BVSI3V3O6R"
# Key is "585bf378450c755f"
# 'X' (58), '[' (5b) ...
# 'B' (42) ... no match.

# What about the Coordinate Cipher for THIS row?
# Lat 0.03, Lon 112.49.
# Analyze_plaintext said 'X'.
# Key[0] is 'X'.

# Is the key just the coordinate character REPEATED?
# If Key was "XXXXXXXX...", then Sig[1] 'P' (50) ^ Key 'X' (58) = 0x08.
# Actual Data[1] = 0x0b.
# Derived Key[1] = 0x5b.
# So Key is NOT just 'X'.

# Is the key the sequence of coordinate characters for the *previous* rows?
# Row 32 -> Uses Key from Row 32? (Which is X)
# But Row 32 has typically 40 bytes.
# Does it use Lat/Lon from Row 32, 33, 34... for bytes 0, 1, 2?
# Let's check.
# Byte 0: Row 32 Coords -> 'X'. Key 'X'. Match.
# Byte 1: Row 33 Coords -> 'Y'. Key '['. (0x59 vs 0x5b).
# Byte 2: Row 34 Coords -> 'I'. Key 0xf3. (0x49 vs 0xf3).
# Byte 3: Row 35 Coords -> 'L'. Key 0x78. (0x4c vs 0x78).

# Let's check if the coordinates for Row 32+ simply ENCODE the key directly?
# As in, the Lat/Lon *values* themselves are the key?
# Lat 0.03. Key 0x58.
# Lon 112.49. Key 0x5b?
# Lat 25.03. Key 0xf3?
# The rows are:
# 32 (Byte 0?)
# 33 (Byte 1?)
# But Row 32 contains MANY bytes.
# Why would Row 33's coordinate affect Byte 1 of Row 32?
# Unless the CSV structure is misleading and each row is actually 1 byte?
# No, `Total encrypted bytes: 1626`. Rows ~40.
# So each row is a chunk.

# Hypothesis: The Key is generated from the coordinates of the *message* rows (1-31).
# We have 31 characters: "QQECZZVRGYNNMUXOOCPPWPCBBNET"
# String length 31 (wait, user said 28 chars? 31 rows... let's count).
# `QQECZZVRGYNNMUXOOCPPWPCBBNET`. Len: 28?
# Let's count characters.
# Q Q E C Z Z V R (8)
# G Y N N M U X O (8)
# O C P P W P C B (8)
# B N E T (4)
# Total 28.
# Rows 1-28?
# But we had 31 rows of text.
# The `analyze_plaintext.py` output had rows 1-31.
# Row 31 (N).
# Let's check `analyze_plaintext.py` output again.
# Row 31: N.
# Row 30: N.
# Row 29: Z.
# ...
# The `QQEC...` string might be truncated or I miscounted.

# Let's try to use the derived `QQEC...` string as a Vigenere Key or XOR key for the PNG.
# Key Length 31 or 28.
# We have `QQE...`.
# Byte 0 (Key 'X'): 'Q' (51) ^ ? = 58. ? = 9.
# Byte 1 (Key '['): 'Q' (51) ^ ? = 5b. ? = a.
# Byte 2 (Key 0xf3): 'E' (45) ^ ? = f3. ? = b6.

# Let's try to determine the key length.
# If it's repeating.
# We have a large amount of data.
# We can use the IHDR chunk structure to guess more key bytes.
# PNG Header: 8 bytes.
# Chunk 1 (IHDR):
# Length: 00 00 00 0D (4 bytes).
# Type: 49 48 44 52 "IHDR" (4 bytes).
# Width: 4 bytes.
# Height: 4 bytes.
# Bit depth: 1 byte.
# Color type: 1 byte.
# Compression: 1 byte.
# Filter: 1 byte.
# Interlace: 1 byte.
# CRC: 4 bytes.

# Total IHDR is 13 data + 12 overhead = 25 bytes.
# Plus 8 signature = 33 bytes.
# We can recover ~33 bytes of key if we assume standard IHDR values.
# Width/Height might be unknown, but Type is known ("IHDR").
# Length is almost always 13 for IHDR.

