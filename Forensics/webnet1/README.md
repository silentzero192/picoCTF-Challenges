# webnet1 CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | webnet1 |
| **Category** | Forensics |
| **Description** | We found this packet capture and key. Recover the flag. |
| **Files Provided** | `capture.pcap` (PCAP packet capture), `picopico.key` (RSA private key), `vulture.jpg` (extracted image) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **TLS Decryption and Object Extraction**: Like webnet0, this challenge requires decrypting TLS traffic using an RSA private key in Wireshark. Additionally, it involves extracting transferred files from HTTP sessions using Wireshark's "Export Objects" feature, which can reconstruct files from HTTP response data.
2. **Image Metadata Forensics**: Digital images often contain EXIF metadata (camera settings, timestamps, GPS coordinates, and sometimes hidden data) that isn't visible in the image itself. Tools like `exiftool` and `strings` can reveal this hidden information, which is often used to hide flags in CTF challenges.

---

## 🔍 Step-by-Step Solution

### Step 1: Configure TLS Decryption
Just like in webnet0, the traffic is encrypted. We must provide the private key to Wireshark to view the underlying HTTP data:

1. Open `capture.pcap` in **Wireshark**
2. Navigate to **Edit → Preferences → Protocols → TLS**
3. Click **Edit** next to **RSA keys list**
4. Add a new entry with the following details:
   - **IP Address**: `any`
   - **Port**: `any`
   - **Protocol**: `http`
   - **Key File**: Select your local copy of `picopico.key`
5. Click **OK** to apply

---

### Step 2: Identify the Target
Once decrypted, look for HTTP traffic. A decoy flag is often present in the HTTP response headers:
```
Pico-Flag: picoCTF{this.is.not.your.flag.anymore}
```

Following the hint that the real flag is elsewhere, notice the presence of an image file being transferred in the decrypted stream: `vulture.jpg`.

---

### Step 3: Extract the Image
We use Wireshark's object export feature to extract the image:

1. Go to **File → Export Objects → HTTP...**
2. Locate `vulture.jpg` in the list of objects
3. Select it and click **Save** to export it to your working directory

Alternatively, you can use `tcpflow` or manually reconstruct the file from the HTTP response data.

---

### Step 4: Extract the Hidden Flag
Standard image analysis involves checking for hidden strings or metadata. We use `exiftool` to examine the image's metadata:

```bash
exiftool vulture.jpg
# Output reveals various EXIF metadata fields
# The flag is hidden within one of the metadata fields
```

Alternatively, you can use the `strings` command to find the flag:
```bash
strings vulture.jpg | grep picoCTF
# Output: picoCTF{honey.roasted.peanuts}
```

The flag is found embedded in the file's EXIF metadata.

---

## 🚩 Flag
```
picoCTF{honey.roasted.peanuts}
```

---

## 💡 Lessons Learned
1. **Decoy Flags**: CTF challenges often include decoy flags to mislead participants. Always verify if a found flag is the real one or continue investigating when hints suggest otherwise.
2. **File Carving from PCAP**: Wireshark's "Export Objects" feature can reconstruct files transferred over HTTP without manual packet reassembly. This works for images, documents, and other files sent in HTTP responses.
3. **EXIF Metadata as a Hiding Place**: Image files store extensive metadata that's invisible to casual viewing. Always run `exiftool` or `strings` on image files recovered from any source - flags are commonly hidden in fields like `Comment`, `UserComment`, `ImageDescription`, or `Artist`.
4. **Multi-Stage Challenges**: This challenge combines network forensics (TLS decryption) with file analysis (image metadata extraction), demonstrating how real-world investigations often require multiple skill sets.
