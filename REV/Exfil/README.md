# Exfil Writeup

![Challenge](challenge.png)

**Category:** Mobile / Reverse Engineering  
**Points:** 500  
**Solves:** 2  

## Challenge Description

> Easy but hard & chaining is key, how good you are?

## Solution

We get an APK file called `exfil.apk`. The hint says "chaining is key" which is a hint about certificate chain.

### First Look

I decompiled the APK using apktool to get the smali code:

```bash
apktool d exfil.apk -o exfil_apktool
```

Looking at the package structure, I found `com.cit.ideh.exfil` with `MainActivity` and `DocsActivity`. There's also a JavaScript interface class.

### Finding the Flag Storage

In `DocsActivity.smali`, I found it creates a WebView and adds a JavaScript interface called "IDEH":

```smali
const-string v2, "IDEH"
invoke-virtual {p1, v1, v2}, Landroid/webkit/WebView;->addJavascriptInterface(...)
```

The interface has two methods:
- `getDeviceInfo()` - returns device model and SDK version
- `readVault()` - decrypts and returns something interesting

### Analyzing readVault()

Looking at the smali code for `readVault()`, it does the following:

1. Reads a raw resource file (R0.bin from res folder)
2. Extracts first 12 bytes as IV, rest as ciphertext
3. Gets the APK signing certificate
4. Computes SHA-256 of the certificate
5. Uses first 16 bytes of hash as AES key
6. Decrypts using AES-GCM with package name as AAD

The encrypted blob is stored in `res/R0.bin`:
```
0d55628b99db2a1f286bce9622cb152e32c2c8ecd1de8e3e03358b15ffca2762edc3d7d3be53387f55ae61365764f4dfc949b4
```

### Getting the Signing Certificate

The key is derived from the APK's signing certificate. I used apksigner to get it:

```bash
$ apksigner verify --print-certs exfil.apk
Signer #1 certificate DN: C=MA, O=CIT IDEH ctf, CN=Tea
Signer #1 certificate SHA-256 digest: c797e89761eadaba8c60dd66eabdfae32e532750b639dc3143a7f42a3091ccb3
```

### Decryption

Now I have everything:
- **IV**: first 12 bytes of blob = `0d55628b99db2a1f286bce96`
- **Ciphertext**: remaining bytes
- **AES Key**: first 16 bytes of cert SHA-256 = `c797e89761eadaba8c60dd66eabdfae3`
- **AAD**: package name = `com.cit.ideh.exfil`

### Solve Script

```python
#!/usr/bin/env python3
from Crypto.Cipher import AES

# SHA-256 of signing certificate (first 16 bytes as key)
cert_sha256 = "c797e89761eadaba8c60dd66eabdfae32e532750b639dc3143a7f42a3091ccb3"
aes_key = bytes.fromhex(cert_sha256)[:16]

# Encrypted blob from res/R0.bin
blob = bytes.fromhex("0d55628b99db2a1f286bce9622cb152e32c2c8ecd1de8e3e03358b15ffca2762edc3d7d3be53387f55ae61365764f4dfc949b4")

# First 12 bytes = IV, rest = ciphertext + tag
iv = blob[:12]
ciphertext = blob[12:]

# Package name as AAD
aad = b"com.cit.ideh.exfil"

# Decrypt
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
cipher.update(aad)
plaintext = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])

print(f"Flag: {plaintext.decode()}")
```

Running it:

```
$ python3 solve.py
Flag: IDEH{m4ster_0f_4ndro1d}
```

## Flag

```
IDEH{m4ster_0f_4ndro1d}
```

The hint "chaining is key" was about the certificate chain - the decryption key comes from the APK signing certificate's SHA-256 hash. Nice Android reversing challenge!
