import argparse
import steg


def cmd_encode(args):
    img = steg.read_img(args.imgfile)
    steg.write_img(args.outfile, steg.encode(img, args.n_bits, bytes(args.msg, "utf-8")))


def cmd_decode(args):
    img = steg.read_img(args.imgfile)
    data = steg.decode_img(img)
    with open(args.outfile, "wb+") as file:
        file.write(data)


if __name__ == "__main__":
    # Create CLI arg parser
    parser = argparse.ArgumentParser(description="Utility for LSB encoding of a message in an image")

    # Sub-parser for encode/decode
    subs = parser.add_subparsers(title="Actions")

    # Parser for encode cmd
    encodeParser = subs.add_parser("encode", description="Encode a message in an image file")
    encodeParser.add_argument("imgfile", action="store", type=str, help="Image file to encode")
    encodeParser.add_argument("msg", action="store", type=str, help="Message to hide")
    encodeParser.add_argument("outfile", action="store", type=str, help="Outfile name.")
    encodeParser.add_argument("n_bits", action="store", type=int, default=1, help="Number of bits to encode")
    encodeParser.set_defaults(func=cmd_encode)

    # Parser for decode command
    decodeParser = subs.add_parser("decode", description="Decode a message stored in an image file")
    decodeParser.add_argument("imgfile", action="store", type=str, help="Image file to extract from")
    decodeParser.add_argument("outfile", action="store", type=str, help="File to write data to")
    decodeParser.set_defaults(func=cmd_decode)

    args = parser.parse_args()
    args.func(args)
