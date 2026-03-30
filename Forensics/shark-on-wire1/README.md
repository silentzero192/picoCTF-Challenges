# Shark on Wire - picoCTF Forensics Writeup

## Challenge Info

| Field | Value |
| --- | --- |
| Challenge | Shark on Wire |
| Category | Forensics |
| File Provided | `capture.pcap` |
| Flag Format | `picoCTF{...}` |

## TL;DR

The packet capture contains several noisy UDP conversations used as decoys. The real flag is hidden in a sequence of single-byte UDP payloads sent to port `8888`. Reassembling the bytes from UDP stream `6` reveals the actual flag:

```text
picoCTF{StaT31355_636f6e6e}
```

There is also a fake flag in UDP stream `7`:

```text
picoCTF{N0t_a_fLag}
```

That one is a decoy.

---

## Files

```text
capture.pcap
```

## Approach

The goal was to inspect the network capture, identify any suspicious traffic, and reconstruct the hidden data.

### 1. Initial Triage

First, confirm what kind of file we were given:

```bash
file capture.pcap
capinfos capture.pcap
```

Output:

```text
capture.pcap: pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet, capture length 262144)
```

```text
Number of packets:   2317
File size:           239 kB
Capture duration:    2261.673491 seconds
```

So this is a normal packet capture, small enough to inspect directly with `tshark`.

### 2. Get a High-Level Protocol Overview

To see which protocols are present:

```bash
tshark -r capture.pcap -q -z io,phs
```

Relevant output:

```text
eth                                      frames:2317 bytes:202359
  ip                                     frames:1230 bytes:113479
    udp                                  frames:1140 bytes:107983
      ssdp                               frames:128 bytes:27137
      llmnr                              frames:205 bytes:13924
      data                               frames:749 bytes:60996
      mdns                               frames:47 bytes:3955
```

The most suspicious line is:

```text
data                               frames:749 bytes:60996
```

That means a large amount of UDP traffic was not decoded as a known higher-level protocol. In CTFs, that is often where the flag lives.

### 3. Check UDP Conversations

Next, inspect UDP conversations:

```bash
tshark -r capture.pcap -q -z conv,udp | sed -n '1,35p'
```

Interesting lines:

```text
10.0.0.2:5000  <-> 10.0.0.5:8990    200 frames
10.0.0.9:5000  <-> 10.0.0.5:8990    135 frames
10.0.0.2:5000  <-> 10.0.0.22:8990   103 frames
10.0.0.2:5000  <-> 10.0.0.3:8990    100 frames
10.0.0.11:5000 <-> 10.0.0.5:8990     70 frames
10.0.0.24:5000 <-> 10.0.0.25:8990    40 frames
10.0.0.100:5000 <-> 10.0.0.88:8990   30 frames
10.0.0.2:5000  <-> 10.0.0.12:8888    27 frames
10.0.0.2:5000  <-> 10.0.0.13:8888    19 frames
```

At this point there are two strong possibilities:

- Large repetitive traffic to port `8990`
- Smaller byte-sized traffic to port `8888`

The `8990` traffic looked noisy and repetitive, so I checked whether the meaningful data might actually be in the smaller flows.

### 4. Extract Single-Byte UDP Payloads

To isolate tiny payloads:

```bash
tshark -r capture.pcap -Y "udp.dstport==8888 && data.len==1" \
  -T fields -e udp.stream -e frame.number -e ip.dst -e data.data
```

Output:

```text
6  63    10.0.0.12  70
7  65    10.0.0.13  70
8  67    10.0.0.15  69
6  69    10.0.0.12  69
7  73    10.0.0.13  69
6  75    10.0.0.12  63
7  79    10.0.0.13  63
6  81    10.0.0.12  6f
7  83    10.0.0.13  6f
7  97    10.0.0.13  43
7  99    10.0.0.13  54
7  101   10.0.0.13  46
6  519   10.0.0.12  43
6  521   10.0.0.12  54
6  523   10.0.0.12  46
7  669   10.0.0.13  7b
7  672   10.0.0.13  4e
7  674   10.0.0.13  30
7  676   10.0.0.13  74
7  679   10.0.0.13  5f
6  745   10.0.0.12  7b
6  747   10.0.0.12  53
6  750   10.0.0.12  74
6  752   10.0.0.12  61
6  754   10.0.0.12  54
7  806   10.0.0.13  61
7  808   10.0.0.13  5f
7  810   10.0.0.13  66
7  812   10.0.0.13  4c
7  814   10.0.0.13  61
6  900   10.0.0.12  33
6  902   10.0.0.12  31
6  904   10.0.0.12  33
6  906   10.0.0.12  35
6  908   10.0.0.12  35
7  910   10.0.0.13  67
7  912   10.0.0.13  7d
6  1328  10.0.0.12  5f
6  1330  10.0.0.12  36
6  1332  10.0.0.12  33
6  1334  10.0.0.12  36
6  1336  10.0.0.12  66
6  1338  10.0.0.12  36
6  1340  10.0.0.12  65
6  1344  10.0.0.12  36
6  1348  10.0.0.12  65
6  1350  10.0.0.12  7d
```

This is exactly what we want: single-byte payloads that look like ASCII hex values.

For example:

- `70` = `p`
- `69` = `i`
- `63` = `c`
- `6f` = `o`

So the traffic is clearly spelling out text one byte at a time.

---

## Reassembling the Streams

The key insight is that the one-byte payloads are split across multiple UDP streams.

### Stream 6

To reconstruct stream `6`:

```bash
tshark -r capture.pcap -Y "udp.stream==6 && data.len==1" \
  -T fields -e data.data | tr -d '\n' | xxd -r -p
```

Output:

```text
picoCTF{StaT31355_636f6e6e}
```

### Stream 7

To reconstruct stream `7`:

```bash
tshark -r capture.pcap -Y "udp.stream==7 && data.len==1" \
  -T fields -e data.data | tr -d '\n' | xxd -r -p
```

Output:

```text
picoCTF{N0t_a_fLag}
```

### Stream 8

Stream `8` only contributes a single byte:

```text
69
```

That is just `i` and is not useful by itself.

---

## Why Stream 7 Is a Decoy

At first glance, stream `7` also produces something that matches the expected flag format:

```text
picoCTF{N0t_a_fLag}
```

But that string literally says "Not a flag", so it is clearly meant to distract solvers.

The actual flag comes from stream `6`, which reconstructs into a plausible picoCTF flag and does not contradict itself.

---

## Why the Other UDP Traffic Was Noise

There is a lot of repetitive traffic to port `8990`. Some of it contains patterns like:

```text
62 repeated many times -> 'b'
63 repeated many times -> 'c'
66 repeated many times -> 'f'
7a repeated many times -> 'z'
```

There are also repeated filler strings such as:

```text
fjdsakf;lankeflksanlkfdn
fjdsakafsdbanlkfdn
aaaaa
AAAAAAAAAAAAAAAA...
```

These are classic CTF distractions. They generate lots of suspicious-looking network traffic, but they do not form the final flag. The cleanest signal is the small set of one-byte payloads on port `8888`.

---

## Full Solve Path

If I were solving this from scratch again, the shortest reliable path would be:

```bash
file capture.pcap
tshark -r capture.pcap -q -z io,phs
tshark -r capture.pcap -q -z conv,udp | sed -n '1,35p'
tshark -r capture.pcap -Y "udp.dstport==8888 && data.len==1" -T fields -e udp.stream -e data.data
tshark -r capture.pcap -Y "udp.stream==6 && data.len==1" -T fields -e data.data | tr -d '\n' | xxd -r -p
```

That final command directly prints:

```text
picoCTF{StaT31355_636f6e6e}
```

---

## Final Flag

```text
picoCTF{StaT31355_636f6e6e}
```

## Notes

- Do not stop at the first flag-shaped string in a PCAP.
- If a candidate literally says it is fake, it probably is.
- In packet captures, tiny repeated payloads are often more important than the largest conversations.
