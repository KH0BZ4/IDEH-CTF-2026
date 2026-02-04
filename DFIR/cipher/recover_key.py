import csv
import base64

def get_png_key_stream(binary_data):
    # PNG Signature (8 bytes)
    png_sig = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    
    key_stream = bytearray()
    
    # Recover first 8 bytes of key
    for i in range(8):
        if i < len(binary_data):
            k = binary_data[i] ^ png_sig[i]
            key_stream.append(k)
            
    return key_stream

# Get binary data
binary_data = bytearray()
with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
         if i >= 31: # Skip text part
             try:
                 binary_data.extend(base64.b64decode(row['Data']))
             except: pass

key_start = get_png_key_stream(binary_data)
print(f"Key Start (Hex): {key_start.hex()}")
print(f"Key Start (ASCII): {key_start}")

# Check for patterns
# X [ ? x E ? u _
