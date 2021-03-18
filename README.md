# Basic Image Encryptor Using Bitwise Operations

## Requirements

* Python 3.8+
* OpenCV2 for Python installed.
* Numpy installed.

---

## Bad Description and Demo

Encrypts an image by generating a random byte key then XORing it with an input image. Can do AND and OR operations for demonstration purposes.

Example usage using the files in [example_files](example_files/).

```
# Encrypts the image using XOR, AND and OR operations using random bytes
python3 image_crypto.py -A alan-turing.png

# Decrypts the XOR image to get the original image again.
python3 image_crypto.py -o decrypted -k image.key out-xor.png
```

**Only use lossless image compression formats such as .png**
