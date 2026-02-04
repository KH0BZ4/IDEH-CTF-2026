import csv
import base64

rows_layout = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

def get_char(lat, lon):
    if lat > 18: r = 0   # Approx 25
    elif lat > 6: r = 1  # Approx 12.5
    else: r = 2          # Approx 0
    
    # Each column is 7.5 width
    c_idx = int(round(lon / 7.5))
    
    if r < len(rows_layout):
        row_str = rows_layout[r]
        # Use modulo to wrap
        char = row_str[c_idx % len(row_str)]
        return char
    return '?'

decoded_msg = []

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    print("Decrypting...")
    for i, row in enumerate(reader):
        lat = float(row['Latitude (?)'])
        lon = float(row['Longitude (?)'])
        key_char = get_char(lat, lon)
        key_byte = ord(key_char)
        
        try:
            data = base64.b64decode(row['Data'])
            # XOR
            decrypted = bytes([b ^ key_byte for b in data])
            # Try to print as text
            print(f"Row {i+1} ({key_char}): {decrypted}")
            decoded_msg.append(decrypted)
        except Exception as e:
            print(f"Row {i+1}: Error {e}")

full_data = b"".join(decoded_msg)
print("\nFull Data Hex:")
print(full_data.hex()[:200]) # Print start
