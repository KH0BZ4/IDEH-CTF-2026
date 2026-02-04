import pyzipper
import sys

def try_zip(password):
    if not password: return False
    try:
        with pyzipper.AESZipFile('flag.zip') as zf:
            zf.extractall(pwd=password.encode())
            print(f"[+] Success! Password: {password}")
            return True
    except:
        return False

pws = [
    "IDPJRMGYYLYUEHIVGPAWOCNITAPA",
    "idpjrmgyylyuehivgpawocnitapa",
    "IDEH{IDPJRMGYYLYUEHIVGPAWOCNITAPA}",
    "IDEH{idpjrmgyylyuehivgpawocnitapa}",
    "PLTSBIGIGDOHSQLIEZCJTLJTACOHPKPULGFVSQIC",
    "pltsbigigdohsqliezcjtljtacohpkpulgfvsqic",
    "IDEH{PLTSBIGIGDOHSQLIEZCJTLJTACOHPKPULGFVSQIC}"
]

for p in pws:
    if try_zip(p):
        sys.exit(0)

print("Failed.")
