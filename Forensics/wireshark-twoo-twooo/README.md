# picoCTF Writeup: Wireshark twoo twooo two twoo... (Forensics)

## Solution

### 1. Analysis
The PCAP contains numerous HTTP packets with decoy flags. The real flag is hidden via **DNS Exfiltration** within subdomains of `reddshrimpandherring.com`.

### 2. Filtering
Filter for DNS traffic directed at the suspicious IP `18.217.1.57`:
`dns and ip.dst == 18.217.1.57`

### 3. Extraction & Decoding
The subdomains contain Base64 encoded fragments. Concatenating these fragments in order yields:
`cGljb0NURntkbnNfM3hmMWxfZnR3X2RlYWRiZWVmfQ==`

Decoding this string reveals the flag.

## Flag
`picoCTF{dns_3xf1l_ftw_deadbeef}`
