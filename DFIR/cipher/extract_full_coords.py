import csv

rows_layout = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

def get_char(lat, lon):
    if lat > 20: r = 0   # Approx 25
    elif lat > 10: r = 1  # Approx 12.5
    else: r = 2          # Approx 0
    
    # Each column is 7.5 width
    c_idx = int(round(lon / 7.5))
    
    if r < len(rows_layout):
        row_str = rows_layout[r]
        # Use modulo to wrap
        char = row_str[c_idx % len(row_str)]
        return char
    return '?'

full_string = ""
binary_string = ""

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        lat = float(row['Latitude (?)'])
        lon = float(row['Longitude (?)'])
        char = get_char(lat, lon)
        full_string += char
        if i >= 31: # Rows 32+ (Index 31+)
            binary_string += char

print(f"Full String: {full_string}")
print(f"Binary Part String: {binary_string}")
