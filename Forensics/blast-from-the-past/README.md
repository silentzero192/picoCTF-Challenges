# blast-from-the-past CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | blast-from-the-past |
| **Category** | Forensics |
| **Description** | The judge for these pictures is a real fan of antiques. Can you age this photo to the specifications? Set the timestamps on this picture to 1970:01:01 00:00:00.001+00:00 with as much precision as possible for each timestamp. |
| **Files Provided** | `original.jpg` (JPEG image file) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **EXIF Metadata Manipulation**: JPEG images contain Exchangeable Image File Format (EXIF) metadata that stores camera settings, timestamps, and other information. Tools like `exiftool` can read and modify these timestamps, including sub-second precision fields.
2. **Binary File Hex Editing**: Some proprietary metadata fields (like Samsung's TimeStamp) are not accessible through standard EXIF tools. In such cases, identifying the exact byte offset of the data and performing precise binary overwrites using Python ensures the file structure remains intact while modifying the target data.

---

## 🔍 Step-by-Step Solution

### Step 1: Initial Analysis
First, we inspect the JPEG image to understand its current metadata:
```bash
exiftool original.jpg
# Output reveals several timestamp fields including:
# ModifyDate: 2023:11:20 14:13:00
# DateTimeOriginal: 2023:11:20 14:13:00
# CreateDate: 2023:11:20 14:13:00
# Samsung:TimeStamp: 1700513181420 (13-digit Unix millisecond integer)
```

The challenge requires modifying all timestamps to Unix Epoch + 1ms: `1970:01:01 00:00:00.001+00:00`.

---

### Step 2: Modify Standard EXIF Metadata
We use `exiftool` to modify the standard EXIF timestamp tags and their sub-second components:
```bash
exiftool "-AllDates=1970:01:01 00:00:00.001" \
         "-SubSecTimeOriginal=001" \
         "-SubSecTimeDigitized=001" \
         "-SubSecTime=001" \
         "-OffsetTime=+00:00" \
         "-OffsetTimeOriginal=+00:00" \
         "-OffsetTimeDigitized=+00:00" \
         original.jpg -overwrite_original
```

This sets:
- `ModifyDate`, `DateTimeOriginal`, `CreateDate` to `1970:01:01 00:00:00`
- Sub-second fields to `001` (representing 0.001 seconds)
- Timezone offsets to `+00:00`

---

### Step 3: Locate the Hidden Samsung Timestamp
Standard EXIF tools cannot modify proprietary manufacturer trailers. We search for the 13-digit Unix millisecond timestamp:
```bash
grep -aobP "\d{13}" original.jpg
# Output: 2851584:1700513181420
```

The target timestamp `1970:01:01 00:00:00.001` in Unix milliseconds is `1`. To maintain the 13-character string length, we overwrite it with `0000000000001`.

---

### Step 4: Hex Manipulation via Python
We perform an in-place binary overwrite at the identified offset to avoid corrupting the JPEG structure:
```bash
python3 -c 'with open("original.jpg", "r+b") as f: f.seek(2851584); f.write(b"0000000000001")'
```

This directly modifies the Samsung TimeStamp field while preserving the rest of the file structure.

---

### Step 5: Verification and Submission
Finally, we verify all timestamps and submit the file to the challenge server:
```bash
# Verify timestamps with exiftool
exiftool original.jpg

# Upload the file to the challenge server
nc -w 2 mimas.picoctf.net 60234 < original.jpg

# Check results
nc mimas.picoctf.net 51294
```

**Verification Results:**
```
ModifyDate: 1970:01:01 00:00:00 ✅
DateTimeOriginal: 1970:01:01 00:00:00 ✅
CreateDate: 1970:01:01 00:00:00 ✅
SubSecCreateDate: 1970:01:01 00:00:00.001 ✅
SubSecDateTimeOriginal: 1970:01:01 00:00:00.001 ✅
SubSecModifyDate: 1970:01:01 00:00:00.001 ✅
Samsung:TimeStamp: 1970:01:01 00:00:00.001+00:00 ✅
```

---

## 🚩 Flag
```
picoCTF{71m3_7r4v311ng_p1c7ur3_83ecb41c}
```

---

## 💡 Lessons Learned
1. **EXIF Metadata Precision**: JPEG images can store timestamps with sub-second precision through special EXIF tags like `SubSecTime*`. All timestamp fields must be consistent for forensic validation.
2. **Proprietary Metadata Fields**: Manufacturer-specific metadata (like Samsung's TimeStamp) may not be accessible through standard tools, requiring direct binary manipulation at known offsets.
3. **Binary File Safety**: When modifying binary files like JPEGs, always use seek-and-write operations at precise offsets rather than string replacement, which could corrupt the file structure.
4. **Unix Time Representation**: Unix timestamps can be represented in seconds or milliseconds. The 13-digit format represents milliseconds since epoch, where `1` = 1970-01-01 00:00:00.001.
