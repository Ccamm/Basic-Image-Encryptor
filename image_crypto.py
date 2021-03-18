import cv2, argparse, os, base64
import numpy as np
# from Crypto.Util.number import bytes_to_long

OUTPUT_FORMAT = "{prefix}-{type}{ext}"

def parse_args():
    parser = argparse.ArgumentParser(description="Very basic image encryptor that generates a list of random bytes and performs XOR on an input image")

    parser.add_argument(
        'image',
        help="image to encrypt/decrypt",
        type=str
    )

    parser.add_argument(
        "-k", "--key_file",
        help="the key file to use for encrypting/decrypting the image",
        type=str
    )

    parser.add_argument(
        "-d", "--dump_key_file",
        help="file to dump the randomly generated key to",
        default="image.key"
    )

    parser.add_argument(
        "-A", "--all_modes",
        help="if set will output the AND and OR along with the XOR when encrypting an image",
        action="store_true"
    )

    parser.add_argument(
        "-o", "--output_prefix",
        help="prefix of output files",
        type=str,
        default="out"
    )

    return parser.parse_args()

def generate_key(image_shape):
    byte_count = 1
    for x in image_shape:
        byte_count *= x
    return os.urandom(byte_count)

def parse_key_to_np_array(key_bytes, image_shape):
    key_array = np.array([x for x in key_bytes], dtype=int)
    return np.reshape(key_array, image_shape)


def main(args):
    input_image_name = args.image
    _name, image_ext = os.path.splitext(input_image_name)

    try:
        input_image_data = cv2.imread(input_image_name, -1)
    except Exception as e:
        print(e)

    image_shape = input_image_data.shape

    if args.key_file:
        with open(args.key_file, "r") as f:
            key = base64.b64decode(f.read())
    else:
        key = generate_key(image_shape)

    key_array = parse_key_to_np_array(key, image_shape)

    xored_data = input_image_data ^ key_array

    cv2.imwrite(
        OUTPUT_FORMAT.format(
            prefix=args.output_prefix,
            type="xor",
            ext=image_ext
        ),
        xored_data
    )

    if args.all_modes:
        and_data = input_image_data & key_array
        or_data = input_image_data | key_array

        cv2.imwrite(
            OUTPUT_FORMAT.format(
                prefix=args.output_prefix,
                type="and",
                ext=image_ext
            ),
            and_data
        )

        cv2.imwrite(
            OUTPUT_FORMAT.format(
                prefix=args.output_prefix,
                type="or",
                ext=image_ext
            ),
            or_data
        )

    with open(args.dump_key_file, "w") as f:
        f.write(base64.b64encode(key).decode())

if __name__ == "__main__":
    args = parse_args()
    main(args)
