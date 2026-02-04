import pyzipper
import sys

passwords = [
    "EZGOFNETSEBWOGDCXEBVKYENHBNV",
    "ezgofnetsebwogdcxebvkyenhbnv",
    "OIPVVITPYJGJVSVGZVLYUNUMUJNR",
    "INAVRWRKYVJGERTHGZLIOMYUTKAM",
    "CHCQTLMPUSZEKIRAFADJIGAPVZVR",
]

zip_file = "flag.zip"

for pwd in passwords:
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = pwd.encode('utf-8')
            zf.extractall("extracted_vig")
            print(f"Success! Password was: {pwd}")
            sys.exit(0)
    except Exception as e:
        pass
print("All failed.")
