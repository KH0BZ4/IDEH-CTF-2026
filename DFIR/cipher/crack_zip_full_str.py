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

# Full extracted coordinate string
s = "QQECZZVRGYNNMUXOOCPPWPCBBNETXYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"
s_bin = "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"

candidates = [
    s,
    s.lower(),
    "IDEH{" + s + "}",
    "flag{" + s + "}",
    "IDEH{" + s_bin + "}",
    "inpt" + s_bin,
    "inpt_" + s_bin,
    s_bin + "inpt",
]

print(f"Testing {len(candidates)} full string candidates.")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
