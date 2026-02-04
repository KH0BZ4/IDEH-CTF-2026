from PIL import Image, ImageOps, ImageEnhance
import sys

def score_plane(plane_bytes, width, height):
    score = 0
    for y in range(height - 1):
        row1 = plane_bytes[y*width : (y+1)*width]
        row2 = plane_bytes[(y+1)*width : (y+2)*width]
        for x in range(width):
            diff = abs(row1[x] - row2[x])
            score += diff
    return score

def process_plane(plane_data, width, height, field_order, serpentine_mode):
    half = len(plane_data) // 2
    part1 = plane_data[:half]
    part2 = plane_data[half:]
    
    # 2. Interlaced Scanning
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
        
        # 3. Serpentine
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

    configs = []
    for fo in ['even_first', 'odd_first']:
        for sm in ['reverse_odd', 'reverse_even', 'none']:
            configs.append((fo, sm))

    plane_len = len(data) // 3
    # Use Green channel for scoring
    g_raw = data[plane_len:2*plane_len]
    
    candidates = [
        (256, 64),
        (512, 32),
        (64, 256)
    ]
    
    best_res_score = float('inf')
    best_res = None
    best_res_config = None
    
    print("Scoring resolutions...")
    for w, h in candidates:
        if w*h != plane_len: continue
        
        local_best = float('inf')
        local_config = None
        
        for config in configs:
            fo, sm = config
            processed = process_plane(g_raw, w, h, fo, sm)
            s = score_plane(processed, w, h)
            if s < local_best:
                local_best = s
                local_config = config
        
        # Normalize score by number of pixels comparisons? 
        # width * height is constant.
        # But we sum width * (height-1) diffs.
        # larger width, smaller height -> fewer vertical comparisons (less total diff usually).
        # We should probably normalize by (width * (height-1)).
        # Normalized Metric = s / (w * (h-1))
        
        norm_score = local_best / (w * (h - 1))
        print(f"Res {w}x{h}: Best Score {local_best} (Norm: {norm_score:.4f}) Config {local_config}")
        
        # Just use raw score for now, but pay attention to norm.
        # 256x64 had score ~100k.
        if local_best < best_res_score:
            best_res_score = local_best
            best_res = (w, h)
            best_res_config = local_config

    print(f"Selecting Best Resolution: {best_res} with config {best_res_config}")
    
    # Generate 256x64 (since user said it's clearer, we stick to it unless 512 is massively better)
    # The scoring on 512x32 might be artificially low because there are very few rows.
    # User feedback "256x64 is more clear" is ground truth.
    
    width, height = 256, 64
    # Re-verify config for this res
    best_config_256 = None
    best_score_256 = float('inf')
    for config in configs:
        fo, sm = config
        processed = process_plane(g_raw, width, height, fo, sm)
        s = score_plane(processed, width, height)
        if s < best_score_256:
            best_score_256 = s
            best_config_256 = config
            
    r_raw = data[0:plane_len]
    b_raw = data[2*plane_len:3*plane_len]
    
    # Generate Normal
    fo, sm = best_config_256
    def make_img(f, s):
        rf = process_plane(r_raw, width, height, f, s)
        gf = process_plane(g_raw, width, height, f, s)
        bf = process_plane(b_raw, width, height, f, s)
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        for y in range(height):
            for x in range(width):
                 pixels[x, y] = (rf[y*width+x], gf[y*width+x], bf[y*width+x])
        return img
    
    img_normal = make_img(fo, sm)
    
    # Generate Mirror (The other one with same score)
    # If ('even_first', 'reverse_odd') is best, try ('even_first', 'reverse_even')
    fo_m, sm_m = fo, 'reverse_even' if sm == 'reverse_odd' else 'reverse_odd'
    img_mirror = make_img(fo_m, sm_m)
    
    # Enhance
    def enhance_and_save(base_img, filename):
        # Scale up
        scale = 8
        big = base_img.resize((width*scale, height*scale), Image.Resampling.NEAREST)
        
        # Contrast
        # converter = ImageEnhance.Contrast(big)
        # big = converter.enhance(2.0)
        
        # Auto levels
        big = ImageOps.autocontrast(big)
        
        big.save(filename)
        print(f"Saved {filename}")
        
    enhance_and_save(img_normal, "flag_256_enhanced_normal.png")
    enhance_and_save(img_mirror, "flag_256_enhanced_mirror.png")
    
    # Create a sharp B&W for OCR readability
    bw = img_normal.convert('L').point(lambda x: 0 if x < 100 else 255, '1')
    bw = bw.resize((width*4, height*4), Image.Resampling.NEAREST)
    bw.save('flag_256_bw.png')
    print("Saved flag_256_bw.png")

if __name__ == "__main__":
    solve()
