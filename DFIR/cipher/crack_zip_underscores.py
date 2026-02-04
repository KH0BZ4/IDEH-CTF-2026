import pyzipper
import sys

def try_zip(password):
    if not password: return False
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.setpassword(password.encode())
            if zf.testzip() is None:
                print(f"[+] Success! Password: {password}")
                zf.extractall(pwd=password.encode())
                return True
    except:
        return False

raw = "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7"
candidates = [
    raw.replace("`", "_"),
    "IDEH{" + raw.replace("`", "_") + "}",
    "IDEH{" + raw.replace("`", "-") + "}",
    "IDEH{" + raw.replace("`", "") + "}",
]

print(f"Testing {len(candidates)} underscore candidates.")
for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
