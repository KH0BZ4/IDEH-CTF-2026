import csv
import base64

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    
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
    
    return bytes(out)

candidates = [
    b"QQECZZVRGYNNMUXOOCPPWPCBBNET",
    b"ZNNXYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV",
    b"QQECZZVRGYNNMUXOOCPPWPCBBNETZNNXYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV",
]

# We know the first few bytes of binary data decrypted to 89 50 4E 47 with SOME key.
# But we need to find the REAL key for the WHOLE file.
# The binary content starts at Row 32.
binary_data = bytearray()
with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
         if i >= 31: # Skip text part
             try:
                 binary_data.extend(base64.b64decode(row['Data']))
             except: pass

# Try to decrypt binary data with candidates
for k in candidates:
    dec = rc4(k, binary_data)
    print(f"Key: {k[:10]}... Decrypted: {dec[:16].hex()}")
    if dec.startswith(b'\x89PNG'):
        print("FOUND PNG!")
        with open('solved.png', 'wb') as f:
            f.write(dec)

# Note: In previous test, "QQEC..." key decrypted to 49c2... which is NOT 8950.
# Wait, I tested "QQEC..." and it matched?
# My previous output:
# Target: 89504e470d0a1a0a
# Key QQECZZVRGY... : 49c2d84f20277741
# Key Z1L432QE... : 24164ed65a8d6c7f
# ...
# NONE matched 8950!

# So RC4 with that key is WRONG.
# The user said "ive already tested the flag its wrong".
# The key might be derived differently.

# What if the key is "Cipher-C"?
# Or "MrYou"?
# The challenge mentions "MrYou".

# Let's try Vigenere on the Coordinate String.
# Ciphertext: QQECZZVRGYNNMUXOOCPPWPCBBNET
# Key: MrYou
# Q (16) - M (12) = 4 (E)
# Q (16) - r (17) = -1 (Z)
# E (4) - Y (24) = -20 (G) ...
# Let's write a script.

