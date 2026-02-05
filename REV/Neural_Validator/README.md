# Neural Validator Writeup

![Challenge](challenge.png)

**Category:** Reverse Engineering  
**Difficulty:** Hard  
**Points:** 500

## Challenge Description

We get a binary called `neural_validator` that checks our input using a neural network.

## Solution

### First Look

Running the binary, it asks for a flag and says "Wrong!" for anything I tried:

```bash
$ ./neural_validator
Enter flag: test
Wrong!

$ ./neural_validator
Enter flag: IDEH{aaaaaaaaaaaaaaaaaaaaaaa}
Wrong!
```

So it expects exactly 30 characters. Let's see what's inside.

### Checking Strings

```bash
$ strings neural_validator | grep -E "IDEH|key|model"
d34dc0d3_n3ur4l_k3y!
IDEH{th1s_1s_n0t_th3_fl4g_l0l}
```

Found a fake flag lol. Nice try. But that `d34dc0d3_n3ur4l_k3y!` looks like a key for something.

### Reversing the Binary

Opened it in Ghidra. The binary:
1. Uses OpenSSL for crypto (SHA256, MD5, AES)
2. Has a big encrypted blob (~32KB)
3. Runs a neural network forward pass on our input

The network structure I found:
- Input: 30 neurons (one per flag character)
- Hidden layer 1: 64 neurons
- Hidden layer 2: 32 neurons  
- Output: 1 neuron

### Finding the Encryption Key

The binary derives the AES key from that string I found earlier:

```python
import hashlib

seed = b"d34dc0d3_n3ur4l_k3y!"
key = hashlib.sha256(seed).digest()[:16]  # First 16 bytes for AES-128
iv = hashlib.md5(seed).digest()            # MD5 as IV
```

### Decrypting the Weights

I extracted the encrypted blob from the binary (it's right after the string section) and decrypted it:

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher.decrypt(encrypted_blob), AES.block_size)
```

Now I have raw neural network weights. But wait... why would the flag be recoverable from just weights? Unless...

### The Flag is Hidden in the Weights!

After staring at the decrypted data for a while, I noticed two things:

**1. Layer 1 biases at indices 32-46 look weird**

Normal neural network weights are small random values. But these looked like encoded ASCII:

```python
import struct

# B1 starts after W1 (1920 doubles)
b1_offset = 1920 * 8
b1 = []
for i in range(64):
    val = struct.unpack('d', decrypted[b1_offset + i*8 : b1_offset + (i+1)*8])[0]
    b1.append(val)

# Values at 32-46 are suspiciously in a specific range
print(b1[32:47])
```

After some trial and error, I figured out the encoding:
```
encoded = (ord(char) ^ 0x42) * 0.0317 - 2.1
```

Reversing it:
```python
part1 = ""
for i in range(32, 47):
    char_val = int(round((b1[i] + 2.1) / 0.0317)) ^ 0x42
    part1 += chr(char_val)
print(part1)  # IDEH{n3ur4l_n3t
```

First half of the flag!

**2. W2 weights have something in their LSBs**

Classic steganography - hiding bits in the least significant bits of floating point numbers:

```python
w2_offset = (1920 + 64) * 8  # After W1 and B1

part2 = ""
for char_idx in range(15):
    byte_val = 0
    for bit_idx in range(8):
        weight_idx = char_idx * 8 + bit_idx
        lsb = decrypted[w2_offset + weight_idx * 8] & 1
        byte_val |= (lsb << bit_idx)
    part2 += chr(byte_val)
print(part2)  # w0rk_r3v3rs1ng}
```

Second half!

### Complete Solver

```python
#!/usr/bin/env python3
import struct
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# The key seed from strings
SEED = b"d34dc0d3_n3ur4l_k3y!"

# Network sizes
W1_SIZE = 1920  # 30 * 64
B1_SIZE = 64
W2_SIZE = 2048  # 64 * 32

# Encoding constants (found through reversing)
MULT = 0.0317
SUB = 2.1
XOR = 0x42

def solve(binary_path):
    # Read binary and find encrypted weights
    # (You need to find the offset in your binary)
    with open(binary_path, 'rb') as f:
        data = f.read()
    
    # Extract encrypted blob (offset depends on binary)
    # encrypted_blob = data[OFFSET:OFFSET+SIZE]
    
    # Derive keys
    key = hashlib.sha256(SEED).digest()[:16]
    iv = hashlib.md5(SEED).digest()
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_blob), AES.block_size)
    
    # Parse B1 biases
    b1_offset = W1_SIZE * 8
    b1 = []
    for i in range(B1_SIZE):
        val = struct.unpack('d', decrypted[b1_offset + i*8 : b1_offset + (i+1)*8])[0]
        b1.append(val)
    
    # Part 1: Decode from B1[32:47]
    part1 = ""
    for i in range(32, 47):
        char_val = int(round((b1[i] + SUB) / MULT)) ^ XOR
        part1 += chr(char_val)
    
    # Part 2: LSB stego from W2
    w2_offset = (W1_SIZE + B1_SIZE) * 8
    part2 = ""
    for char_idx in range(15):
        byte_val = 0
        for bit_idx in range(8):
            weight_idx = char_idx * 8 + bit_idx
            lsb = decrypted[w2_offset + weight_idx * 8] & 1
            byte_val |= (lsb << bit_idx)
        part2 += chr(byte_val)
    
    return part1 + part2

if __name__ == "__main__":
    flag = solve("neural_validator")
    print(f"Flag: {flag}")
```

### Anti-Debug Bypass

The binary has some anti-analysis tricks:
- Checks `TracerPid` in `/proc/self/status`
- Timing checks to detect stepping
- Fake flag in strings

You can patch these out or just do static analysis like I did.

### Alternative Method: Z3 Solver

If you want to solve it properly through the neural network (not just extracting from weights), you could use Z3:

```python
from z3 import *

# Create symbolic input
flag = [BitVec(f'c{i}', 8) for i in range(30)]

# Add constraints
s = Solver()
for i, c in enumerate(flag):
    s.add(c >= 32, c <= 126)  # Printable ASCII

# Add constraint that flag starts with IDEH{
s.add(flag[0] == ord('I'))
s.add(flag[1] == ord('D'))
s.add(flag[2] == ord('E'))
s.add(flag[3] == ord('H'))
s.add(flag[4] == ord('{'))
s.add(flag[29] == ord('}'))

# Implement neural network forward pass symbolically
# ... (complex, but possible)

# Add constraint that output > 0.5
# s.add(output > 0.5)

if s.check() == sat:
    m = s.model()
    print(''.join(chr(m[c].as_long()) for c in flag))
```

But honestly, extracting from weights is way easier.

## Flag

```
IDEH{n3ur4l_n3tw0rk_r3v3rs1ng}
```

## What I Learned

- Neural network weights can hide data in multiple ways
- Biases are good spots for encoded data (people focus on weights)
- LSB steganography works on floats too
- Always check for fake flags in strings
- The "key" to crypto is often nearby in the binary

Cool challenge - first time I've seen ML used as a hiding mechanism in RE!
