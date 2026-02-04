
from PIL import Image

import os

# Since I installed tesseract via brew, it should be in path. Pytesseract might not find it if not in path, but usually it does.
# I need to install pytesseract wrapper first. But I can just use subprocess to call tesseract.

import subprocess

def run_tesseract(image_path):
    result = subprocess.run(['tesseract', image_path, 'stdout'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

# Open image and process
img = Image.open('output.png')
# Convert to grayscale
img = img.convert('L')
img.save('output_gray.png')
print("Gray OCR:", run_tesseract('output_gray.png'))

# Threshold
threshold = 128
img_thresh = img.point(lambda p: p > threshold and 255)
img_thresh.save('output_thresh.png')
print("Thresh OCR:", run_tesseract('output_thresh.png'))

# Resize
img_resized = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
img_resized.save('output_resized.png')
print("Resized OCR:", run_tesseract('output_resized.png'))
