from PIL import Image
import sys

def calculate_smoothness(image_bytes, width, height):
    # Lower score is improved smoothness
    # Simple sum of absolute vertical differences
    score = 0
    # We only check one channel for speed/simplicity, or sum all.
    # Let's verify using the green channel (middle of RGB).
    # image_bytes is separate R, G, B planes. 
    # But here we pass the reconstructed interleaved bytes for one plane.
    pass

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
        
        # Determine strict line indices in final image
        # Even field -> lines 0, 2, 4...
        # Odd field -> lines 1, 3, 5...
        
        # Apply serpentine reverse based on physical line index
        # Line 2*i is Even
        if serpentine_mode == 'reverse_even':
            line_e = line_e[::-1]
            
        # Line 2*i + 1 is Odd
        if serpentine_mode == 'reverse_odd':
            line_o = line_o[::-1]
            
        lines.append(line_e)
        lines.append(line_o)
        
    return b"".join(lines)

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

def solve():
    with open('blackbox_vram.bin', 'rb') as f:
        data = f.read()

    width = 128
    height = 128
    plane_size = width * height
    
    r_raw = data[0:plane_size]
    g_raw = data[plane_size:2*plane_size]
    b_raw = data[2*plane_size:3*plane_size]
    
    # We only need to check one plane to check geometry correctness
    # Green is usually essentially luminance, good for structure.
    test_plane = g_raw

    configs = []
    # (Field Order, Serpentine Mode)
    for fo in ['even_first', 'odd_first']:
        for sm in ['reverse_odd', 'reverse_even', 'none']:
            configs.append((fo, sm))
            
    best_score = float('inf')
    best_config = None
    
    print("Testing configurations...")
    for config in configs:
        fo, sm = config
        processed = process_plane(test_plane, width, height, fo, sm)
        s = score_plane(processed, width, height)
        print(f"Config: {config}, Score: {s}")
        if s < best_score:
            best_score = s
            best_config = config
            
    print(f"Best Config found: {best_config}")
    
    # Generate full image with best config
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
            
    img.save('flag.png')
    print("Saved flag.png")
    
    # Save raw reconstructed data to check for strings
    with open('flag.raw', 'wb') as f:
        # Interleave RGB? Or just dump planes?
        # Usually strings would be contiguous.
        # Let's dump the interleaved RGB bytes from the loop/pixels
        raw_data = bytearray()
        for y in range(height):
            for x in range(width):
                 idx = y * width + x
                 raw_data.append(r_final[idx])
                 raw_data.append(g_final[idx])
                 raw_data.append(b_final[idx])
        f.write(raw_data)
    print("Saved flag.raw")

if __name__ == "__main__":
    solve()
