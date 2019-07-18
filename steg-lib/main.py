import argparse
import steg


def cmd_encode_string(args):
    img = steg.read_img(args.imgfile)
    steg.write_img(args.outfile, steg.encode(img, args.n_bits, bytes(args.msg, "utf-8")))

def cmd_encode_file(args):
    img = steg.read_img(args.imgfile)

    with open(args.encfile, "rb") as file:
        data = file.read()

    steg.write_img(args.outfile, steg.encode(img, args.n_bits, data))


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

    # Parser for encode string cmd
    string_encode_parser = subs.add_parser("encode_string", description="Encode a message in an image file")
    string_encode_parser.add_argument("imgfile", action="store", type=str, help="Image file to encode")
    string_encode_parser.add_argument("outfile", action="store", type=str, help="Outfile name.")
    string_encode_parser.add_argument("msg", action="store", type=str, help="Message to hide")
    string_encode_parser.add_argument("-n_bits", action="store", type=int, default=1,
                                      help="Number of bits to encode on each channel")
    string_encode_parser.set_defaults(func=cmd_encode_string)

    # Parser for encode file cmd
    file_encode_parser = subs.add_parser("encode_file", )
    file_encode_parser.add_argument("imgfile", action="store", type=str, help="Image file to encode")
    file_encode_parser.add_argument("outfile", action="store", type=str, help="Outfile name.")
    file_encode_parser.add_argument("encfile", action="store", type=str, help="File to hide in img")
    file_encode_parser.add_argument("-n_bits", action="store", type=int, default=1,
                                    help="Number of bits to encode on each channel")
    file_encode_parser.set_defaults(func=cmd_encode_file)

    # Parser for decode command
    decode_parser = subs.add_parser("decode", description="Decode a message stored in an image file")
    decode_parser.add_argument("imgfile", action="store", type=str, help="Image file to extract from")
    decode_parser.add_argument("outfile", action="store", type=str, help="File to write extracted data to")
    decode_parser.set_defaults(func=cmd_decode)

    args = parser.parse_args()
    args.func(args)
