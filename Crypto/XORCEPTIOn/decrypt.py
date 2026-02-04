
def xor_data(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

key = b"M44GiC"

with open("challenge.bin", "rb") as f:
    encrypted_data = f.read()

decrypted_data = xor_data(encrypted_data, key)

# Check if it starts with PNG signature
png_sig = b"\x89PNG\r\n\x1a\n"
if decrypted_data.startswith(png_sig):
    print("Valid PNG signature found!")
    with open("output.png", "wb") as f:
        f.write(decrypted_data)
    print("Decrypted image saved to output.png")
else:
    print("Invalid signature.")
    print("First 8 bytes:", decrypted_data[:8])
    print("Expected:", png_sig)

