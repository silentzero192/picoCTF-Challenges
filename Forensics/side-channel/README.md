# side-channel CTF Writeup

---

## 📋 Challenge Information
| Detail | Value |
|--------|-------|
| **Challenge Name** | side-channel |
| **Category** | Forensics / Cryptography |
| **Description** | There's something fishy about this `pin_checker` binary. Can you figure out the PIN and get the flag from the master server? |
| **Files Provided** | `pin_checker` (ELF executable binary) |
| **Flag Format** | `picoCTF{...}` |

---

## 🧠 Background
This challenge tests understanding of two core concepts:
1. **Timing Side-Channel Attacks**: A timing attack is a side-channel attack where an attacker measures the time a system takes to execute operations. If a program compares a PIN digit-by-digit and performs additional operations for each correct digit (like a delay or nested check), the execution time increases measurably with each correct digit, revealing the secret.
2. **Incremental Brute Force**: Unlike traditional brute force that tries all combinations blindly, a timing side-channel allows an iterative approach - discovering one digit at a time by measuring which candidate causes a noticeable increase in execution time, then locking that digit and moving to the next position.

---

## 🔍 Step-by-Step Solution

### Step 1: Initial Analysis
We start by making the binary executable and running it with a random 8-digit PIN:
```bash
chmod +x pin_checker
./pin_checker
# Input: 12345678
# Output: Access Denied.
```

The binary expects an 8-digit PIN and provides feedback on whether it's correct.

---

### Step 2: Measure Execution Time
Using the Linux `time` command, we measure how long the program takes to run. We test digits 0-9 for the first position:

```bash
time echo "00000000" | ./pin_checker  # ~0.1s
time echo "10000000" | ./pin_checker  # ~0.1s
time echo "20000000" | ./pin_checker  # ~0.1s
time echo "30000000" | ./pin_checker  # ~0.1s
time echo "40000000" | ./pin_checker  # ~0.25s <-- Noticeable jump!
```

The jump in time (from ~0.1s to ~0.25s) indicates that `4` is the correct first digit. The program performs additional operations when a digit is correct.

---

### Step 3: Iterative Brute-Force
We repeat this process for each subsequent digit. For each correct digit found, the total execution time increases by approximately 0.1s to 0.15s:

```bash
time echo "40000000" | ./pin_checker  # ~0.25s
time echo "48000000" | ./pin_checker  # ~0.40s
time echo "48300000" | ./pin_checker  # ~0.55s
time echo "48390000" | ./pin_checker  # ~0.70s
time echo "48390500" | ./pin_checker  # ~0.85s
time echo "48390510" | ./pin_checker  # ~1.00s
time echo "48390513" | ./pin_checker  # ~1.15s
```

After testing each position, the recovered PIN is: **48390513**

---

### Step 4: Local Verification
Running the binary with the full PIN locally confirms it is correct:
```bash
./pin_checker
# Please enter your 8-digit PIN code:
# 48390513
# Checking PIN...
# Access granted. You may use your PIN to log into the master server.
```

---

### Step 5: Retrieve the Flag
Finally, we connect to the picoCTF master server using `nc` and enter the discovered PIN:
```bash
nc saturn.picoctf.net 59511
# Output:
# Verifying that you are a human...
# Please enter the master PIN code:
# 48390513
# Password correct. Here's your flag:
# picoCTF{t1m1ng_4tt4ck_eb4d7efb}
```

---

## 🚩 Flag
```
picoCTF{t1m1ng_4tt4ck_eb4d7efb}
```

---

## 💡 Lessons Learned
1. **Timing Leaks**: Poorly implemented comparison functions that return early on mismatch (or add work on match) create timing side-channels. Constant-time comparison functions should be used for security-critical checks.
2. **Measuring Execution Time**: The `time` command in Linux (or `time.perf_counter()` in Python) provides sufficient precision to detect timing differences as small as milliseconds when the effect is amplified across multiple iterations.
3. **Side-Channel Defense**: Developers should use constant-time comparison algorithms (like `CRYPTO_memcmp`) and avoid branching or early returns based on secret data to prevent timing attacks.
4. **Practical Exploitation**: Timing attacks don't require sophisticated tools - even basic shell commands with `time` can exploit significant timing differences in vulnerable binaries.
