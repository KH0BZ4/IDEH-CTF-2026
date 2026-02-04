import pandas as pd
import base64

# Try decrypting PNG with repeating string "inpt", "IDEH", "XYIL..." etc.
key_strs = [
    "inpt", "IDEH", "ideh", "Inpt",
    "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV", # Bin coord
    "QQECZZVRGYNNMUXOOCPPWPCBBNET", # Text coord
    "PLTSBIGIGDOHSQLIEZCJTLJTACOHPKPULGFVSQIC", # Vig(inpt) of Bin
    "IDPJRMGYYLYUEHIVGPAWOCNITAPA", # Vig(inpt) of Text
    "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7",
    "a0b524c5d28d530c2425320504ef32af2b29d08776969a0e16"
]

encrypted_data = bytearray()
df = pd.read_csv('logs.csv')
for i in range(31, len(df)):
    try:
        encrypted_data.extend(base64.b64decode(df.iloc[i]['Data']))
    except: pass

print(f"Encrypted data: {len(encrypted_data)} bytes")

for k_str in key_strs:
    # Try XOR
    key_bytes = k_str.encode()
    dec = bytearray()
    for i in range(len(encrypted_data)):
        dec.append(encrypted_data[i] ^ key_bytes[i % len(key_bytes)])
    
    start = dec[:16].hex()
    # print(f"Key {k_str[:10]}... Start: {start}")
    if dec.startswith(b'\x89PNG'):
        print(f"MATCH XOR! Key: {k_str}")
        with open(f"flag_xor_{k_str[:5]}.png", "wb") as f:
            f.write(dec)
            
    # Try RC4
    # (Reuse RC4 func from before if needed, or import)
    pass
