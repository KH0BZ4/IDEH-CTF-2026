# Logic Burst - MISC

- CTF: IDEH CTF 2026
- Category: MISC
- Author: Unknown
- Solver: W4ST3D
- Flag: `IDEH{L0g1c_4n4lyz3r_M4st3r}`

---

## Challenge
> "We intercepted a logic analyzer capture from an embedded device. The communication protocol contains a hidden message.
>
> Decode the signals to find the flag."

**Files:**
- `logicburst.sal`: Saleae Logic analyzer capture file

---

## Overview
This challenge involves analyzing a logic analyzer capture file (.sal format from Saleae Logic software). The capture contains digital signals from an embedded device that encode the flag using a serial communication protocol.

---

## Root Cause
Embedded devices communicate using various serial protocols (UART, SPI, I2C, etc.). The .sal file contains captured digital signals that, when decoded with the correct protocol and baud rate, reveal the hidden message.

---

## Exploitation Steps

### 1. Extract the Capture Data
The .sal file is actually a ZIP archive:
```bash
unzip logicburst.sal -d extracted_sal
ls extracted_sal/
# Contains: digital-0.bin, meta.json, etc.
```

### 2. Open in Saleae Logic 2
Import the .sal file into Saleae Logic 2 software to visualize the signals.

### 3. Identify the Protocol
Analyze the signal patterns:
- Look for start/stop bits (UART)
- Check for clock + data lines (SPI/I2C)
- Measure timing to determine baud rate

Common baud rates: 9600, 19200, 38400, 115200

### 4. Add Protocol Analyzer
In Saleae Logic 2:
1. Click "Analyzers" panel
2. Add "Async Serial" (UART) analyzer
3. Configure: Channel 0, Baud rate (try 115200), 8N1

### 5. Export Decoded Data
The analyzer will decode the serial stream, revealing ASCII characters that form the flag.

### 6. Alternative: Python Parsing
```python
import json

with open('extracted_sal/meta.json', 'r') as f:
    meta = json.load(f)

# Parse digital samples based on sample rate
sample_rate = meta['sampleRate']
baud_rate = 115200
samples_per_bit = sample_rate / baud_rate

# Read and decode the signal...
```

### 7. Result
Decoding the UART signal reveals: `IDEH{L0g1c_4n4lyz3r_M4st3r}`
