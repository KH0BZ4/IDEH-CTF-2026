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

candidates = [
    "585bf378450c755f",
    "X[\xf3xE\x0cu_",
    "X[\xf3xE\x0cu_",
    "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7",
    "QQECZZVRGYNNMUXOOCPPWPCBBNET",
    "CT_LOG_BVSI3V3O6R",
    "BVSI3V3O6R",
    "K39NRZHB"
]

for c in candidates:
    if try_zip(c):
        sys.exit(0)
    # Also clean hex
    if try_zip(c.replace("`", "")):
        sys.exit(0)

print("Failed.")
