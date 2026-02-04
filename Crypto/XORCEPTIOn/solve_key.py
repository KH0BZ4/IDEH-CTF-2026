
file_bytes = bytes.fromhex("c4647a006449573e3447694e047c701569434b0134476ac74532344769aa6087")
png_header = bytes.fromhex("89504E470D0A1A0A")

key = []
for f, p in zip(file_bytes, png_header):
    key.append(f ^ p)

print(f"Key bytes derived from PNG header: {[hex(k) for k in key]}")

# Let's also check for JPEG
jpeg_header = bytes.fromhex("FFD8FF")
key_jpeg = []
for f, p in zip(file_bytes, jpeg_header):
    key_jpeg.append(f ^ p)
print(f"Key bytes derived from JPEG header: {[hex(k) for k in key_jpeg]}")

# BMP
bmp_header = bytes.fromhex("424D")
key_bmp = []
for f, p in zip(file_bytes, bmp_header):
    key_bmp.append(f ^ p)
print(f"Key bytes derived from BMP header: {[hex(k) for k in key_bmp]}")

# GIF89a
gif_header = bytes.fromhex("474946383961")
key_gif = []
for f, p in zip(file_bytes, gif_header):
    key_gif.append(f ^ p)
print(f"Key bytes derived from GIF header: {[hex(k) for k in key_gif]}")
