from PIL import Image, ImageOps
import sys

def process_plane(plane_data, width, height, field_order, serpentine_mode):
    # field_order: 'even_first' or 'odd_first'
    # serpentine_mode: 'reverse_odd' or 'reverse_even' or 'none'
    
    half = len(plane_data) // 2
    part1 = plane_data[:half]
    part2 = plane_data[half:]
    
    if field_order == 'even_first':
        even_field = part1
        odd_field = part2
    else:
        odd_field = part1
        even_field = part2
        
    lines = []
    for i in range(height // 2):
        line_e = even_field[i*width : (i+1)*width]
        line_o = odd_field[i*width : (i+1)*width]
        
        if serpentine_mode == 'reverse_even':
            line_e = line_e[::-1]
            
        if serpentine_mode == 'reverse_odd':
            line_o = line_o[::-1]
            
        lines.append(line_e)
        lines.append(line_o)
        
    return b"".join(lines)

def generate_image(width, height, r_p, g_p, b_p, field_order, serpentine_mode, name):
    r_final = process_plane(r_p, width, height, field_order, serpentine_mode)
    g_final = process_plane(g_p, width, height, field_order, serpentine_mode)
    b_final = process_plane(b_p, width, height, field_order, serpentine_mode)
    
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            pixels[x, y] = (r_final[idx], g_final[idx], b_final[idx])
            
    # Try an autolevels to make it pop
    # img = ImageOps.autocontrast(img) 
    # Actually, raw pixels might be better to see what is going on first
    img.save(name)
    print(f"Saved {name}")

def solve():
    with open('blackbox_vram.bin', 'rb') as f:
        data = f.read()

    # 1. Standard 128x128
    width = 128
    height = 128
    plane_size = width * height
    
    r_raw = data[0:plane_size]
    g_raw = data[plane_size:2*plane_size]
    b_raw = data[2*plane_size:3*plane_size]
    
    if len(r_raw) == plane_size:
        print("Generating candidates for 128x128...")
        # Best from before
        generate_image(width, height, r_raw, g_raw, b_raw, 'even_first', 'reverse_odd', 'flag_128_normal.png')
        # Mirror check
        generate_image(width, height, r_raw, g_raw, b_raw, 'even_first', 'reverse_even', 'flag_128_mirror.png')
        
    # 2. Try Width 256 (Height 64)
    # Total pixels = 16384
    width = 256
    height = 64
    plane_size = width * height
    # Plane data is identical buffer, just interpreted differently?
    # Yes, r_raw is just the first 16384 bytes.
    
    if len(r_raw) == plane_size:
        print("Generating candidates for 256x64...")
        generate_image(width, height, r_raw, g_raw, b_raw, 'even_first', 'reverse_odd', 'flag_256_normal.png')
        
    # 3. Create Montage
    from PIL import ImageDraw, ImageFont
    
    # Load all
    cands = [
        ('flag_128_normal.png', "128x128 Normal"),
        ('flag_128_mirror.png', "128x128 Mirror"),
        ('flag_256_normal.png', "256x64 Normal")
    ]
    
    images = []
    for fn, label in cands:
        try:
            im = Image.open(fn)
            images.append((im, label))
        except:
            pass
            
    # Calculate montage size
    # Max width 256
    total_h = sum(im.height + 20 for im, l in images)
    max_w = max(im.width for im, l in images)
    
    montage = Image.new('RGB', (max_w, total_h), (50, 50, 50))
    y_off = 0
    draw = ImageDraw.Draw(montage)
    
    for im, label in images:
        montage.paste(im, (0, y_off))
        draw.text((5, y_off), label, fill=(255, 255, 0))
        y_off += im.height + 20
        
    montage.save('flag_montage.png')
    print("Saved flag_montage.png")

if __name__ == "__main__":
    solve()
