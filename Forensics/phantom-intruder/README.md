# Ph4nt0m 1ntrud3r

## Challenge Info

- **Category:** Forensics
- **Name:** `Ph4nt0m 1ntrud3r`
- **Description:** A digital ghost has breached my defenses, and my sensitive data has been stolen. The goal is to analyze the provided PCAP, identify how the attacker hid the data, and recover the flag.
- **Hint:** `Filter your packets to narrow down your search. Attacks were done in timely manner. Time is essential`
- **Flag format:** `picoCTF{...}`

## Files

- [`myNetworkTraffic.pcap`](./myNetworkTraffic.pcap)

## TL;DR

The PCAP only contains 22 TCP SYN packets from `192.168.0.2:20` to `192.168.1.2:80`.  
Each packet carries a small payload that looks like Base64.  
The important trick is that the packets are **not stored in chronological order**.

Once the packets are sorted by their **actual timestamps**, the final Base64 chunks decode into the flag.

## Initial Recon

Start by checking basic capture metadata:

```bash
capinfos myNetworkTraffic.pcap
```

Interesting result:

```text
Number of packets:   22
Strict time order:   False
```

That `Strict time order: False` line is the biggest clue. It means the packets in the file are not arranged by time, which matches the hint that **time is essential**.

## Inspecting the Traffic

Listing packets with `tshark` shows only SYN packets with payloads:

```bash
tshark -r myNetworkTraffic.pcap
```

To extract the exact timestamps and payloads:

```bash
tshark -r myNetworkTraffic.pcap -T fields -e frame.time_epoch -e tcp.payload
```

This produces entries like:

```text
1741231902.550317000  657a46305833633063773d3d
1741231902.551541000  66513d3d
1741231902.551325000  4e4749314e7a6b774f513d3d
...
```

Those hex payloads convert to ASCII strings such as:

```text
ezF0X3c0cw==
fQ==
NGI1NzkwOQ==
...
```

These are clearly Base64 fragments.

## Key Observation

If you decode the fragments in **file order**, the result is mostly garbage.

If you sort them by `frame.time_epoch`, the later packets form readable text:

```text
cGljb0NURg== -> picoCTF
ezF0X3c0cw== -> {1t_w4s
bnRfdGg0dA== -> nt_th4t
XzM0c3lfdA== -> _34sy_t
YmhfNHJfZA== -> bh_4r_d
NGI1NzkwOQ== -> 4b57909
fQ==         -> }
```

Concatenating them gives:

```text
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_d4b57909}
```

## Reproduction

One easy way to reproduce the solve is:

```bash
tshark -r myNetworkTraffic.pcap -T fields -e frame.time_epoch -e tcp.payload
```

Then sort the output by timestamp and decode the final meaningful Base64 chunks.

For a quick Python reproduction:

```python
import base64

rows = [
    (1741231902.550085000, "cGljb0NURg=="),
    (1741231902.550317000, "ezF0X3c0cw=="),
    (1741231902.550547000, "bnRfdGg0dA=="),
    (1741231902.550867000, "XzM0c3lfdA=="),
    (1741231902.551103000, "YmhfNHJfZA=="),
    (1741231902.551325000, "NGI1NzkwOQ=="),
    (1741231902.551541000, "fQ=="),
]

flag = "".join(base64.b64decode(chunk).decode() for _, chunk in sorted(rows))
print(flag)
```

## Why This Works

The attacker hid data inside the payloads of TCP SYN packets and relied on the fact that the PCAP was not stored in chronological order.  
Anyone reading the packets top-to-bottom would get misleading results.  
Sorting by timestamp reveals the correct sequence of Base64-encoded chunks.

## Flag

```text
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_d4b57909}
```
