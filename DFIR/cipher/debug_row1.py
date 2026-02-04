import csv
import base64

row1_data = "YTBiNTI0YzVkMjhkNTMwYzI0MjUzMjA1MDRlZjMyYWYyYjI5ZDA4Nzc2OTY5YTBlMTY="
data = base64.b64decode(row1_data)
print(f"Raw Bytes: {data.hex()}")
print(f"Raw Ascii (approx): {data}")

key_char = 'Q'
key_byte = ord(key_char)
print(f"Key Q: {hex(key_byte)}")

decrypted = bytes([b ^ key_byte for b in data])
print(f"XOR Q: {decrypted}")

key_char_R = 'R'
key_byte_R = ord(key_char_R)
print(f"Key R: {hex(key_byte_R)}")
decrypted_R = bytes([b ^ key_byte_R for b in data])
print(f"XOR R: {decrypted_R}")

# Check if result matches 'b040...'
target = b'b040'
print(f"Target logic check:")
# b0 ^ 61 ('a') = D1.
# b0 ^ 30 ('0') = 80.
# b0 ^ 62 ('b') = D2.
