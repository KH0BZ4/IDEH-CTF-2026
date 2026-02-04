import base64
import csv
import hashlib

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = bytearray()
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return out

def xor(key, data):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    # Row 32
    row = rows[31]
    payload = base64.b64decode(row['Data'])
    log_id = row['Log_ID'] # CT_LOG_BVSI3V3O6R
    
    parts = log_id.split('_')
    key_cand = parts[2] if len(parts) > 2 else log_id
    
    print(f"Trying key: {key_cand} for row 32")
    
    # Try RC4
    res = rc4(key_cand.encode(), payload)
    print(f"RC4 Res: {res[:8].hex()}")
    
    # Try XOR
    res_xor = xor(key_cand.encode(), payload)
    print(f"XOR Res: {res_xor[:8].hex()}")
    
    # Try RC4 with Full Log ID
    res_full = rc4(log_id.encode(), payload)
    print(f"RC4 Full: {res_full[:8].hex()}")
