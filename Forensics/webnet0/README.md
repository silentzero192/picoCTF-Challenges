# webnet0 CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | webnet0 |
| **Category** | Forensics |
| **Description** | We found this packet capture and key. Recover the flag. |
| **Files Provided** | `capture.pcap` (PCAP packet capture), `picopico.key` (RSA private key) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **TLS Decryption with RSA Private Keys**: When RSA key exchange is used in TLS connections (TLS 1.2 and earlier), having the server's private key allows Wireshark to decrypt the entire session. This is possible because the session keys are derived from the RSA-encrypted premaster secret that can be decrypted with the private key.
2. **HTTP Protocol Analysis in Wireshark**: After decrypting TLS traffic, HTTP requests and responses become visible. Custom HTTP headers often contain sensitive information like flags, API keys, or authentication tokens that are transmitted in cleartext over the encrypted channel.

---

## 🔍 Step-by-Step Solution

### Step 1: Analyze the Files
We start by checking the provided files:
```bash
ls
# Output: capture.pcap  picopico.key

file picopico.key
# Output: picopico.key: OpenSSH private key (no password)
```

Opening `capture.pcap` in Wireshark shows mostly TLSv1.2 traffic. Since the traffic is encrypted, we cannot see the HTTP requests or the flag directly.

---

### Step 2: Decrypt the TLS Traffic
To view the underlying data, we must provide Wireshark with the private key found in `picopico.key`:

1. Open Wireshark and load `capture.pcap`
2. Go to **Edit → Preferences**
3. Expand **Protocols** on the left and select **TLS** (or SSL in older versions)
4. Next to **RSA keys list**, click **Edit**
5. Click the **+** icon and fill in the following:
   - **IP Address**: `any`
   - **Port**: `any`
   - **Protocol**: `http`
   - **Key File**: Select the path to your `picopico.key`
6. Click **OK** on both windows

---

### Step 3: Find the Flag
Once the key is applied, Wireshark decrypts the traffic. New HTTP protocol packets will appear in the list.

```bash
# Apply display filter to show only HTTP traffic
http
```

Select any of the HTTP packets (e.g., a GET request or a 200 OK response). Right-click the packet and select **Follow → HTTP Stream** (or **Follow → TLS Stream**).

In the stream window, look through the HTTP headers. The flag is located in one of the custom HTTP response headers:

```
HTTP/1.1 200 OK
Date: Mon, 15 Nov 2021 00:58:00 GMT
Server: Apache
Pico-Flag: picoCTF{nongshim.shrimp.crackers}
Content-Type: text/html; charset=UTF-8
```

---

## 🚩 Flag
```
picoCTF{nongshim.shrimp.crackers}
```

---

## 💡 Lessons Learned
1. **RSA Key Exchange Vulnerability**: When RSA key exchange is used (not Diffie-Hellman), anyone with the server's private key can decrypt all past and future traffic captured for that server. Modern TLS configurations use ephemeral Diffie-Hellman (DHE/ECDHE) to provide forward secrecy.
2. **Wireshark TLS Decryption**: Wireshark's TLS dissector can use RSA private keys to decrypt sessions. The key must match the server's certificate, and the protocol must be correctly specified (http in this case).
3. **Custom HTTP Headers**: Applications often use custom HTTP headers (like `Pico-Flag`) to transmit metadata. These headers are visible in decrypted traffic and are a common place to hide CTF flags.
4. **PCAP Analysis Workflow**: The standard workflow for encrypted traffic analysis is: capture → obtain key → configure Wireshark → decrypt → follow stream → extract data.
