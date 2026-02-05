# Frozen Truth Writeup

![Challenge](challenge.png)

**Category:** Reverse Engineering  
**Difficulty:** Easy / Beginner  
**Format:** PyInstaller (Python executable)

## Challenge Description

You are given a single executable built using **PyInstaller**.
The goal is to recover the hidden flag.
The flag is **not stored in plaintext**. Instead, it is encoded and reconstructed at runtime.

---

## Method 1 — PyInstaller Extraction + Decompilation

### Step 1 — Identify the binary

Run basic file inspection:

```bash
file frozen_truth
strings -n 6 frozen_truth | head
```

You should observe:
- ELF executable
- PyInstaller bootloader strings
- No obvious plaintext flag

This indicates a **PyInstaller one-file binary**.

### Step 2 — Extract the PyInstaller archive

Use `pyinstxtractor.py`:

```bash
python3 pyinstxtractor.py frozen_truth
```

This creates a directory:

```
frozen_truth_extracted/
 ├── challenge.pyc
 ├── pyiboot01_bootstrap.pyc
 ├── PYZ.pyz
 └── ...
```

The interesting file is `challenge.pyc`.

### Step 3 — Decompile the Python bytecode

Because the binary was built using **Python 3.8**, standard tools work correctly:

```bash
uncompyle6 frozen_truth_extracted/challenge.pyc
```

This produces readable Python source code.

### Step 4 — Analyze the decoding logic

From the decompiled output:

```python
SHIFT = 3

def decode(data):
    out = bytearray()
    for b in data:
        out.append(b - SHIFT)
    return out.decode("utf-8")

encoded_flag = [
    76, 71, 72, 75, 126,
    102, 114, 112, 115, 108, 111, 108, 113, 106, 98,
    122, 108, 58, 107, 98,
    115, 124, 108, 113, 118, 58, 100, 111, 111, 54, 117, 98,
    108, 118, 98,
    113, 114, 58, 98,
    118, 54, 102, 120, 117, 54,
    128
]
```

This is a classic **Caesar shift** - each byte was encoded as `ord(character) + 3`.

### Step 5 — Recover the flag

```python
encoded_flag = [
    76, 71, 72, 75, 126,
    102, 114, 112, 115, 108, 111, 108, 113, 106, 98,
    122, 108, 58, 107, 98,
    115, 124, 108, 113, 118, 58, 100, 111, 111, 54, 117, 98,
    108, 118, 98,
    113, 114, 58, 98,
    118, 54, 102, 120, 117, 54,
    128
]

flag = ''.join(chr(b - 3) for b in encoded_flag)
print(flag)
```

---

## Method 2 — Dynamic Analysis (Memory Dump)

If you don't want to extract and decompile, you can catch the flag at runtime.

### Step 1 — Run with ltrace/strace

Since the program prints the decoded flag, we can trace it:

```bash
ltrace ./frozen_truth 2>&1 | grep -i ideh
```

Or simply run and capture output:

```bash
./frozen_truth
```

If the flag is printed, you get it directly!

### Step 2 — Using GDB to dump memory

If the flag isn't printed but exists in memory:

```bash
gdb ./frozen_truth
```

```gdb
(gdb) run
# Let it initialize, then Ctrl+C
(gdb) info proc mappings
(gdb) find /b 0x00000000, 0x7fffffff, 'I', 'D', 'E', 'H'
(gdb) x/s <address_found>
```

### Step 3 — Python trace hook

Create a wrapper that hooks the decode function:

```python
import sys
import importlib.util

# Load the extracted challenge module
spec = importlib.util.spec_from_file_location("challenge", "frozen_truth_extracted/challenge.pyc")
module = importlib.util.module_from_spec(spec)

# Trace all function returns
def trace_calls(frame, event, arg):
    if event == 'return' and 'IDEH' in str(arg):
        print(f"[FOUND] {arg}")
    return trace_calls

sys.settrace(trace_calls)
spec.loader.exec_module(module)
```

---

## Method 3 — Direct Bytecode Analysis (No Decompiler)

If `uncompyle6` fails, you can read bytecode directly.

### Step 1 — Disassemble the .pyc

```python
import dis
import marshal

with open("frozen_truth_extracted/challenge.pyc", "rb") as f:
    f.read(16)  # Skip header (Python 3.8+)
    code = marshal.load(f)

dis.dis(code)
```

### Step 2 — Look for LOAD_CONST with the encoded list

In the disassembly output, look for:

```
LOAD_CONST    ([76, 71, 72, 75, 126, ...])
```

### Step 3 — Extract constants programmatically

```python
import marshal

with open("frozen_truth_extracted/challenge.pyc", "rb") as f:
    f.read(16)
    code = marshal.load(f)

# Find all list constants
for const in code.co_consts:
    if isinstance(const, tuple) and len(const) > 10:
        if all(isinstance(x, int) and 50 < x < 130 for x in const):
            print("Found encoded flag:", list(const))
            # Try Caesar shift
            for shift in range(1, 10):
                try:
                    flag = ''.join(chr(b - shift) for b in const)
                    if 'IDEH' in flag:
                        print(f"Shift {shift}: {flag}")
                except:
                    pass
```

---

## Method 4 — Brute Force from Strings

Even without extraction, the encoded bytes might appear in strings output.

### Step 1 — Dump all printable strings

```bash
strings -n 10 frozen_truth > all_strings.txt
```

### Step 2 — Look for number sequences

```bash
grep -oE '\[([0-9]+,\s*)+[0-9]+\]' all_strings.txt
```

### Step 3 — Try common encodings on any arrays found

```python
import re

with open("all_strings.txt") as f:
    content = f.read()

# Find number arrays
arrays = re.findall(r'\[[\d,\s]+\]', content)

for arr in arrays:
    nums = [int(x) for x in re.findall(r'\d+', arr)]
    if len(nums) > 20:
        # Try shifts 1-10
        for shift in range(1, 10):
            try:
                decoded = ''.join(chr(n - shift) for n in nums)
                if 'IDEH' in decoded or 'FLAG' in decoded.upper():
                    print(f"Found with shift {shift}: {decoded}")
            except:
                pass
```

---

## Flag

```
IDEH{compiling_wi7h_pyins7all3r_is_no7_s3cur3}
```

---

## Summary

| Method | Pros | Cons |
|--------|------|------|
| Extract + Decompile | Clean, readable source | Requires working decompiler |
| Dynamic/Memory | Works when decompilers fail | Need execution environment |
| Bytecode Analysis | No external tools needed | More complex |
| Brute Force Strings | Quick and dirty | May not always work |

The challenge teaches:
- PyInstaller extraction
- `.pyc` decompilation
- Basic encoding reversal
- Alternative RE approaches when standard tools fail
