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
        # print(f"[-] Failed: {password} ({e})")
        return False

# Base string
s = "QQECZZVRGYNNMUXOOCPPWPCBBNET"

candidates = [
    s,
    s.lower(),
    "IDEH{" + s + "}",
    "IDEH{" + s.lower() + "}",
    "flag{" + s + "}",
    "flag{" + s.lower() + "}"
]

for c in candidates:
    if try_zip(c):
        sys.exit(0)
        
print("Paper candidates failed.")
