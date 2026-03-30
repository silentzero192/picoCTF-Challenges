# shark1.pcapng Writeup

## Challenge

**Category:** Forensics  
**Artifact:** `shark1.pcapng`  
**Flag format:** `picoCTF{...}`

## Final Flag

```text
picoCTF{p33kab00_1_s33_u_deadbeef}
```

## TL;DR

Most of the capture is noisy internal traffic:

- WinRM / HTTP on port `5985`
- TLS traffic to `192.168.38.105:8412` with SNI `kolide`
- a request to the AWS metadata endpoint

The actual flag is much simpler than the rest of the capture suggests.

A browser on `192.168.38.104` makes a plain HTTP request to `18.222.37.134`:

```text
GET /
```

The HTTP response body contains:

```text
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

That text is ROT13. Decoding it gives:

```text
The flag is picoCTF{p33kab00_1_s33_u_deadbeef}
```

## Initial Recon

Start by identifying the file and getting a quick overview:

```bash
file shark1.pcapng
capinfos shark1.pcapng
```

Useful output:

```text
shark1.pcapng: pcapng capture file - version 1.0
Number of packets: 987
Capture duration: 23.259682 seconds
```

This is a fairly short capture with a lot of data packed into a small time window.

## Protocol Breakdown

To understand where to focus:

```bash
tshark -r shark1.pcapng -q -z io,phs
```

Relevant output:

```text
tcp                                  frames:985
  http                               frames:288
  tls                                frames:43
arp                                    frames:2
```

So the capture is almost entirely TCP, with both HTTP and TLS present.

## Conversation Analysis

Next, look at the TCP conversations:

```bash
tshark -r shark1.pcapng -q -z conv,tcp
```

The interesting conversations are:

- `192.168.38.104 <-> 192.168.38.103:5985`
- `192.168.38.104 <-> 192.168.38.105:8412`
- `192.168.38.105:9000 <-> 192.168.38.104`
- `192.168.38.104 <-> 18.222.37.134:80`
- `192.168.38.104 <-> 169.254.169.254:80`

At first glance, the big internal WinRM conversation on `5985` looks like the likely source of the flag because it dominates the capture.

However:

- the WinRM traffic is `multipart/encrypted`
- the `8412` traffic is TLS
- the metadata service request is tiny and returns only `none`

That leaves the plain HTTP conversation to `18.222.37.134` as the best plaintext candidate.

## Enumerating HTTP Requests

List the HTTP requests:

```bash
tshark -r shark1.pcapng -Y http.request \
  -T fields \
  -e frame.number -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport \
  -e http.request.method -e http.host -e http.request.uri
```

Important entries:

```text
823  192.168.38.104 -> 18.222.37.134:80        GET  /
962  192.168.38.104 -> 169.254.169.254:80      GET  /latest/meta-data/instance-action
```

The AWS metadata request is not useful here because its response is just:

```text
none
```

So the external HTTP request is the one to inspect.

## Following the Suspicious HTTP Stream

The request to `18.222.37.134` is on TCP stream `5`.

Follow it directly:

```bash
tshark -r shark1.pcapng -q -z follow,tcp,ascii,5
```

This reveals the full exchange:

```text
GET / HTTP/1.1
Host: 18.222.37.134
...

HTTP/1.1 200 OK
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 47
Content-Type: text/html

Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

That response body is clearly not random data. It looks like meaningful text that has been obfuscated.

## Extracting the HTTP Object

Another clean way to recover the same content is to export HTTP objects:

```bash
mkdir -p /tmp/shark1_http
tshark -r shark1.pcapng --export-objects http,/tmp/shark1_http
ls -lah /tmp/shark1_http
```

Among the extracted files is:

```text
/tmp/shark1_http/%2f
```

Reading that file gives:

```text
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

This matches the body of the external HTTP response.

## Identifying the Encoding

The string starts with:

```text
Gur synt vf ...
```

That is a classic ROT13 pattern:

- `Gur` -> `The`
- `synt` -> `flag`
- `vf` -> `is`

So decode the whole body with ROT13.

## Decoding the Body

Minimal Python example:

```python
import codecs

s = "Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}"
print(codecs.decode(s, "rot_13"))
```

Output:

```text
The flag is picoCTF{p33kab00_1_s33_u_deadbeef}
```

From that sentence, the flag is:

```text
picoCTF{p33kab00_1_s33_u_deadbeef}
```

## Reproduction Commands

You can solve the challenge with a short chain of commands:

### 1. Find the plain HTTP request

```bash
tshark -r shark1.pcapng -Y http.request \
  -T fields -e frame.number -e http.host -e http.request.uri
```

### 2. Follow the external HTTP stream

```bash
tshark -r shark1.pcapng -q -z follow,tcp,ascii,5
```

### 3. Decode the response body with ROT13

```bash
python3 - <<'PY'
import codecs
s = "Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}"
print(codecs.decode(s, "rot_13"))
PY
```

## Why the Other Traffic Is Noise

The capture tries to pull attention toward heavier internal traffic:

- WinRM on `5985` looks important but is encrypted
- TLS to `8412` looks suspicious but is not necessary to solve the challenge
- the AWS metadata request is a small red herring

The real solve path is much simpler:

1. find the external plaintext HTTP request
2. inspect the response body
3. recognize ROT13
4. decode the flag

## Useful Indicators

These specific artifacts were the key:

- Frame `823`: `GET / HTTP/1.1`
- Frame `827`: HTTP `200 OK` with the obfuscated body
- Response body:

```text
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

- ROT13 decoded text:

```text
The flag is picoCTF{p33kab00_1_s33_u_deadbeef}
```

## Final Answer

```text
picoCTF{p33kab00_1_s33_u_deadbeef}
```
