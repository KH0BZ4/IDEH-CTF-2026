# Cipher - DFIR

- CTF: IDEH CTF 2026
- Category: DFIR
- Author: MrYou
- Solver: W4ST3D
- Flag: `IDEH{C00rd1n4t3_C1ph3r_Tr4ck1ng}`

---

## Challenge
> "We've intercepted communication logs from a suspected threat actor. The logs contain timestamps, coordinates, and encoded data. Something is hidden within this seemingly innocent tracking data.
>
> Analyze the patterns and decrypt the hidden message."

**Files:**
- `logs.csv`: CSV file containing timestamp, coordinates, Log_ID, and Base64-encoded data
- `flag.zip`: AES-encrypted ZIP file containing the flag

---

## Overview
This challenge involves analyzing a CSV log file containing GPS coordinates and encoded data. The coordinates encode a Vigenère cipher key, and the data field contains both text-based and binary-encoded information. The binary portion is an XOR-encrypted PNG image.

---

## Root Cause
The GPS coordinates in the log file encode information when quantized to grid positions. The Longitude and Latitude values map to specific characters that form a Vigenère key. This key decrypts the ZIP password.

---

## Exploitation Steps

### 1. Analyze the Log Structure
The CSV contains multiple encoded layers:
- Rows 1-31: Base64-encoded hex strings (text cipher)
- Rows 32+: Base64-encoded binary data (encrypted PNG)

```python
import csv
import base64

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
# Separate text and binary sections
text_data = [base64.b64decode(r['Data']).decode() for r in rows[:31]]
binary_data = b''.join([base64.b64decode(r['Data']) for r in rows[31:]])
```

### 2. Extract Key from Coordinates
The coordinates encode a Vigenère key when mapped to a grid:
```python
def coord_to_char(lat, lon):
    row_idx = 0 if lat > 20 else (1 if lat > 10 else 2)
    col_idx = round((lon - start_lon) / 7.5)
    # Map to alphabet character
    return chr(ord('A') + (row_idx * 10 + col_idx) % 26)

key = ''.join([coord_to_char(r['Latitude'], r['Longitude']) for r in rows])
# Key derived: QQECZZVRGYNNMUXOOCPPWPCBBNETZNN
```

### 3. Decrypt the PNG
The binary data is XOR-encrypted with an 8-byte key derived from the first 8 bytes XORed with PNG magic:
```python
keystream = [0x58, 0x5b, 0xf3, 0x78, 0x45, 0x0c, 0x75, 0x5f]

decrypted = bytearray()
for i, b in enumerate(binary_data):
    decrypted.append(b ^ keystream[i % 8])

with open('flag.png', 'wb') as f:
    f.write(decrypted)
```

### 4. Crack the ZIP Password
Using the Vigenère-derived key as the ZIP password:
```python
import pyzipper

password = "QQECZZVRGYNNMUXOOCPPWPCBBNETZNN"
with pyzipper.AESZipFile('flag.zip') as zf:
    zf.pwd = password.encode()
    zf.extractall("extracted_flag")
```

### 5. Result
The extracted flag.txt contains: `IDEH{C00rd1n4t3_C1ph3r_Tr4ck1ng}`
