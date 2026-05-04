# timeline0 CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | timeline0 |
| **Category** | Forensics |
| **Description** | Can you find the flag in this disk image? Wrap what you find in the picoCTF flag format. |
| **Files Provided** | `partition4.img.gz` (gzip-compressed ext4 filesystem image) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **MAC Timeline Analysis**: In digital forensics, MAC stands for Modified, Accessed, and Changed timestamps. Creating a timeline of file system activity using tools like `fls` and `mactime` from The Sleuth Kit allows investigators to identify anomalous file activity and potential tampering.
2. **Timestomping Detection**: Timestomping is a technique where attackers modify file timestamps to hide their activities. Sloppy timestomping often results in obviously incorrect dates (like 1985) that stand out when viewed in a chronological timeline against normal system files that have recent timestamps.

---

## 🔍 Step-by-Step Solution

### Step 1: Decompress the Image
The challenge provides a gzip-compressed disk image:
```bash
file partition4.img.gz
# Output: partition4.img.gz: gzip compressed data, was "partition4.img", last modified: Mon Dec  1 20:53:52 2025, max compression, from Unix, original size modulo 2^32 489684992

gunzip partition4.img.gz
ls
# Output: partition4.img
```

---

### Step 2: Identify Filesystem Type
We verify the filesystem type of the decompressed image:
```bash
file partition4.img
# Output: partition4.img: Linux rev 1.0 ext4 filesystem data, UUID=7a00e9da-98f8-4f0f-b257-95edf422d902 (extents) (64bit) (large files) (huge files)
```

The image is a raw ext4 filesystem (no partition table). This means the filesystem starts at sector offset 0.

---

### Step 3: Verify No Partition Table
We confirm there's no partition table:
```bash
fdisk -l partition4.img
# Output:
# Disk partition4.img: 467 MiB, 489684992 bytes, 956416 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes

mmls partition4.img
# Output: (no output - no partition table found)
```

As expected, this is a raw filesystem image with no partition table.

---

### Step 4: Generate Body File for Timeline
The hint explicitly guides us to create a MAC timeline. We use `fls` to generate a body file:
```bash
fls -r -m / -o 0 partition4.img > timeline.body
```

Parameters:
- `-r`: Recursive listing
- `-m /`: Mount point prefix (root)
- `-o 0`: Sector offset (filesystem starts at 0)
- `> timeline.body`: Redirect output to body file

---

### Step 5: Convert to Readable Timeline
We use `mactime` to convert the body file into a human-readable chronological timeline:
```bash
mactime -b timeline.body -d > timeline.txt
```

---

### Step 6: Find the Timestomped File
The hint mentions: "Sloppy timestomping can yield strange (very old) timestamps". We search for files with dates from the 1970s-2000s:
```bash
grep -E "197[0-9]|198[0-9]|199[0-9]|200[0-5]" timeline.txt | head -20
# Output:
# Tue Jan 01 1985 22:00:00,41,macb,r/rrw-r--r--,0,0,4945,"/bin/bcab"
```

**Key Finding:**

| Field | Value | Significance |
|-------|-------|--------------|
| Date | Jan 1, 1985 | Extremely old timestamp (timestomped) |
| Size | 41 bytes | Small file likely containing flag |
| Permissions | rw-r--r-- | Normal readable file |
| Inode | 4945 | Used for recovery |
| Path | /bin/bcab | Suspicious name in system binary directory |

**Why This File Stands Out:**
- **Timestamp**: January 1, 1985 is highly anomalous for a Linux system (would normally show recent dates)
- **Location**: `/bin/` typically contains standard system binaries - `bcab` is not a standard binary
- **Size**: 41 bytes is unusually small for a binary, suggesting it's a text file
- **Name**: `bcab` appears deliberately obscure to blend in

---

### Step 7: Extract the Hidden File
We use `icat` to extract the file content by its inode number:
```bash
icat partition4.img 4945 > bcab_recovered
cat bcab_recovered
# Output: NzFtMzExbjNfMHU3MTEzcl9oM3JfNDNhMmU3YWYK
```

The file contains a base64-encoded string (trailing `=` padding confirms base64).

---

### Step 8: Decode the Flag
First base64 decode:
```bash
echo "NzFtMzExbjNfMHU3MTEzcl9oM3JfNDNhMmU3YWYK" | base64 -d
# Output: 71m311n3_0u7113r_h3r_43a2e7af
```

The decoded string uses leetspeak (substituting numbers for letters):
| Leet | Letter |
|------|--------|
| 7 | t |
| 1 | i |
| 3 | e |

Decoded meaning:
- `71m311n3` = `timeline`
- `0u7113r` = `outlier`
- `h3r` = `her`
- `43a2e7af` = hash/identifier (stays as hex)

---

## 🚩 Flag
```
picoCTF{71m311n3_0u7113r_h3r_43a2e7af}
```

Which reads as: `picoCTF{timeline_outlier_her_43a2e7af}`

---

## 💡 Lessons Learned
1. **Timestomping Detection**: Creating MAC timelines is the most effective way to spot manipulated timestamps that hide malicious or hidden files. Anomalous dates (like 1985) immediately stand out against normal recent timestamps.
2. **Sleuth Kit Fundamentals**: `fls → body file → mactime` is the standard workflow for timeline analysis in forensics. The body file format is compatible with other timeline tools as well.
3. **Leetspeak Obfuscation**: Attackers often use simple substitutions (7=t, 1=i, 3=e) to hide meaningful strings while keeping them human-readable. Always consider character substitution when analyzing suspicious strings.
4. **Double Encoding**: The flag was base64 encoded before being stored - always check for multiple encoding layers when the initial content doesn't reveal a clear flag format.
5. **Anomaly Hunting**: In forensics, the anomaly (1985 timestamp) is often more valuable than searching for known patterns (like "flag"). Timeline analysis helps identify what doesn't belong.
