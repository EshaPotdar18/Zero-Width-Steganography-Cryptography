# !pip install pillow

from PIL import Image
import numpy as np
from google.colab import files
from io import BytesIO

# Function to encode text into an image
def encode_text_into_image(image, text):
    def text_to_bin(text):
        return ''.join(format(ord(i), '08b') for i in text)

    def modify_pixel(pixel, bit):
        return (pixel & ~1) | bit

    data = text_to_bin(text) + '00000000'  # Append a null byte to indicate end of message
    data_len = len(data)
    
    img = np.array(image)
    flat_img = img.flatten()
    for i in range(data_len):
        bit = int(data[i])
        flat_img[i] = modify_pixel(flat_img[i], bit)
    
    img = Image.fromarray(flat_img.reshape(img.shape))
    return img

# Function to decode text from an image
def decode_text_from_image(image):
    def pixel_to_bin(pixel):
        return str(pixel & 1)

    img = np.array(image)
    flat_img = img.flatten()
    bin_data = ''.join(pixel_to_bin(pixel) for pixel in flat_img)
    
    # Convert binary data to text
    text = ''
    for i in range(0, len(bin_data), 8):
        byte = bin_data[i:i+8]
        if byte == '00000000':
            break
        text += chr(int(byte, 2))
    
    return text

# Upload image and encode text
uploaded = files.upload()
image_file = next(iter(uploaded.keys()))
image = Image.open(image_file)

# Encode a message into the image
message = "Hello, World!"
encoded_image = encode_text_into_image(image, message)
encoded_image.save('/content/encoded_image.png')
files.download('/content/encoded_image.png')

# Upload the encoded image to decode the message
uploaded_encoded = files.upload()
encoded_image_file = next(iter(uploaded_encoded.keys()))
encoded_image = Image.open(encoded_image_file)

# Decode the message from the encoded image
decoded_message = decode_text_from_image(encoded_image)
print(f"Decoded message: {decoded_message}")
