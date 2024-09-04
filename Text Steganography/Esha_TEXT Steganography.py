# Function to encode the secret message using zero-width characters
def encode_text(secret_message):
    # Convert the secret message to binary
    secret_binary = ''.join(format(ord(char), '08b') for char in secret_message)

    # Use zero-width characters to encode the binary message
    encoded_text = ''
    for bit in secret_binary:
        if bit == '0':
            encoded_text += '\u200B'  # Zero-width space
        elif bit == '1':
            encoded_text += '\u200C'  # Zero-width non-joiner
    return encoded_text

# Function to decode the secret message from the encoded text
def decode_text(encoded_text):
    # Convert the zero-width characters to binary
    binary_message = ''
    for char in encoded_text:
        if char == '\u200B':
            binary_message += '0'
        elif char == '\u200C':
            binary_message += '1'

    # Convert the binary message to text
    decoded_message = ''
    for i in range(0, len(binary_message), 8):
        decoded_message += chr(int(binary_message[i:i+8], 2))
    return decoded_message

# Read the text file
file_path = "your_file.txt"  # Update with the path to your text file
with open(file_path, 'r') as file:
    original_text = file.read()

# Encode the text from the file
encoded_message = encode_text(original_text)

# Save the encoded text to a new file
encoded_file_path = "encoded_your_file.txt"  # Update with the desired path for the encoded file
with open(encoded_file_path, 'w') as file:
    file.write(encoded_message)

print("Text encoded successfully.")

# Decode the encoded message
decoded_message = decode_text(encoded_message)