def solve_vigenere(text, key):
    res = ""
    ki = 0
    key_indices = [ord(k.upper()) - 65 for k in key]
    
    for char in text:
        if char.isalpha():
            c_val = ord(char.lower()) - 97
            shift = key_indices[ki % len(key_indices)]
            # Decrypt: P = (C - K) % 26
            p_val = (c_val - shift) % 26
            res += chr(p_val + 97)
            ki += 1
        else:
            res += char
    return res

text = "b040`hc0ib234e2`i4c0bic75ba7g42ci0d5h4c4fbc7g7h`7"
key = "TEYB" # Derived from b->I, h->D, c->E, i->H

decrypted = solve_vigenere(text, key)
print(f"Key TEYB: {decrypted}")

key_byte = "BYTE"
print(f"Key BYTE: {solve_vigenere(text, key_byte)}")
