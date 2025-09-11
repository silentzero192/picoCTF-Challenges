import base64
import urllib.parse


def recover_password(expected: str) -> str:
    # Step 1: Base64 decode
    base64_decoded = base64.b64decode(expected).decode()

    # Step 2: URL decode (reverse of urlEncode)
    password = urllib.parse.unquote(base64_decoded)

    return password


if __name__ == "__main__":
    expected = (
        "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"
        "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"
        "JTM0JTVmJTY1JTMzJTMxJTM1JTMyJTYyJTY2JTM0"
    )

    password = recover_password(expected)
    print("Recovered password: picoCTF{" + password + "}")
