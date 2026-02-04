# Emotional Encryption - Crypto

- CTF: IDEH CTF 2026
- Category: Crypto
- Solver: W4ST3D
- Flag: `IDEH{Em0j1_Encrypt10n_1s_N0t_S3cur3}`

---

## Challenge
> "We intercepted a private communication from Nemesis. He seems to have developed his own language to bypass our keyword filters.
>
> At first glance, it looks like a meaningless sequence of emojis. But we know Nemesis is a logical being. He always starts from an origin point, a Smiling Face with Horns (😈), and transforms his thoughts using a simple 3 digits numeric key.
>
> Decipher this dialect to uncover what he is hiding."

**Files:**
- `message_emoji.txt`: The intercepted encrypted message

---

## Overview
This challenge involves a custom emoji-based encryption scheme. Each character in the flag is encoded as an emoji by calculating an offset from a base character (😈 - "Smiling Face with Horns") and XORing with a numeric key.

---

## Root Cause
The encryption uses a simple XOR cipher with a fixed 3-digit key applied to unicode offsets. Since the flag format `IDEH{` is known, we can derive the key through known-plaintext attack.

---

## Exploitation Steps

### 1. Analyze the Encryption Scheme
The emojis in the message file are encoded based on their unicode distance from the origin emoji (😈). The encryption formula is:
```
emoji_codepoint = origin_codepoint + (char_ascii ^ key)
```

### 2. Derive the Key
Using the known flag prefix `IDEH{`, we can reverse-engineer the key by XORing the expected ASCII values with the observed unicode offsets:
```python
origin = ord('😈')  # 128520
# From first emoji offset and 'I' (73), derive key
key = (emoji_offset) ^ ord('I')
```

### 3. Decrypt the Message
```python
def analyze():
    with open('message_emoji.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    origin = ord('😈')
    key = 239  # Derived from IDEH{
    
    decoded = ""
    for c in content:
        diff = ord(c) - origin
        char_code = diff ^ key
        decoded += chr(char_code)
        
    print(f"Decoded: {decoded}")

if __name__ == '__main__':
    analyze()
```

### 4. Result
Running the solver reveals the flag: `IDEH{Em0j1_Encrypt10n_1s_N0t_S3cur3}`
