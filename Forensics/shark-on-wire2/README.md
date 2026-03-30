# shark-on-wire2 Writeup

## Challenge

**Category:** Forensics  
**Artifact:** `capture.pcap`  
**Flag format:** `picoCTF{...}`

## TL;DR

The obvious UDP payloads in the packet capture are mostly decoys. The real flag is hidden in a covert channel near the end of the capture:

- A UDP packet to destination port `22` contains the string `start`
- After that, several UDP packets from `10.0.0.66` to destination port `22` carry dummy payload `aaaaa`
- The **source port** of each of those packets encodes one character
- `source_port - 5000 = ASCII value`
- A final UDP packet to destination port `22` contains the string `end`

Recovered flag:

```text
picoCTF{p1LLf3r3d_data_v1a_st3g0}
```

## Files

```text
capture.pcap
```

## Initial Recon

First, identify what kind of file we were given:

```bash
file capture.pcap
capinfos capture.pcap
```

Useful output:

```text
capture.pcap: pcap capture file, microsecond ts (little-endian)
Number of packets: 1326
Capture duration: 1193.438759 seconds
```

Next, inspect the protocol mix:

```bash
tshark -r capture.pcap -q -z io,phs
```

Important takeaway:

```text
ip
  udp                                  frames:599
  tcp                                  frames:138
arp                                    frames:560
```

There is a lot of UDP traffic, which is a common place for CTF covert channels.

## Looking at UDP Conversations

To see which UDP streams stand out:

```bash
tshark -r capture.pcap -q -z conv,udp
```

Several flows look suspicious:

- `10.0.0.2:5000 -> 10.0.0.22:8990`
- `10.0.0.7:5000 -> 10.0.0.1:8990`
- `10.0.0.3:5000 -> 10.0.0.1:8990`
- `10.0.0.24:5000 -> 10.0.0.25:8990`
- `10.0.0.66:* -> 10.0.0.1:22`

Dumping UDP fields makes the early part of the capture look promising:

```bash
tshark -r capture.pcap -Y "udp && data" \
  -T fields \
  -e frame.number -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e udp.length -e data.data
```

Some payloads decode to readable strings:

```text
picoCTF Sure is fun!
I really want to find some picoCTF flags
```

There are also many single-byte UDP payloads such as:

```text
i i i c c o o C T F { N 0 t _ ...
```

At first glance this looks like it might be the flag.

## False Lead: Decoy Single-Byte Payloads

If we reconstruct only the one-byte UDP payloads in order, we get a noisy message:

```text
iiiccooCTFCTF{N0t_{StaTa_fLaffffffffffffffffffffffffffffffffffffffff31355g}_36f6e6e}zazazazaz...
```

That is a strong sign that the capture contains deliberate noise:

- repeated `f` packets
- long runs of `z` and `a`
- duplicated fragments like `CTF`
- partial strings that look flag-like but do not cleanly resolve

Breaking the one-byte packets down by flow makes the deception clear:

- `10.0.0.24 -> 10.0.0.25:8990` sends many `f` characters
- `10.0.0.7 -> 10.0.0.1:8990` sends many `z` characters
- `10.0.0.3 -> 10.0.0.1:8990` sends many `a` characters
- a few `8888` streams contain partial text fragments

These are distractions, not the final answer.

## Finding the Real Channel

Later in the capture there is a much cleaner pattern.

Dump the tail of the UDP traffic:

```bash
tshark -r capture.pcap -Y "frame.number>=985" \
  -T fields \
  -e frame.number -e frame.time_relative -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e udp.length -e data.data
```

Near the end we see this:

```text
1104  10.0.0.66:5000 -> 10.0.0.1:22  data="start"
...
1303  10.0.0.80:5000 -> 10.0.0.1:22  data="end"
```

Between `start` and `end`, many packets go to destination port `22` with payload `aaaaa`:

```text
10.0.0.66:5112 -> 10.0.0.1:22
10.0.0.66:5105 -> 10.0.0.1:22
10.0.0.66:5099 -> 10.0.0.1:22
10.0.0.66:5111 -> 10.0.0.1:22
...
```

The payload stays constant, which suggests the interesting data is not in the payload. That leaves packet metadata, and the source ports are the obvious candidate.

## Decoding Method

Take each packet from `10.0.0.66` to destination port `22` between the `start` and `end` markers.

For each packet:

```text
character = chr(source_port - 5000)
```

Examples:

| Source Port | Calculation | ASCII | Character |
|---|---:|---:|---|
| 5112 | 5112 - 5000 | 112 | `p` |
| 5105 | 5105 - 5000 | 105 | `i` |
| 5099 | 5099 - 5000 | 99 | `c` |
| 5111 | 5111 - 5000 | 111 | `o` |
| 5067 | 5067 - 5000 | 67 | `C` |
| 5084 | 5084 - 5000 | 84 | `T` |
| 5070 | 5070 - 5000 | 70 | `F` |
| 5123 | 5123 - 5000 | 123 | `{` |

That immediately spells:

```text
picoCTF{
```

Continuing the same process for the remaining packets reconstructs the full flag.

## Reproduction Script

This script extracts the flag directly from the PCAP:

```python
import subprocess

cmd = (
    "tshark -r capture.pcap -Y 'udp' "
    "-T fields -e frame.number -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e data.data"
)

out = subprocess.check_output(cmd, shell=True, text=True)

rows = []
for line in out.strip().splitlines():
    parts = line.split("\t")
    while len(parts) < 6:
        parts.append("")
    rows.append(parts)

start = None
end = None

for i, (frame, src, sport, dst, dport, data) in enumerate(rows):
    text = bytes.fromhex(data).decode("latin1") if data else ""
    if text == "start" and dport == "22":
        start = i
    if text == "end" and dport == "22":
        end = i
        break

flag = []
for frame, src, sport, dst, dport, data in rows[start + 1:end]:
    if src == "10.0.0.66" and dport == "22":
        flag.append(chr(int(sport) - 5000))

print("".join(flag))
```

## Verification

Running the extraction produces:

```text
picoCTF{p1LLf3r3d_data_v1a_st3g0}
```

You can also verify it manually from the packet list:

```text
5112 -> p
5105 -> i
5099 -> c
5111 -> o
5067 -> C
5084 -> T
5070 -> F
5123 -> {
...
5125 -> }
```

## Why This Works

This is a classic steganography/covert-channel trick inside network metadata:

- the payload is intentionally boring
- the actual message is stored in packet metadata
- source ports are used as ASCII values with an offset
- the `start` and `end` packets act as delimiters for the hidden message

The noisy earlier traffic is there to make simple string extraction or naive packet reconstruction produce misleading results.

## Final Flag

```text
picoCTF{p1LLf3r3d_data_v1a_st3g0}
```
