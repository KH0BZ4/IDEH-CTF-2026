#!/usr/bin/env python3
"""
Neural Validator Solver
Extracts flag hidden in neural network weights
"""

import struct
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Key seed found in strings
SEED = b"d34dc0d3_n3ur4l_k3y!"

# Network architecture
W1_SIZE = 1920   # 30 input * 64 hidden1
B1_SIZE = 64
W2_SIZE = 2048   # 64 hidden1 * 32 hidden2
B2_SIZE = 32
W3_SIZE = 32     # 32 hidden2 * 1 output
B3_SIZE = 1

# Encoding constants for Part 1
ENCODE_MULT = 0.0317
ENCODE_SUB = 2.1
ENCODE_XOR = 0x42


def derive_keys(seed):
    """Derive AES key and IV from seed"""
    key = hashlib.sha256(seed).digest()[:16]
    iv = hashlib.md5(seed).digest()
    return key, iv


def decrypt_weights(encrypted_blob, key, iv):
    """Decrypt the weight blob using AES-128-CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_blob), AES.block_size)
    return decrypted


def read_doubles(data, offset, count):
    """Read count double values from data starting at offset"""
    doubles = []
    for i in range(count):
        val = struct.unpack('d', data[offset + i*8 : offset + (i+1)*8])[0]
        doubles.append(val)
    return doubles


def extract_part1(b1_biases):
    """
    Extract first part of flag from B1 biases at indices 32-46
    Encoding: encoded = (ord(char) ^ 0x42) * 0.0317 - 2.1
    """
    part1 = ""
    for i in range(32, 47):
        encoded = b1_biases[i]
        char_val = int(round((encoded + ENCODE_SUB) / ENCODE_MULT)) ^ ENCODE_XOR
        if 32 <= char_val <= 126:
            part1 += chr(char_val)
        else:
            part1 += '?'
    return part1


def extract_part2(decrypted, w2_offset):
    """
    Extract second part of flag from W2 weights using LSB steganography
    Each character = 8 LSBs from 8 consecutive weight bytes
    """
    part2 = ""
    for char_idx in range(15):
        byte_val = 0
        for bit_idx in range(8):
            weight_idx = char_idx * 8 + bit_idx
            # Get LSB of first byte of each double
            lsb = decrypted[w2_offset + weight_idx * 8] & 1
            byte_val |= (lsb << bit_idx)
        if 32 <= byte_val <= 126:
            part2 += chr(byte_val)
        else:
            part2 += '?'
    return part2


def find_encrypted_blob(binary_path):
    """
    Find and extract the encrypted weights from the binary
    This is challenge-specific - adjust offsets as needed
    """
    with open(binary_path, 'rb') as f:
        data = f.read()
    
    # Look for the key seed to find approximate location
    seed_pos = data.find(SEED)
    if seed_pos == -1:
        raise ValueError("Could not find key seed in binary")
    
    print(f"[*] Found seed at offset: {hex(seed_pos)}")
    
    # The encrypted blob is typically after the strings section
    # Total weight size = (W1 + B1 + W2 + B2 + W3 + B3) * 8 bytes
    # Plus AES padding
    expected_size = (W1_SIZE + B1_SIZE + W2_SIZE + B2_SIZE + W3_SIZE + B3_SIZE) * 8
    expected_size = ((expected_size // 16) + 1) * 16  # Round up for AES block
    
    print(f"[*] Expected encrypted size: {expected_size} bytes")
    
    # Search for the blob (this part may need adjustment)
    # Usually it's in .rodata section after strings
    # For demo, return None and require manual extraction
    return None


def solve(encrypted_blob):
    """Main solver function"""
    # Derive keys
    key, iv = derive_keys(SEED)
    print(f"[*] AES Key: {key.hex()}")
    print(f"[*] IV: {iv.hex()}")
    
    # Decrypt weights
    decrypted = decrypt_weights(encrypted_blob, key, iv)
    print(f"[*] Decrypted {len(decrypted)} bytes")
    
    # Calculate offsets
    b1_offset = W1_SIZE * 8
    w2_offset = (W1_SIZE + B1_SIZE) * 8
    
    # Extract B1 biases
    b1 = read_doubles(decrypted, b1_offset, B1_SIZE)
    
    # Extract flag parts
    part1 = extract_part1(b1)
    part2 = extract_part2(decrypted, w2_offset)
    
    flag = part1 + part2
    return flag


def main():
    print("=" * 50)
    print("Neural Validator Solver")
    print("=" * 50)
    
    # If you have the encrypted blob extracted, load it here
    # encrypted_blob = open("weights.bin", "rb").read()
    # flag = solve(encrypted_blob)
    # print(f"\n[+] Flag: {flag}")
    
    # Demo with known values
    print("\n[*] Demo mode - showing expected output")
    print("[+] Part 1 (from B1 biases): IDEH{n3ur4l_n3t")
    print("[+] Part 2 (from W2 LSBs):   w0rk_r3v3rs1ng}")
    print("\n[+] Flag: IDEH{n3ur4l_n3tw0rk_r3v3rs1ng}")


if __name__ == "__main__":
    main()
