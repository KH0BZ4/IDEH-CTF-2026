import pyzipper
import sys

def try_zip(password):
    if not password: return False
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.pwd = password.encode()
            zf.extractall(pwd=password.encode())
            print(f"[+] Success! Password: {password}")
            return True
    except:
        return False

candidates = [
    "inpt",
    "IDEH",
    "inpt / IDEH/",
    "inpt / IDEH",
    "inpt/IDEH",
    "inptIDEH",
    "IDEHinpt",
    "ideh inpt",
    "ideh/inpt",
    "a0b524c5d28d530c2425320504ef32af2b29d08776969a0e16"
]

print(f"Testing {len(candidates)} specific candidates.")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
