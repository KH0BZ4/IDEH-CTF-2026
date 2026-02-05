# Blue Horizon Writeup

![Challenge](challenge.png)

**Category:** Reverse Engineering  
**Points:** 300  
**Solves:** 3

## Challenge Description

> Checkpoint A then checkpoint B
> 
> Patch it and you get a decoy, reverse it to recover the flag.

## Solution

So we got an ELF binary called `Horizon`. The description is interesting - it says if we patch it we get a decoy. That means we need to actually reverse it properly.

### First Look

I opened the binary in my decompiler and started looking at the main function. The program takes a license key either from command line or asks for input. Then it does some processing on our input and runs it through something called `vm_run()`.

Looking deeper, I found there are two VM runs - this matches the "Checkpoint A then checkpoint B" hint. If both checkpoints pass, it decrypts and prints something.

### The VM

The binary has a custom virtual machine with different opcodes. It can do stuff like:
- Basic operations (XOR, ADD, SUB, rotations)
- Jumps and conditional jumps
- Memory read/write
- Some crypto-like operations

There's also a `digest256()` function which is a custom hash, and `xtea_dec()` for XTEA decryption.

### Finding the Trap

I tried patching the binary to skip the VM checks at first. When I did that, I got this output:

```
IDEH{vm_patch_prints_this_fake}
```

Lol nice try. This is the decoy flag they mentioned. So patching won't work here.

### The Real Approach

Looking at the code more carefully, I noticed something interesting. When both checkpoints pass, the program:

1. Takes the hash output from checkpoint B
2. Uses it to derive an XTEA key
3. Decrypts the real flag with that key

The key thing is - the expected hash values are hardcoded in the binary! I found them in the `.rodata` section:

```
At 0x403380: 3ce6fc09 14b72e8f cdf3a27c 3e7c5f4e
At 0x403390: a009cc1c cc96f686 deb573d4 95423a73
```

### Getting the Flag

So I don't need to find an input that passes the VM checks. I can just use the expected hash values directly to derive the XTEA key and decrypt the flag!

The key derivation from the code does some XOR and rotations on the hash values:

```python
key[0] = hash_part2[0] ^ hash_part1[1]
key[1] = hash_part1[2] + hash_part2[1]
key[2] = ROL(hash_part1[3], 13) ^ hash_part2[2]
key[3] = ROL(hash_part1[0], 7) + hash_part2[3]
```

The encrypted flag is at offset `0x4032f8` in the binary.

### Solve Script

```python
#!/usr/bin/env python3
import struct

def rol32(val, n):
    n = n & 31
    return ((val << n) | (val >> (32 - n))) & 0xffffffff

def xtea_dec(v, key):
    v0, v1 = v
    sum_val = 0xC6EF3720
    
    for _ in range(32):
        k_idx = (sum_val >> 11) & 3
        v1 = (v1 - ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (key[k_idx] + sum_val))) & 0xffffffff
        sum_val = (sum_val + 0x61c88647) & 0xffffffff
        k_idx = sum_val & 3
        v0 = (v0 - ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (key[k_idx] + sum_val))) & 0xffffffff
    
    return v0, v1

# expected hash values from the binary
var_4c8 = struct.unpack('<IIII', bytes.fromhex("3ce6fc0914b72e8fcdf3a27c3e7c5f4e"))
var_4d8 = struct.unpack('<IIII', bytes.fromhex("a009cc1ccc96f686deb573d495423a73"))

# derive the XTEA key
key = [
    var_4d8[0] ^ var_4c8[1],
    (var_4c8[2] + var_4d8[1]) & 0xffffffff,
    rol32(var_4c8[3], 13) ^ var_4d8[2],
    (rol32(var_4c8[0], 7) + var_4d8[3]) & 0xffffffff
]

# encrypted flag from the binary
encrypted = bytes.fromhex(
    "f7537fee56feb53fc5d303bb2f256531"
    "a035bcdd5d74245c460e27448e0d4d62"
    "e605540d639c7155"
)

# decrypt it
result = []
for i in range(0, len(encrypted), 8):
    block = encrypted[i:i+8]
    if len(block) == 8:
        v0, v1 = struct.unpack('<II', block)
        d0, d1 = xtea_dec((v0, v1), key)
        result.extend([d0, d1])

flag = b''.join(struct.pack('<I', x) for x in result).split(b'\x00')[0]
print(f"Flag: {flag.decode()}")
```

Running it:

```
$ python3 solve.py
Flag: IDEH{H0pe_y0u_enj0y3d_s33_u_n3xt_year}
```

## Flag

```
IDEH{H0pe_y0u_enj0y3d_s33_u_n3xt_year}
```

Cool challenge! The anti-patching trick was nice - it makes you actually understand what's happening instead of just NOPing out the checks.
