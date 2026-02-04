from PIL import Image, ImageOps

def score_plane(plane_bytes, width, height):
    score = 0
    # Compare row N with row N+1
    for y in range(height - 1):
        row1 = plane_bytes[y*width : (y+1)*width]
        row2 = plane_bytes[(y+1)*width : (y+2)*width]
        # Sum absolute differences
        for x in range(width):
            diff = abs(row1[x] - row2[x])
            score += diff
    return score

def process_plane(plane_data, width, height, field_order, serpentine_mode):
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
    lines_per_field = height // 2
    
    for i in range(lines_per_field):
        line_e = even_field[i*width : (i+1)*width]
        line_o = odd_field[i*width : (i+1)*width]
        
        if serpentine_mode == 'reverse_even':
            line_e = line_e[::-1]
            
        if serpentine_mode == 'reverse_odd':
            line_o = line_o[::-1]
            
        lines.append(line_e)
        lines.append(line_o)
        
    return b"".join(lines)

def solve():
    with open('blackbox_vram.bin', 'rb') as f:
        data = f.read()

    # The user says 256x64 is clearer.
    width = 256
    height = 64
    plane_size = width * height
    
    r_raw = data[0:plane_size]
    g_raw = data[plane_size:2*plane_size]
    b_raw = data[2*plane_size:3*plane_size]

    # Find best config for THIS resolution
    configs = []
    for fo in ['even_first', 'odd_first']:
        for sm in ['reverse_odd', 'reverse_even', 'none']:
            configs.append((fo, sm))
            
    best_score = float('inf')
    best_config = None
    
    test_plane = g_raw
    print(f"Testing configurations for {width}x{height}...")
    
    for config in configs:
        fo, sm = config
        processed = process_plane(test_plane, width, height, fo, sm)
        s = score_plane(processed, width, height)
        print(f"Config: {config}, Score: {s}")
        if s < best_score:
            best_score = s
            best_config = config
            
    print(f"Best Config for 256x64: {best_config}")
    
    fo, sm = best_config
    
    r_final = process_plane(r_raw, width, height, fo, sm)
    g_final = process_plane(g_raw, width, height, fo, sm)
    b_final = process_plane(b_raw, width, height, fo, sm)
    
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            pixels[x, y] = (r_final[idx], g_final[idx], b_final[idx])
            
    # Upscale specifically to make it "more clear" to read
    # 4x scaling
    scale = 4
    new_size = (width * scale, height * scale)
    # NEAREST preserves the pixel sharpness which is vital for reading pixel text
    img_large = img.resize(new_size, Image.Resampling.NEAREST)
    
    img_large.save('flag_256_final.png')
    print("Saved flag_256_final.png")

if __name__ == "__main__":
    solve()
