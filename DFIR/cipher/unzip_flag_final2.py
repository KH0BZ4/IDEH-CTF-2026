import pyzipper
import sys

passwords = [
    "QQECZZVRGYNNMUXOOCPPWPCBBNETZNN",
    "QQECZZVRGYNNMUXOOCPPWPCBBNETZ",
    "QQECZZVRGYNNMUXOOCPPWPCBBNETZN",
    "QQECZZVRGYNNMUXOOCPPWPCBBNET",
]

zip_file = "flag.zip"

for pwd in passwords:
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.pwd = pwd.encode('utf-8')
            zf.extractall("extracted_flag_2")
            print(f"Success! Password was: {pwd}")
            with open(f"extracted_flag_2/flag.txt", "r") as f:
                print(f"Flag Content: {f.read()}")
            sys.exit(0)
    except Exception as e:
        pass

print("All passwords failed.")
