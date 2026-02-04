import csv
import base64
import binascii

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    with open('reconstructed_file.bin', 'wb') as out:
        for i, row in enumerate(reader):
            try:
                data_b64 = row['Data']
                raw_data = base64.b64decode(data_b64)
                
                # Check if it's the hex-string type
                # Rows 1-31 approx.
                try:
                    s = raw_data.decode('utf-8').strip()
                    if all(c in '0123456789abcdefABCDEF' for c in s):
                         if len(s) % 2 != 0: s = '0' + s
                         chunk = binascii.unhexlify(s)
                         out.write(chunk)
                    else:
                        # Not hex string, write raw
                        out.write(raw_data)
                except:
                    # Not utf-8, write raw
                    out.write(raw_data)
            except Exception as e:
                print(f"Error Row {i}: {e}")

print("Done. Saved to reconstructed_file.bin")
