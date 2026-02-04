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

raw = "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7"
candidates = [
    raw,
    raw.replace("`", ""),
    raw.replace("`", "_"),
    "IDEH{" + raw.replace("`", "") + "}",
    "IDEH{" + raw + "}",
]

print(f"Testing {len(candidates)} cleaned candidates.")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
