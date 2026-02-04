def vigenere_decrypt(ciphertext, key):
    key_idx = 0
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)].upper()) - 65
            if char.isupper():
                p = chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                p = chr((ord(char) - 97 - shift) % 26 + 97)
            plaintext += p
            key_idx += 1
        else:
            plaintext += char
    return plaintext

cipher = "QQECZZVRGYNNMUXOOCPPWPCBBNET"
keys = ["MrYou", "CipherC", "Cipher-C", "IDEH", "475", "12.5"]

for k in keys:
    res = vigenere_decrypt(cipher, k)
    print(f"Key {k}: {res}")

# Maybe encrypt?
def vigenere_encrypt(plaintext, key):
    key_idx = 0
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)].upper()) - 65
            if char.isupper():
                c = chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                c = chr((ord(char) - 97 + shift) % 26 + 97)
            ciphertext += c
            key_idx += 1
        else:
            ciphertext += char
    return ciphertext

for k in keys:
    res = vigenere_encrypt(cipher, k)
    print(f"Key {k} (Enc): {res}")
