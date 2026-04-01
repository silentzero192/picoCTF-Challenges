# Open the file in binary mode to catch the specific hex values
with open('whitepages.txt', 'rb') as f:
    data = f.read()

# Replace the whitespace patterns with 0 and 1
binary_str = data.replace(b'\xe2\x80\x83', b'0').replace(b'\x20', b'1')

# Convert binary string to ASCII text
# Note: We convert the binary string (bytes object) to an integer first
binary_int = int(binary_str, 2)
# Calculate the number of bytes needed
byte_count = (binary_int.bit_length() + 7) // 8
# Convert to bytes and decode to ASCII
flag_data = binary_int.to_bytes(byte_count, "big").decode('ascii', errors='ignore')

print(flag_data)
