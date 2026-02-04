import pyzipper
import sys
import csv

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

candidates = [
    "inpt", "IDEH", "inptIDEH", "IDEHinpt", "inpt_IDEH", "inpt-IDEH",
    "IDEH{inpt}", "flag{inpt}", "inpt{IDEH}",
    "coordinates", "Coordinates", "LatitudeLongitude",
    "CipherC", "Cipher-C", "MrYou",
    "585bf378450c755fe6d608565cab79f2", # Key hex
    "X[\xf3xE\x0cu_\xe6\xd6\x08V\\\xaby\xf2", # Key ascii
    # Coordinates for Row 32: 0.03, 112.49
    "0.03,112.49", "0.03112.49", "112.490.03",
    # Log ID Row 32
    "CT_LOG_BVSI3V3O6R", "BVSI3V3O6R",
    # Row 32 Data (Base 64)
]

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    if len(rows) > 31:
        r32 = rows[31]
        candidates.append(r32['Data'])
        candidates.append(r32['Log_ID'])
        candidates.append(str(r32['Latitude (?)']) + str(r32['Longitude (?)']))
        candidates.append(str(r32['Longitude (?)']) + str(r32['Latitude (?)']))

        # Try all Log IDs just in case
        for r in rows:
            candidates.append(r['Log_ID'])

print(f"Candidates count: {len(candidates)}")

for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
