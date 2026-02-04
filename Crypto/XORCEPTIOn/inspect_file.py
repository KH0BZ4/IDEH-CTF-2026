
with open("challenge.bin", "rb") as f:
    data = f.read(32)
    print(data)
    print("Hex:", data.hex())
