# forensics-git1 CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | forensics-git1 |
| **Category** | Forensics |
| **Description** | How can you checkout the files of a previous commit? Analyze the given file carefully and find the flag. |
| **Files Provided** | `disk.img` (1GB raw disk image) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **Git Object Persistence**: Git stores all committed file versions as compressed objects in the `.git/objects` directory. Even if a file is deleted in a newer commit, its contents remain in the object store if it was committed in a prior version.
2. **Disk Image Analysis Without Mounting**: When root privileges are unavailable to mount a disk image, `debugfs` (ext filesystem debugger) can read ext4 filesystem contents directly from the image.

---

## 🔍 Step-by-Step Solution

### Step 1: Initial Enumeration
First, we inspect the provided disk image to understand its structure:
```bash
ls -la
# Output: -rw-r--r-- 1 jilani jilani 1073741824 Nov 19 14:25 disk.img

file disk.img
# Output: DOS/MBR boot sector; 3 partitions (2 Linux ext4, 1 swap)
```

The `file` output reveals Partition 3 (start sector: 1140736) is an ext4 Linux filesystem, which is our target.

---

### Step 2: Extract the Ext4 Partition
We use `dd` to extract Partition 3 from the full disk image into a separate file for easier analysis:
```bash
dd if=disk.img of=/tmp/opencode/partition3.img bs=512 skip=1140736 count=956416
file /tmp/opencode/partition3.img
# Output: Linux rev 1.0 ext4 filesystem data
```

---

### Step 3: Explore the Filesystem with `debugfs`
Since we cannot use `sudo` to mount the partition, we use `debugfs` to read the ext4 filesystem directly:
```bash
# List root directory contents of the extracted partition
debugfs -R "ls -l" /tmp/opencode/partition3.img
```

We find a user home directory at `home/ctf-player/Code/secrets` containing a `.git` folder, confirming a Git repository exists here.

---

### Step 4: Analyze the Git Repository
We inspect the `.git` directory to gather context about the repository state:
```bash
# Check current branch (HEAD)
debugfs -R "cat home/ctf-player/Code/secrets/.git/HEAD" /tmp/opencode/partition3.img
# Output: ref: refs/heads/master

# Check the last commit message
debugfs -R "cat home/ctf-player/Code/secrets/.git/COMMIT_EDITMSG" /tmp/opencode/partition3.img
# Output: Remove flag  <-- Critical hint!
```

The commit message "Remove flag" tells us the flag was present in a previous commit and deleted in the current version.

---

### Step 5: Retrieve Full Commit History
We read the Git reflog (stored in `.git/logs/HEAD`) to see all commits made to the repository:
```bash
debugfs -R "cat home/ctf-player/Code/secrets/.git/logs/HEAD" /tmp/opencode/partition3.img
# Output:
# 0000000000000000000000000000000000000000 177789af0b300e043ea8f54ea57d6cee352291ae ctf-player <ctf-player@example.com> 1763544005 +0000	commit (initial): Add flag
# 177789af0b300e043ea8f54ea57d6cee352291ae 5fb8194539c770a830b8ba089a50778c07072b03 ctf-player <ctf-player@example.com> 1763544005 +0000	commit: Remove flag
```

We now have two commits:
- Initial commit: `177789af0b300e043ea8f54ea57d6cee352291ae` (Message: "Add flag")
- Current commit: `5fb8194539c770a830b8ba089a50778c07072b03` (Message: "Remove flag")

---

### Step 6: Extract the Initial Commit Object
Git objects are stored as zlib-compressed files in `.git/objects` (first 2 characters of the hash are the subdirectory name). We extract and decompress the initial commit object:
```bash
# Extract the commit object
debugfs -R "cat home/ctf-player/Code/secrets/.git/objects/17/7789af0b300e043ea8f54ea57d6cee352291ae" /tmp/opencode/partition3.img > /tmp/commit_obj

# Decompress with Python (zlib-flate is unavailable)
python3 -c "import zlib; data=open('/tmp/commit_obj','rb').read(); print(zlib.decompress(data).decode())"
# Output:
# commit 179
# tree a62340e078686778969b9a555fc722147cf14e5a
# author ctf-player <ctf-player@example.com> 1763544005 +0000
# committer ctf-player <ctf-player@example.com> 1763544005 +0000
# 
# Add flag
```

The commit points to a tree object `a62340e078686778969b9a555fc722147cf14e5a`, which lists all files in this commit.

---

### Step 7: Extract the Tree Object to Find the Flag File
We extract and decompress the tree object to find the file containing the flag:
```bash
debugfs -R "cat home/ctf-player/Code/secrets/.git/objects/a6/2340e078686778969b9a555fc722147cf14e5a" /tmp/opencode/partition3.img > /tmp/tree_obj
python3 -c "import zlib; data=open('/tmp/tree_obj','rb').read(); print(zlib.decompress(data))"
# Output:
# b'tree 36\x00100644 flag.txt\x00\xf1P\xf4z]\xab\xfbC\x97pj\xa1\x89\x05\xdf\x93e\x95\xa8n'
```

This reveals a file named `flag.txt` in the initial commit, with the blob hash `f150f47a5dabfb4397706aa18905df936595a86e` (the 20-byte hash after the null separator).

---

### Step 8: Extract the Flag Blob
Finally, we extract and decompress the `flag.txt` blob object to get the flag:
```bash
debugfs -R "cat home/ctf-player/Code/secrets/.git/objects/f1/50f47a5dabfb4397706aa18905df936595a86e" /tmp/opencode/partition3.img > /tmp/flag_blob
python3 -c "import zlib; data=open('/tmp/flag_blob','rb').read(); print(zlib.decompress(data).decode())"
# Output:
# blob 31
# picoCTF{g17_r3m3mb3r5_d4ddf904}
```

---

## 🚩 Flag
```
picoCTF{g17_r3m3mb3r5_d4ddf904}
```

---

## 💡 Lessons Learned
1. Git never truly deletes committed data unless you run garbage collection and prune unreferenced objects. Historical file versions are always accessible if you know the commit hash.
2. `debugfs` is an essential tool for forensics work when you need to read ext filesystems without mounting them.
3. When standard compression tools are unavailable, Python's built-in `zlib` module can decompress Git objects (which use standard zlib compression).
