# picoCTF Writeup: Trivial Flag Transfer Protocol (Forensics)

## Description
Figure out how they moved the flag.

## Solution

### 1. Extract Files from PCAP
The provided file is a packet capture of **TFTP** traffic. 
- Open `tftp.pcapng` in **Wireshark**.
- Navigate to `File > Export Objects > TFTP...`.
- Click **Save All** to extract: `instructions.txt`, `plan`, `program.deb`, `picture1.bmp`, `picture2.bmp`, and `picture3.bmp`.

### 2. Decode the Hints
The text files are encoded with **ROT13**.
- **instructions.txt** decodes to: `TFTP DOESNT ENCRYPT OUR TRAFFIC SO WE MUST DISGUISE OUR FLAG TRANSFER. I USED THE PROGRAM. ENCRYPTED THE FLAG AND USED THE PESKY PHOTO TO HIDE IT. [...]`
- **plan** decodes to: `I USED THE PROGRAM AND HID IT WITH - DUEDILIGENCE. CHECK OUT THE PHOTOS`

### 3. Identify the Tool
The `program.deb` file is an installer for **steghide**, a steganography tool. The word **DUEDILIGENCE** is the passphrase for extraction.

### 4. Extract the Flag
Use `steghide` on the extracted images using the discovered passphrase. The flag is hidden in `picture3.bmp`.

```bash
# Install steghide if needed: sudo apt install steghide
steghide extract -sf picture3.bmp -p DUEDILIGENCE
