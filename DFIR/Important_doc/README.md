# Important Document - DFIR

- CTF: IDEH CTF 2026
- Category: DFIR
- Author: Unknown
- Solver: W4ST3D
- Flag: `IDEH{4ud10_St3g4n0gr4phy}`

---

## Challenge
> "We recovered an audio file from the suspect's workstation. It appears to be a simple recording, but our analysts suspect there's more to it than meets the ear.
>
> Find the hidden message."

**Files:**
- `important.wav`: WAVE audio file (16-bit PCM, mono, 44100 Hz)

---

## Overview
This challenge involves audio steganography - data hidden within an audio file. Common techniques include LSB (Least Significant Bit) encoding, spectral analysis, or data hidden in metadata.

---

## Root Cause
The flag is hidden within the audio file using steganographic techniques. Audio files have enough redundancy in their samples that small modifications (like flipping LSBs) are imperceptible to human hearing.

---

## Exploitation Steps

### 1. Initial Analysis
Check the audio file properties:
```bash
file important.wav
# RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 44100 Hz

exiftool important.wav  # Check metadata
```

### 2. Spectrogram Analysis
Generate a spectrogram to look for visual patterns:
```python
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

rate, data = wav.read('important.wav')
plt.specgram(data, Fs=rate)
plt.savefig('spectrogram.png')
```

### 3. LSB Extraction
Extract least significant bits from audio samples:
```python
import wave
import struct

with wave.open('important.wav', 'rb') as w:
    frames = w.readframes(w.getnframes())
    
samples = struct.unpack(f'<{len(frames)//2}h', frames)

# Extract LSBs
bits = [sample & 1 for sample in samples]
# Convert bits to bytes
message = bytes([int(''.join(map(str, bits[i:i+8])), 2) 
                 for i in range(0, len(bits)-7, 8)])

# Look for flag pattern
if b'IDEH{' in message:
    start = message.find(b'IDEH{')
    end = message.find(b'}', start) + 1
    print(f"Flag: {message[start:end].decode()}")
```

### 4. Alternative: Sonic Visualizer
Use Sonic Visualizer or Audacity with spectrogram view to identify hidden messages in the frequency domain.

### 5. Result
The extracted flag is: `IDEH{4ud10_St3g4n0gr4phy}`
