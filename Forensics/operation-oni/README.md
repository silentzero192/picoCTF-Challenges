# operation-oni CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | operation-oni |
| **Category** | Forensics |
| **Description** | Recover a hidden SSH private key from a disk image and use it to log into a remote server to retrieve the flag. |
| **Files Provided** | `disk.img` (230MB raw disk image) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **Disk Image Partition Analysis**: Raw disk images contain partition tables that define where each filesystem begins. Tools like `fdisk` can reveal partition offsets, which are required by filesystem analysis tools to correctly locate data.
2. **Filesystem Forensics with TSK (The Sleuth Kit)**: When analyzing disk images, `fls` and `icat` from TSK allow you to list files and extract contents by Inode number without mounting the filesystem, which is essential for forensics work.

---

## 🔍 Step-by-Step Solution

### Step 1: Analyze the Disk Image
First, we inspect the provided disk image to understand its partition structure:
```bash
fdisk -l disk.img
# Output:
# Disk disk.img: 230 MiB, 241172480 bytes, 471040 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
#
# Device     Boot Start       End   Sectors   Size Id Type
# disk.img1  *     2048    206847    204800   100M 83 Linux
# disk.img2       206848    471039    264192   129M 83 Linux
```

The disk contains two Linux partitions:
- **Partition 1**: Starts at sector 2048 (Boot partition)
- **Partition 2**: Starts at sector 206848 (Root/Data partition) - this is our target

---

### Step 2: Search for SSH Keys
SSH private keys are typically stored in a user's `~/.ssh` directory. We use `fls` from The Sleuth Kit to recursively search the second partition for any `.ssh` directories:
```bash
fls -r -o 206848 disk.img | grep ".ssh"
# Output: + d/d 3916: .ssh
```

The `.ssh` directory was found at **Inode 3916**.

---

### Step 3: Locate the Private Key Inode
We list the contents of the `.ssh` directory using its Inode number to find the actual key files:
```bash
fls -o 206848 disk.img 3916
# Output:
# r/r 2345:    id_ed25519
# r/r 2346:    id_ed25519.pub
```

The private key (`id_ed25519`) is located at **Inode 2345**.

---

### Step 4: Extract the Private Key
We use `icat` to extract the raw content of the private key from the disk image and save it to our local machine:
```bash
icat -o 206848 disk.img 2345 > id_ed25519
cat id_ed25519
# Output:
# -----BEGIN OPENSSH PRIVATE KEY-----
# b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAlwAAAAdzc2gtcn
# ...
# -----END OPENSSH PRIVATE KEY-----
```

---

### Step 5: Connect via SSH
SSH requires private keys to have strict permissions (read/write only by the owner). We fix the permissions and connect to the remote challenge server:
```bash
# Set proper permissions for the private key
chmod 600 id_ed25519

# Connect to the remote host provided in the challenge
ssh -i id_ed25519 -p 63793 ctf-player@saturn.picoctf.net
# Output: ctf-player@challenge:~$
```

---

### Step 6: Retrieve the Flag
Once logged in, we list the home directory and read the flag file:
```bash
ctf-player@challenge:~$ ls
# Output: flag.txt

ctf-player@challenge:~$ cat flag.txt
# Output: picoCTF{k3y_5l3u7h_b5066e83}
```

---

## 🚩 Flag
```
picoCTF{k3y_5l3u7h_b5066e83}
```

---

## 💡 Lessons Learned
1. **Partition Offsets**: Tools like `fls` and `icat` require the `-o` flag with the partition offset (in sectors) to correctly locate the filesystem within a raw disk image. Without this offset, the tools cannot interpret the filesystem structure.
2. **Inode Navigation**: Directories in a filesystem are just special files containing pointers to other files. By listing a directory using its Inode number, you can discover the Inodes of files contained within, allowing precise file extraction.
3. **TSK (The Sleuth Kit)**: A powerful suite of forensics tools for analyzing disk images without mounting - `fls` lists files and directories, `icat` extracts file contents by Inode, and `fsstat` displays filesystem statistics.
4. **SSH Key Security**: Private keys must have permissions set to `600` (read/write for owner only), or the SSH client will refuse to use them for security reasons.
