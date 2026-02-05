#!/usr/bin/env python3
import struct

def rol32(val, n):
    n = n & 31
    return ((val << n) | (val >> (32 - n))) & 0xffffffff

def ror32(val, n):
    n = n & 31
    return ((val >> n) | (val << (32 - n))) & 0xffffffff

def xtea_dec(v, key):
    """XTEA decryption - 32 rounds"""
    v0, v1 = v
    delta = 0x9E3779B9
    # Starting sum for decryption (after 32 rounds of encryption)
    # The code shows: for i = -0x3910c8e0; i; i += 0x61c88647
    # -0x3910c8e0 = 0xc6ef3720 (unsigned), which is 32*delta
    sum_val = 0xC6EF3720
    
    for _ in range(32):
        # Decrypt in reverse order
        # rcx -= ((rsi << 4 ^ rsi >> 5) + rsi) ^ rdi_1;  where rdi_1 = key[(sum>>11)&3] + sum
        # rsi -= ((rcx << 4 ^ rcx >> 5) + rcx) ^ (key[sum&3] + sum);
        # sum += 0x61c88647  (which is -delta in 32-bit)
        
        k_idx = (sum_val >> 11) & 3
        v1 = (v1 - ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (key[k_idx] + sum_val))) & 0xffffffff
        sum_val = (sum_val + 0x61c88647) & 0xffffffff  # This is equivalent to sum -= delta
        k_idx = sum_val & 3
        v0 = (v0 - ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (key[k_idx] + sum_val))) & 0xffffffff
    
    return v0, v1

# From the rodata dump:
# data_4033a0 (decoy XTEA key): d4c3b2a1 88776655 0df0ad0b 37133713
decoy_key = [0xa1b2c3d4, 0x55667788, 0x0badf00d, 0x13371337]

# Encrypted decoy flag at 0x3020 (from "i`2L" pattern seen in code)
# The code copies from "i`2L" which is at offset 0x3020
encrypted_decoy = bytes.fromhex(
    "6960324c9b5866508645d4be8d00a6d4"
    "e213e9cfd5b08e1c7e921303c037d182"
    "00000000000000000000000000000000"
    "00000000000000000000000000000000"
)

# Let's decrypt the decoy flag
print("=== Decoy Flag (what you get by patching) ===")
decoy_result = []
for i in range(0, 64, 8):
    block = encrypted_decoy[i:i+8]
    if len(block) == 8:
        v0, v1 = struct.unpack('<II', block)
        d0, d1 = xtea_dec((v0, v1), decoy_key)
        decoy_result.extend([d0, d1])

decoy_bytes = b''.join(struct.pack('<I', x) for x in decoy_result)
print(f"Decoy: {decoy_bytes}")

# Now for the REAL flag
# The real flag uses a key derived from the hash output
# Looking at the code:
# zmm0_3 = var_4d8 ^ *(&var_4c8 + 4);
# rax_21 = *(&var_4c8 + 8) + *(&var_4d8 + 4);
# temp0_58 = (ROLD(*(&var_4c8 + 0xc), 0xd) ^ *(&var_4d8 + 8), ROLD(var_4c8, 7) + *(&var_4d8 + 0xc))
# var_508 = unpacklo(unpacklo(zmm0_3, rax_21), temp0_58)

# The encrypted real flag is at data_4032f8
# f7537fee 56feb53f c5d303bb 2f256531 a035bcdd 5d74245c 460e2744 8e0d4d62 e605540d 639c7155
encrypted_real = bytes.fromhex(
    "f7537fee56feb53fc5d303bb2f256531"
    "a035bcdd5d74245c460e27448e0d4d62"
    "e605540d639c7155"
)

# The hash values we need to match for checkpoint B:
# data_403380: 3ce6fc09 14b72e8f cdf3a27c 3e7c5f4e
# data_403390: a009cc1c cc96f686 deb573d4 95423a73
hash_b_expected = bytes.fromhex("3ce6fc0914b72e8fcdf3a27c3e7c5f4ea009cc1ccc96f686deb573d495423a73")

# For checkpoint A:
# data_403350: 7627a569 67c16050 af0daf1b 4cdf102d
# data_403360: d1d09a58 85c09e23 fa0584a3 ef8a78f6
hash_a_expected = bytes.fromhex("7627a56967c16050af0daf1b4cdf102dd1d09a5885c09e23fa0584a3ef8a78f6")

print("\n=== Analyzing the real flag decryption ===")
print(f"Hash A expected: {hash_a_expected.hex()}")
print(f"Hash B expected: {hash_b_expected.hex()}")

# The key for real flag XTEA comes from var_4c8/var_4d8 (the digest256 output)
# If we pass checkpoint B, the hash should equal hash_b_expected

# Let's work backwards from the hash
# var_4c8 and var_4d8 together form a 32-byte hash
# The expected values are at data_403380/data_403390

var_4c8 = struct.unpack('<IIII', bytes.fromhex("3ce6fc0914b72e8fcdf3a27c3e7c5f4e"))
var_4d8 = struct.unpack('<IIII', bytes.fromhex("a009cc1ccc96f686deb573d495423a73"))

print(f"\nvar_4c8: {[hex(x) for x in var_4c8]}")
print(f"var_4d8: {[hex(x) for x in var_4d8]}")

# Key derivation from the decompiled code:
# zmm0_3 = var_4d8[0] ^ var_4c8[1]
# rax_21 = var_4c8[2] + var_4d8[1]
# temp0_58[0] = ROLD(var_4c8[3], 13) ^ var_4d8[2]
# temp0_58[1] = ROLD(var_4c8[0], 7) + var_4d8[3]

key0 = var_4d8[0] ^ var_4c8[1]
key1 = (var_4c8[2] + var_4d8[1]) & 0xffffffff
key2 = rol32(var_4c8[3], 13) ^ var_4d8[2]
key3 = (rol32(var_4c8[0], 7) + var_4d8[3]) & 0xffffffff

real_key = [key0, key1, key2, key3]
print(f"\nDerived XTEA key: {[hex(x) for x in real_key]}")

# Now decrypt the real flag
print("\n=== Real Flag ===")
real_result = []
for i in range(0, len(encrypted_real), 8):
    block = encrypted_real[i:i+8]
    if len(block) == 8:
        v0, v1 = struct.unpack('<II', block)
        d0, d1 = xtea_dec((v0, v1), real_key)
        real_result.extend([d0, d1])

real_bytes = b''.join(struct.pack('<I', x) for x in real_result)
# Print until null
flag = real_bytes.split(b'\x00')[0]
print(f"Flag: {flag.decode('utf-8', errors='replace')}")
print(f"Raw: {real_bytes.hex()}")
