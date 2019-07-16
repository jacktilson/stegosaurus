import argparse, os, numpy, cv2, bitarray
from itertools import product, islice

def encode(img: numpy.ndarray, bits: int, data: bitarray.bitarray):

    # calculate some things
    bitdepth = img.dtype.itemsize * 8  # no. of bits in each channel

    # no. of available bits (LSB per channel * width * height * channels) - header bit size
    available = bits * (numpy.product(img.shape)) - (40 * 8)

    assert data.length() < available, "Image not big enough for data, either increase image size or bits."
    assert bitdepth > bits, "Image bit depth not big enough for encoding with that many LSBs"

    datasize = bitarray.bits2bytes(data.length())  # size of the actual data in bytes
    mask = ((2**bitdepth) - 1) - (2**(bits-1))  # bitmask to erase LSBs on pixels
    height, width, depth = img.shape
    indexes = product(range(width), range(height), range(depth))  # all indexes in the image

    # header: 8 bits (UINT_8): number of lsbs. 32 bits (UINT_32): number bytes encoded)

    header = bitarray.bitarray(endian="little")
    header.frombytes(bits.to_bytes(1, byteorder="little"))
    header.frombytes(datasize.to_bytes(4, byteorder="little"))

    # write header
    writedata(img, islice(indexes, 40), (2**bitdepth) - 2, (header[i:i+1] for i in range(header.length())))

    # write data
    writedata(img, indexes, mask, (data[i:i+bits] for i in range(0, data.length(), bits)))

    return img


def writedata(img, indexes, mask, data):
    for (x, y, c), d in zip(indexes, data):
        colour = img.item(x, y, c)
        encoded = (colour & mask) | int.from_bytes(d.tobytes(), byteorder="little")
        print(f"Pixel@({x},{y})(c{c}) Data: {d.to01()}, Colour: {colour}, Encoded: {encoded}")
        img.itemset(x, y, c, encoded)


def cmd_encode(args):
    assert os.path.isfile(args.imgfile), "Input file doesn't exist"
    img = cv2.imread(args.imgfile)
    data = bitarray.bitarray(endian="little")
    data.frombytes(bytes(args.message, "utf-8"))
    cv2.imwrite(args.outfile, encode(img, args.bits, data))


def cmd_decode(args):
    assert os.path.isfile(args.imgfile), "Input file doesnt exist"


if __name__ == "__main__":

    # Create CLI arg parser
    parser = argparse.ArgumentParser(description="Utility for LSB encoding of a message in an image")

    # Sub-parser for encode/decode
    subs = parser.add_subparsers(title="Actions")

    # Parser for encode cmd
    encodeParser = subs.add_parser("encode", description="Encode a message in an image file")
    encodeParser.add_argument("-imgfile", required=True, action="store", type=str, help="Image file to encode")
    encodeParser.add_argument("-message", required=True, action="store", type=str, help="Message to hide")
    encodeParser.add_argument("-outfile", required=True, action="store", type=str, help="Outfile name.")
    encodeParser.add_argument("-bits", action="store", type=int, default=1, help="Number of bits to encode")
    encodeParser.set_defaults(func=cmd_encode)

    # Parser for decode command
    decodeParser = subs.add_parser("decode", description="Decode a message stored in an image file")
    decodeParser.add_argument("-imgfile", required=True, action="store", help="Image file to extract data from")
    decodeParser.set_defaults(func=cmd_decode)

    args = parser.parse_args()
    args.func(args)
