# picoCTF - File-Types (Forensics)

## Challenge Description
The challenge provides a file named `Flag.pdf` which is actually a series of nested archives, starting with a Shell Archive (SHAR).

## Solution
The challenge is a "Russian Doll" style extraction. Each step involves identifying the file type and using the appropriate decompression tool.

### Extraction Steps:
1. **SHAR**: `chmod +x Flag.pdf && ./Flag.pdf` (extracted `flag`)
2. **AR**: `ar x flag`
3. **CPIO**: `cpio -ivu < flag`
4. **Bzip2**: `bunzip2 flag`
5. **Gzip**: `gunzip flag`
6. **Lzip**: `lzip -d flag`
7. **LZ4**: `lz4 -d flag.lz4 flag`
8. **LZMA**: `lzma -d flag`
9. **LZOP**: `lzop -d flag`
10. **Lzip**: `lzip -d flag`
11. **XZ**: `xz -d flag`

### Final Decoding:
After the final extraction, the file `flag` contained a Hex-encoded string:
`7069636f4354467b66316c656e406d335f6d406e3170756c407431306e5f6630725f3062326375723137795f37396230316332367d0a`

To get the plaintext flag:
```bash
cat flag | xxd -r -p
