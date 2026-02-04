import csv

keystream = [0x58, 0x5b, 0xf3, 0x78, 0x45, 0x0c, 0x75, 0x5f]

print("RowOffset | Lat | Lon | RowIdx | ColIdx | KeyHex | KeyChar")

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    # Binary starts at row 32 (1-based), so index 31 (0-based)
    start_index = 31
    
    for i in range(8):
        if start_index + i >= len(rows): break
        
        row = rows[start_index + i]
        lat = float(row['Latitude'])
        lon = float(row['Longitude'])
        
        row_idx = -1
        if lat > 20: row_idx = 0
        elif lat > 10: row_idx = 1
        else: row_idx = 2
        
        # Col calculation
        start_lon = -124.12
        col_idx = round((lon - start_lon) / 7.5)
        
        print(f"{i} | {lat:.2f} | {lon:.2f} | {row_idx} | {col_idx} | {hex(keystream[i])} | {chr(keystream[i])}")
