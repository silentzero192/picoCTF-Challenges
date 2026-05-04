# forensics-git0 CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | forensics-git0 |
| **Category** | Forensics |
| **Description** | Find the flag hidden in the disk image. |
| **Files Provided** | `disk.img` (1GB raw disk image) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **Disk Image Partition Analysis**: Raw disk images contain partition tables (MBR/GPT) that define where each filesystem begins. The `fdisk` tool reveals partition offsets, which are required by filesystem analysis tools like `fls` to correctly locate data within specific partitions.
2. **Git Repository Forensics**: Git repositories store metadata in the `.git` directory, including commit messages (`COMMIT_EDITMSG`), branch references (`HEAD`), and object data. The `COMMIT_EDITMSG` file often contains valuable information as it stores the most recent commit message, which can sometimes contain flags or hints in CTF challenges.

---

## 🔍 Step-by-Step Solution

### Step 1: Identify Disk Image Type
First, we verify the file type to confirm we're dealing with a disk image:
```bash
file disk.img
# Output: disk.img: DOS/MBR boot sector
```

The image is a raw disk with a Master Boot Record (MBR) containing multiple partitions.

---

### Step 2: Examine Partition Layout
We use `fdisk` to examine the partition structure:
```bash
fdisk -l disk.img
# Output:
# Disk disk.img: 1 GiB, 1073741824 bytes, 2097152 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: dos
# Disk identifier: 0x610b63c2
#
# Device     Boot   Start     End Sectors  Size Id Type
# disk.img1  *       2048  616447  614400  300M 83 Linux
# disk.img2        616448 1140735  524288  256M 82 Linux swap / Solaris
# disk.img3       1140736 2097151  956416  467M 83 Linux
```

The disk has three partitions:
| Partition | Start Sector | Size | Type |
|-----------|--------------|------|------|
| disk.img1 | 2048 | 300M | Linux (boot) |
| disk.img2 | 616448 | 256M | Linux swap |
| disk.img3 | 1140736 | 467M | Linux (data) |

The largest partition (disk.img3) is the most likely location for user data.

---

### Step 3: List Contents of Partition 3
Using The Sleuth Kit's `fls` tool with the partition offset to recursively list files:
```bash
fls -r -o 1140736 disk.img | head -30
# Output:
# d/d 64770:	home
# + d/d 64771:	ctf-player
# ++ d/d 65663:	Code
# +++ d/d 65664:	secrets
# ++++ d/d 65665:	.git
# +++++ d/d 65666:	branches
# +++++ r/r 65667:	description
# +++++ d/d 65668:	hooks
# ...
```

**Key Finding:** A `.git` directory exists at `/home/ctf-player/Code/secrets/.git` (inode 65665).

---

### Step 4: List All Files in the .git Directory
We list the contents of the `.git` directory using its Inode number:
```bash
fls -r -o 1140736 disk.img 65665
# Output:
# d/d 65666:	branches
# r/r 65667:	description
# d/d 65668:	hooks
# + r/r 65669:	applypatch-msg.sample
# + r/r 65670:	pre-commit.sample
# ...
# d/d 65689:	objects
# + d/d 65694:	46
# ++ r/r 65695:	064ac3ab7afd9a95bc1224aa8b4cef23741fcc
# + d/d 65697:	18
# ++ r/r 65698:	6ca660f488a4e4cdd92e7678fcfa3da478aee7
# + d/d 65699:	32
# ++ r/r 65700:	327681bb38cf467cec328eec9707b240e3e74ced
# r/r 65688:	HEAD
# r/r 65662:	index
# r/r 65693:	COMMIT_EDITMSG
# ...
```

Important files identified:
- `COMMIT_EDITMSG` (inode 65693) - contains the last commit message
- `HEAD` (inode 65688) - current branch reference
- `index` (inode 65662) - staging area
- Various git objects in `objects/` directory

---

### Step 5: Extract the Commit Message
The `COMMIT_EDITMSG` file typically contains the most recent commit message and is a prime location for flags. We extract it using `icat`:
```bash
mkdir git_repo
cd git_repo
icat -o 1140736 ../disk.img 65693 > COMMIT_EDITMSG
cat COMMIT_EDITMSG
# Output: Wrap this phrase in the flag format: g17_1n_7h3_d15k_041217d8
```

Success! The commit message contains the flag phrase.

---

## 🚩 Flag
```
picoCTF{g17_1n_7h3_d15k_041217d8}
```

---

## 💡 Lessons Learned
1. **Git Repository Artifacts**: The `.git` directory contains a wealth of information including commit messages, which can be valuable sources of hidden data in forensics challenges.
2. **TSK Workflow**: `fls` with recursive listing (`-r`) and offset (`-o`) allows navigation through filesystem structures without mounting, making it ideal for forensics work.
3. **Inode-Based File Recovery**: Tools like `icat` can extract file contents directly by Inode number, bypassing the need for filenames or directory structures.
4. **Partition Offsets**: Always identify partition boundaries using `fdisk` before using filesystem analysis tools - the offset in sectors is crucial for tools like `fls` and `icat` to work correctly.
