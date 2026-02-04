import csv
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

coord_candidates = []

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    print("Reading coords...")
    for i, row in enumerate(reader):
        lat = row['Latitude (?)']
        lon = row['Longitude (?)']
        c_str = f"{lat},{lon}"
        c_str2 = f"{lat}{lon}"
        c_str3 = f"{lat} {lon}"
        coord_candidates.append(c_str)
        coord_candidates.append(c_str2)
        coord_candidates.append(c_str3)
        if i == 0:
            print(f"Row 1: {c_str}")
        if i == 31:
            print(f"Row 32: {c_str}")
            # Add Row 32 specific
            coord_candidates.append(f"inpt{c_str}")
            coord_candidates.append(f"IDEH{c_str}")

# Add b040 variations
b040 = "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7"
candidates = [
    b040,
    "IDEH{" + b040 + "}",
    "inpt" + b040,
    "inpt", "IDEH", "input", "Input",
    "IDEH{inpt}", "flag{inpt}",
    "coordinates", "Coordinates",
    "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV", # Binary coord string
    "QQECZZVRGYNNMUXOOCPPWPCBBNET", # Text coord string
]

# Coordinate patterns
# "inpt" + Coords?
for c in coord_candidates[:10]: # First 10 rows
    candidates.append(c)
    candidates.append(f"inpt{c}")
    candidates.append(f"IDEH{c}")

# Row 32 (Binary start) is important
candidates.append("0.03,112.49")
candidates.append("inpt0.03,112.49")
candidates.append("inpt(0.03,112.49)")

print(f"Candidates: {len(candidates)}")
for c in candidates:
    if try_zip(c):
        sys.exit(0)

print("Failed.")
