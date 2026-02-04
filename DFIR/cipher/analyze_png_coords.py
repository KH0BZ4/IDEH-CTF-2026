import pandas as pd
import struct

def get_keyboard_char(lat, lon):
    # Keyboard layout
    keyboard = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ]
    
    # Latitude determines row (approx)
    # Row 0 (QWERTY...): Lat ~ 25
    # Row 1 (ASDF...): Lat ~ 12.5?
    # Row 2 (ZXCV...): Lat ~ 0
    
    if lat > 20:
        row_idx = 0
    elif lat > 10:
        row_idx = 1
    else:
        row_idx = 2
        
    # Longitude determines column
    # Step 7.5
    # -124.X -> 0
    # -116.X -> 1
    # ...
    
    # Base longitudes for index 0:
    # Q: -124.12
    # A: -123.67
    # Z: -123.08
    # Roughly -124 starts 0.
    # -124 + (idx * 7.5) = lon
    # idx = (lon - (-124)) / 7.5
    # Actually, we can just find the closest match if we had the table.
    
    # Hardcoded ranges based on previous observation
    # Steps are roughly 7.5 degrees
    
    start_lon = -124.0 # Approx start
    
    # Adjust start lon per row if needed, but let's try generic
    # The previous success used idx = (lon - start) / step
    # Let's reverse engineer from known good chars
    # Row 32 Lat=0.0 -> Z row. 
    # Let's just output Lat, Lon for Rows 32+ and manual check vs keystream
    return row_idx, lon

df = pd.read_csv('logs.csv')

# Rows 32 to 39 (first 8 bytes of PNG)
# Note: CSV index 0 is row 2 in Excel?
# Index 31 is Row 32? (Start of binary data?)
# Let's checking the split point
# Previous script said Row 32 starts binary.
# Access by index.

print("Row | Lat | Lon | DerivedRow | DerivedCol | KeystreamByte")
# Keystream: 58 5b f3 78 45 0c 75 5f
keystream = [0x58, 0x5b, 0xf3, 0x78, 0x45, 0x0c, 0x75, 0x5f]

for i in range(8):
    idx = 31 + i # Assuming binary starts at index 31 (Row 32)
    row = df.iloc[idx]
    lat = float(row['Latitude'])
    lon = float(row['Longitude'])
    
    row_idx = -1
    if lat > 20: row_idx = 0
    elif lat > 10: row_idx = 1
    else: row_idx = 2
    
    # Calculate col index
    # Q is at -124.12. Column 0.
    # W is at -116. Column 1.
    start_lon = -124.12
    col_idx = round((lon - start_lon) / 7.5)
    
    print(f"{i} | {lat} | {lon} | {row_idx} | {col_idx} | {hex(keystream[i])}")
