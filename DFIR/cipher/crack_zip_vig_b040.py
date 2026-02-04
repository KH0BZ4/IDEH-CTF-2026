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

# From previous step
candidates = [
    "i040`de0hi234a2`k4b0iee75ah7c42eh0k5d4e4eiy7i7g`7",
    "IDEH{i040`de0hi234a2`k4b0iee75ah7c42eh0k5d4e4eiy7i7g`7}",
    "IDEH{i040_de0hi234a2_k4b0iee75ah7c42eh0k5d4e4eiy7i7g_7}",
    "a040`jj0ea234g2`p4y0akj75xz7i42je0c5j4j4bae7n7d`7",
    "IDEH{a040`jj0ea234g2`p4y0akj75xz7i42je0c5j4j4bae7n7d`7}",
    "IDEH{a040_jj0ea234g2_p4y0akj75xz7i42je0c5j4j4bae7n7d_7}",
    "TEYB", "BYTE", "byte", "teyb"
]

print(f"Testing {len(candidates)}.")
for c in candidates:
    if try_zip(c):
        sys.exit(0)
print("Failed.")
