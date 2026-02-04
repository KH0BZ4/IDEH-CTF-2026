
def analyze():
    with open('message_emoji.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    origin = ord('😈')
    key = 239 # Derived from IDEH{
    
    decoded = ""
    for c in content:
        diff = ord(c) - origin
        # Check if diff must be positive
        char_code = diff ^ key
        decoded += chr(char_code)
        
    print(f"Decoded: {decoded}")

if __name__ == '__main__':
    analyze()
