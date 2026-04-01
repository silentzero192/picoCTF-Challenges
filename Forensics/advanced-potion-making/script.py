from PIL import Image

img = Image.open('fixed-potion.png')
pixels = img.load()
width, height = img.size

# Create a new image to store the result
new_img = Image.new('RGB', (width, height))
new_pixels = new_img.load()

for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        # Check the least significant bit of the red channel
        # If the LSB is 1, make the pixel white; otherwise, black.
        val = 255 if (r & 1) else 0
        new_pixels[x, y] = (val, val, val)

new_img.save('recovered_flag.png')
