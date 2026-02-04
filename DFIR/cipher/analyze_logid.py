import csv
import base64

keystream_start = [0x58, 0x5b, 0xf3, 0x78, 0x45, 0x0c, 0x75, 0x5f]

with open('logs.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
    start_index = 31 # Row 32
    
    print("Row | Log_ID | PayloadStart | KeystreamByte")
    
    # We suspect keystream changes per BYTE.
    # But let's check if Log_ID relates to the START of the block encryption.
    
    # Actually, we need to know if the keystream is consumed by the bytes in the row.
    # Row 32 has ~37 bytes.
    # Keystream[0] corresponds to Row 32 Byte 0.
    # Keystream[1] corresponds to Row 32 Byte 1.
    
    # So Log_ID of Row 32 should explain Keystream[0]...Keystream[36].
    
    row = rows[start_index]
    log_id = row['Log_ID']
    print(f"32 | {log_id}")
    
    # Analyze Log_ID vs Keystream[0..7]
    # Log_ID: CT_LOG_...
    # Key: 58 5b ...
    
    # Maybe Log_ID IS the key?
    # CT_LOG_...
    # Let's verify.
    
    print(f"Key: {bytes(keystream_start).hex()}")
