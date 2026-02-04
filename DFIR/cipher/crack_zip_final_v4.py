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

candidates = [
    "inpt", "IDEH", "ideh", "Inpt",
    "inptIDEH", "IDEHinpt", "inpt_IDEH", "IDEH_inpt",
    "inpt-IDEH", "IDEH-inpt",
    "inpt/IDEH", "IDEH/inpt", "inpt / IDEH", "IDEH / inpt",
    "IDEH{inpt}", "flag{inpt}", "inpt{IDEH}",
    "coordinates", "Coordinates",
    "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7", # Raw
    "b040hc0ib234e2i4c0bic75ba7g42ci0d5h4c4fbc7g7h7", # Clean
    "IDPJRMGYYLYUEHIVGPAWOCNITAPA", # Vig
    "PLTSBIGIGDOHSQLIEZCJTLJTACOHPKPULGFVSQIC", # Vig Bin
    "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV", # Bin Coords
    "QQECZZVRGYNNMUXOOCPPWPCBBNET", # Text Coords
    "TIDP", "SIDO", "SUDO", "shadow", "side channel",
    "BVSI3V3O6R", "CT_LOG_BVSI3V3O6R",
    "X[\xf3xE\x0cu_\xe6\xd6\x08V\\\xaby\xf2",
    "585bf378450c755fe6d608565cab79f2",
    "24.97657,0.03848",
    "0.02672,112.49352"
]

# Add more simple ones
candidates.extend(["inpt" + str(i) for i in range(10)])
candidates.extend(["IDEH" + str(i) for i in range(10)])

print(f"Testing {len(candidates)}.")
for c in candidates:
    if try_zip(c):
        sys.exit(0)
    # Try with 'IDEH{' wrapper for all
    if try_zip("IDEH{" + c + "}"):
        sys.exit(0)

print("Failed.")
