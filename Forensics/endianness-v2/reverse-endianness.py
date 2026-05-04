with open('challengefile', 'rb') as f_in:
    with open('fixed_file', 'wb') as f_out:
        while True:
            chunk = f_in.read(4)
            if not chunk:
                break
            # Pad with null bytes if the file size isn't a multiple of 4
            if len(chunk) < 4:
                chunk = chunk.ljust(4, b'\x00')
            # Reverse the 4-byte chunk
            f_out.write(chunk[::-1])
