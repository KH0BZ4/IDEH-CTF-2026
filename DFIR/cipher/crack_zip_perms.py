import pyzipper
import sys
import itertools

def try_zip(password):
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.pwd = password.encode()
            zf.extractall(pwd=password.encode())
            print(f"[+] Success! Password: {password}")
            return True
    except:
        return False

# Components
comps = [
    "inpt", "IDEH", "ideh", "Inpt", "input", "Input",
    "585bf378450c755fe6d608565cab79f2",
    "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV",
    "QQECZZVRGYNNMUXOOCPPWPCBBNET",
    "3aea192a83cbe4c18e2a382fd30f6ec28a5d9e2e732f6f91f",
    "a0b524c5d28d530c2425320504ef32af2b29d08776969a0e16"
]

candidates = set(comps)

# Pairs
for a, b in itertools.permutations(comps, 2):
    candidates.add(a + b)
    candidates.add(a + "_" + b)
    candidates.add(a + "-" + b)
    candidates.add("IDEH{" + a + "}")
    candidates.add("flag{" + a + "}")

# Triples with inpt/IDEH
for c in comps:
    candidates.add(f"IDEH{{inpt_{c}}}")
    candidates.add(f"IDEH{{inpt{c}}}")
    candidates.add(f"inpt{{IDEH_{c}}}")

print(f"Testing {len(candidates)} candidates.")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
