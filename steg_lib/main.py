import argparse
import pathlib
import steg
import base64


def cmd_encode_string(args):
    img = steg.read_img(args.imgfile)
    steg.write_img(args.outfile, steg.encode(img, bytes(args.msg, "utf-8"), n_lsb=args.n_lsb, extension="txt"))


def cmd_encode_file(args):
    img = steg.read_img(args.imgfile)
    path = pathlib.Path(args.encfile)

    with open(args.encfile, "rb") as file:
        data = file.read()

    flags = dict()
    if args.n_lsb > 0:
        flags["n_lsb"] = args.n_lsb
    if args.enc_filename:
        flags["filename"] = path.stem
    if args.enc_extension:
        flags["extension"] = path.suffix[1:]
    if args.encrypt:
        flags["encrypt"] = base64.b64encode(str.encode(args.encrypt))

    steg.write_img(args.outfile, steg.encode(img, data, **flags))


def cmd_decode(args):
    img = steg.read_img(args.imgfile)
    data, meta = steg.decode_img(img, base64.b64encode(str.encode(args.encrypt)))
    filename = meta["filename"] if "filename" in meta else "output"
    ext = f".{meta['extension']}" if "extension" in meta else ""
    with open(f"{args.o}{filename}{ext}", "wb+") as file:
        file.write(data)


if __name__ == "__main__":
    # Create CLI arg parser
    parser = argparse.ArgumentParser(description="Utility for LSB encoding of a message in an image")

    # Sub-parser for encode/decode
    subs = parser.add_subparsers(title="Actions")

    # Parser for encode string cmd
    string_encode_parser = subs.add_parser("encode_string", description="Encode a message in an image file")
    string_encode_parser.add_argument("imgfile", action="store", type=str, help="Image file to encode")
    string_encode_parser.add_argument("outfile", action="store", type=str, help="Outfile name.")
    string_encode_parser.add_argument("msg", action="store", type=str, help="Message to hide")
    string_encode_parser.add_argument("-n_lsb", action="store", type=int, default=1,
                                      help="Number of bits to encode on each channel")
    string_encode_parser.set_defaults(func=cmd_encode_string)

    # Parser for encode file cmd
    file_encode_parser = subs.add_parser("encode_file", )
    file_encode_parser.add_argument("imgfile", action="store", type=str, help="Image file to encode")
    file_encode_parser.add_argument("outfile", action="store", type=str, help="Output file name.")
    file_encode_parser.add_argument("encfile", action="store", type=str, help="File to hide in img")
    file_encode_parser.add_argument("-n_lsb", action="store", type=int, default=1,
                                    help="Number of bits to encode on each channel")
    file_encode_parser.add_argument("-enc_extension", action="store_true", help="Encode the extension in the image.")
    file_encode_parser.add_argument("-enc_filename", action="store_true", help="Encode the filename in the image.")
    file_encode_parser.add_argument("-encrypt", action="store", type=str, help="Encrypt the data")
    file_encode_parser.set_defaults(func=cmd_encode_file)

    # Parser for decode command
    decode_parser = subs.add_parser("decode", description="Decode a message stored in an image file.")
    decode_parser.add_argument("imgfile", action="store", type=str, help="Image to decode")
    decode_parser.add_argument("-o", action="store", type=str, default="./Decoded/",
                               help="Optional output directory")
    decode_parser.add_argument("-encrypt", action="store", type=str, help="Encrypt the data")
    decode_parser.set_defaults(func=cmd_decode)

    args = parser.parse_args()
    args.func(args)
