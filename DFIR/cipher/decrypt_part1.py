import csv
import base64
import binascii

rows_layout = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

def get_char(lat, lon):
    if lat > 18: r = 0
    elif lat > 6: r = 1
    else: r = 2
    c_idx = int(round(lon / 7.5))
    if r < len(rows_layout):
        row_str = rows_layout[r]
        return row_str[c_idx % len(row_str)]
    return '?'

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    print("Decrypting Part 1 (Hex Rows)...")
    
    decoded_text = ""
    
    for i, row in enumerate(reader):
        try:
            lat = float(row['Latitude (?)'])
            lon = float(row['Longitude (?)'])
            key_char = get_char(lat, lon)
            key_byte = ord(key_char)
            
            data_b64 = row['Data']
            data_bytes = base64.b64decode(data_b64)
            
            # Check if it looks like ASCII hex
            s = data_bytes.decode('utf-8').strip()
            if all(c in '0123456789abcdefABCDEF' for c in s):
                if len(s) % 2 != 0: s = '0' + s
                bin_chunk = binascii.unhexlify(s)
                
                # XOR
                decrypted_chunk = bytes([b ^ key_byte for b in bin_chunk])
                
                # Check if it looks like text
                try:
                    text_chunk = decrypted_chunk.decode('utf-8')
                    print(f"Row {i+1} ({key_char}): {text_chunk}")
                    decoded_text += text_chunk
                except:
                    print(f"Row {i+1} ({key_char}): [Binary] {decrypted_chunk.hex()}")
            else:
                pass # Not hex
        except Exception as e:
            pass

    print(f"\nFull Decoded Text:\n{decoded_text}")
