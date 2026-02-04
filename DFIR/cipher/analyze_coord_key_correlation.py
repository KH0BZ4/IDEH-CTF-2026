import pandas as pd
import struct

# Let's see if the coordinates 0.03, 112.49 can be converted to the key byte 0x58.
# 0.03 (Lat). 112.49 (Lon). Key: 0x58 (88).
# 25.03 (Lat). 112.55 (Lon). Key: 0x5b (91).Diff: Lat +25. Key +3. Lon +0.06.
# 25.01 (Lat). 127.50 (Lon). Key: 0xf3 (243). Diff: Lat -0.02. Lon +15. Key +152.

# Key diff 91 -> 243. (+152).
# Lon diff 112.55 -> 127.50 (+15).
# 15 * 10 = 150? Close to 152.

# Let's check Row 32 -> Row 33 (First 2 points).
# X (88) -> [ (91).
# Lat 0 -> 25.
# Lon 112.49 -> 112.55.
# If Key ~ Lon * 10?
# 112.49 * 10 = 1124.9.
# 1124 % 256 = 100? No.

# Let's try `Key = (Lon - Offset) * Factor`?
# 112.49 -> 88.
# 127.50 -> 243.
# Diff Lon = 15.01. Diff Key = 155.
# Scale = 155 / 15.01 ~ 10.3.

# Let's checking exactness.
# Maybe `round(Lon - 100) * 10`?
# (112.49 - 100) * 10 = 124.9. (125).
# 88? No.

# What about Latitude?
# Row 32 (Lat 0) -> X (88).
# Row 33 (Lat 25) -> [ (91).
# Lat diff 25. Key diff 3.
# Lat doesn't seem to drive the key much.

# What about `Key = CharCoordinate(Lat, Lon) ^ MAGIC`?
# Row 32: Char X? My script says 0x58 (X).
# If Char is X, Key is X.
# Row 33: Char [? My script `v2` says Char '?'. 
# Let's verify Char for Row 33 manually.
# Lat 25 (Row 0: QWERTY...).
# Lon 112.55.
# If My script said `112.5 -> Key X` (Lon 112.49 in Row 2).
# X is index 1 of Row 2.
# Lon ~112.5 corresponds to Index 1 (in my broken "v2" script? No, in my head).

# Let's re-run `extract_full_coords.py` logic trace.
# `get_char` logic: `c_idx = int(round(lon / 7.5))`.
# 112.49 / 7.5 = 14.99. -> 15.
# Row 2 (ZXCVBNM,./). Length 10.
# 15 % 10 = 5.
# Row 2 Index 5 is 'N'.
# But the key is 'X' (Index 1).
# So `c_idx` calculation is WRONG.

# If `Key == Char`, then `X` (Index 1 of Row 2) means `c_idx % 10 == 1`.
# So `c_idx` should be 1, 11, 21...
# Lon 112.49.
# If `c_idx = Lon / Step`?
# 112.49 / X = 11? X ~ 10.
# 112.49 / X = 21? X ~ 5.3.

# Wait!
# 112.49 matches 'X' (Index 1).
# 127.50 matches '\xf3' (243). Matches 'ó' in Latin-1. Key is `f3`.
# Row 34: Lat 25.01 (Row 0). Lon 127.50.
# Q W E R T Y U I O P [ ]
# 0 1 2 3 4 5 6 7 8 9 10 11
# If `f3` is the char. Where is `f3`?
# Maybe `f3` IS the Char?
# `Q`=51.
# `f3`=243.
# Just bytes.

# Re-evaluate Key Bytes.
# 58, 5b, f3, 78, 45, 0c, 75, 5f ...
# 58 = X.
# 5b = [.
# f3.
# 78 = x.
# 45 = E.
# 0c.
# 75 = u.
# 5f = _.

# Notice `X` (58) vs `x` (78).
# X is upper. x is lower.
# `[` (5b). Is related to keys.
# `_` (5f).

# What if the key is composed of `(LonByte ^ LatByte)`?
# Or `int(Lon) ^ int(Lat)`?
# Row 32: Lat 0.03. Lon 112.49.
# int(0) ^ int(112) = 112 (0x70). Key 0x58. Diff 0x28.
# Row 33: Lat 25.03. Lon 112.55.
# int(25) ^ int(112) = 25 ^ 112 = 121 (0x79). Key 0x5b. Diff 0x22.

# Using derived key `58 5b f3 78 45 0c 75 5f`.
# Let's try to find a formula: `F(Lat, Lon) = Key`.
# Data:
# (0.03, 112.49) -> 0x58
# (25.03, 112.55) -> 0x5b
# (25.01, 127.50) -> 0xf3
# (12.53, 127.46) -> 0x78
# (12.52, 112.50) -> 0x45

# 127.50 -> f3?
# 112.50 -> 45 (E)?
# 112.49 -> 58 (X)?

# 112.49 vs 112.50. Lon almost same.
# Lat 0.03 vs 12.52.
# Key 58 vs 45.
# 0x58 (88). 0x45 (69).
# Diff -19.
# Lat Diff +12.5.
# Does Lat correlate negatively?

# 127.50 -> f3 (243).
# 127.46 -> 78 (120).
# Lon same-ish.
# Lat 25.01 vs 12.53.
# Key Diff 243 vs 120 = 123.
# Lat Diff 12.5.

# 12.5 Lat change -> 19 change?
# 12.5 Lat change -> 123 change?
# Inconsistent.

# Let's try the Coordinates as STRING directly.
# "0.03112.49" ...
# Or the Log_ID?

pass
