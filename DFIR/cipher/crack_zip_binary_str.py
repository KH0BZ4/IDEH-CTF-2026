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

s = "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"
candidates = [
    s,
    s.lower(),
    "IDEH{" + s + "}",
    "flag{" + s + "}"
]

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
