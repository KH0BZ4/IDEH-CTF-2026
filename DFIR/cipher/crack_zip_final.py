import pyzipper
import sys

def try_zip(password):
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.pwd = password.encode()
            zf.extractall(pwd=password.encode())
            print(f"[+] Success! Password: {password}")
            return True
    except Exception as e:
        return False

# Key derived from Header and IHDR
key_bytes = bytes.fromhex("585bf378450c755fe6d608565cab79f2")
candidates = [
    key_bytes.decode('latin-1'),
    key_bytes.hex(),
    "585bf378450c755f",
    "IDEH{585bf378450c755f}",
    "IDEH{e6d608565cab79f2}",
    "MrYou",
    "Cipher-C",
    "CipherC",
    "Coordinates",
    "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7",
    "3aea192a83cbe4c18e2a382fd30f6ec28a5d9e2e732f6f91f"
]

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Final attempt failed.")
