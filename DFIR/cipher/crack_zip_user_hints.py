import pyzipper
import sys
import itertools

def try_zip(password):
    if not password: return False
    # Print progress for debugging long lists
    # print(f"Trying: {password}") 
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.pwd = password.encode()
            zf.extractall(pwd=password.encode())
            print(f"[+] Success! Password: {password}")
            return True
    except Exception as e:
        return False

# Base candidates
bases = [
    "inpt", "IDEH", "input", "Input", "Inpt", "ideh", "Ideh",
    "585bf378450c755fe6d608565cab79f2", # Recovered PNG key
    "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV", # Binary coord string
    "QQECZZVRGYNNMUXOOCPPWPCBBNET", # Text coord string
    "3aea192a83cbe4c18e2a382fd30f6ec28a5d9e2e732f6f91f", # Hex string
    "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7", # Decrypted hex
]

# Generate combinations
candidates = []
candidates.extend(bases)

# IDEH{...} format
for b in bases:
    candidates.append(f"IDEH{{{b}}}")
    candidates.append(f"ideh{{{b}}}")
    candidates.append(f"flag{{{b}}}")

# Combinations of "inpt" and strings
for s in [bases[2], bases[3]]: # Cord strings
    candidates.append(f"inpt{s}")
    candidates.append(f"IDEH{s}")
    candidates.append(f"{s}inpt")
    candidates.append(f"{s}IDEH")

# Key bytes raw?
# candidates.append(bytes.fromhex("585bf378450c755fe6d608565cab79f2").decode('latin-1'))

print(f"Testing {len(candidates)} candidates...")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
