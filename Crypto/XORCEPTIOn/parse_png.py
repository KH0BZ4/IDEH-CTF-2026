
import struct

def parse_png_chunks(filename):
    with open(filename, "rb") as f:
        header = f.read(8)
        if header != b"\x89PNG\r\n\x1a\n":
            print("Not a PNG file")
            return

        while True:
            length_bytes = f.read(4)
            if len(length_bytes) < 4:
                break
            length = struct.unpack(">I", length_bytes)[0]
            
            chunk_type = f.read(4)
            chunk_data = f.read(length)
            crc = f.read(4)
            
            print(f"Chunk: {chunk_type.decode('ascii', errors='ignore')} - Length: {length}")
            
            if chunk_type in [b"tEXt", b"zTXt", b"iTXt"]:
                print(f"  Data: {chunk_data}")
            
            if chunk_type == b"IEND":
                break

parse_png_chunks("output.png")
