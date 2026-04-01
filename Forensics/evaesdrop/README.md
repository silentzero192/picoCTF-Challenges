# picoCTF 2022: Eavesdrop

- **Category:** Forensics
- **Difficulty:** Medium
- **Hint:** "All we know is that this packet capture includes a chat conversation and a file transfer."

## 📝 Challenge Description

The challenge provides a .pcap file. We need to analyze the network traffic to recover a secret file transferred during a chat session.

## 🛠️ Tools Used

- Wireshark (Traffic Analysis)
- tcpdump / strings (Initial Recon)
- OpenSSL (Decryption)

## 🚀 Solution

1. **Initial Analysis**

   First, we look for any human-readable text in the packet capture to understand the context of the "chat conversation."

   ```bash
   strings capture.flag.pcap | less
   ```

   Use code with caution.

   **Found Conversation:**

   In the output, we see a dialogue between two users. One user mentions sending a file and provides a specific decryption command:

   > "Hey, how do I decrypt this file?"
   >
   > "You can use this: openssl des3 -d -salt -in file.des3 -out file.txt -k capybara"

2. **Locating the File Transfer**

   We need to find the actual `file.des3` within the traffic.
   - Open `capture.flag.pcap` in Wireshark.
   - Go to **Statistics > Conversations > TCP**.
   - We see a few streams. Stream 0 is the chat. Stream 2 appears to contain binary data.
   - Apply the filter: `tcp.stream eq 2`.
   - Right-click a packet -> Follow > TCP Stream.

3. **Extracting the Encrypted File**

   In the "Follow TCP Stream" window, change the "Show data as" dropdown from ASCII to Raw.

   Notice the file starts with the magic bytes `Salted__`. This confirms it is an OpenSSL encrypted file.

   Click **Save as...** and name the file `file.des3`.

4. **Decrypting the Flag**

   Using the command recovered from the chat log (Step 1), we run the decryption:

   ```bash
   openssl des3 -d -salt -in file.des3 -out flag.txt -k capybara
   ```

   Use code with caution.

   Note: If `des3` throws a "deprecated" error on newer systems, add `-pbkdf2` or use an older version of OpenSSL.

5. **Reading the Flag**

   ```bash
   cat flag.txt
   ```

   Use code with caution.

   **Flag:** picoCTF{REDACTED}

## 💡 Key Takeaways

- **TCP Streams:** Always follow the streams to separate chat (control plane) from file transfers (data plane).
- **Raw Extraction:** When saving files from Wireshark, ensure you are in "Raw" mode to avoid encoding corruption.
- **OpenSSL:** Pay close attention to the flags (`-des3`, `-salt`, `-k`) provided in hints/chats.
