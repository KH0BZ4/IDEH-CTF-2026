def solve_vigenere(text, key):
    key = key.upper()
    res = ""
    ki = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[ki % len(key)]) - 65
            c_val = ord(char.upper()) - 65
            p_val = (c_val - shift) % 26
            res += chr(p_val + 65)
            ki += 1
        else:
            res += char
    return res

text = "QQECZZVRGYNNMUXOOCPPWPCBBNET"
key = "INPT"

print(f"Key {key}: {solve_vigenere(text, key)}")

key2 = "IDEH"
print(f"Key {key2}: {solve_vigenere(text, key2)}")

# Binary string
bin_text = "XYILJVVBOQDAADABMMRCBYYMIPDAXXENTTUOADXV"
print(f"Bin Key {key}: {solve_vigenere(bin_text, key)}")
