import os, numpy, cv2, bitarray
from itertools import product, islice
from typing import Iterable, Tuple

LSB = 1
EXT = 2
NAME = 4


##################
# util functions #
##################


def read_img(img_filepath: str) -> numpy.ndarray:
    assert os.path.isfile(img_filepath), "Not a valid path"
    assert img_filepath.split(".")[-1].lower() in ["bmp"], "Not an accepted file extension"
    return cv2.imread(img_filepath)


def read_img_binary(bin_img: bytes) -> numpy.ndarray:
    return cv2.imdecode(bin_img, flags=cv2.IMREAD_ANYDEPTH)


def write_img(img_filepath: str, img: numpy.ndarray):
    cv2.imwrite(img_filepath, img)


def string_to_bitarray(text: str) -> bitarray.bitarray:
    return bytes_to_bitarray(bytes(text, "utf-8"))


def bytes_to_bitarray(data: bytes) -> bitarray.bitarray:
    bits = bitarray.bitarray(endian="little")
    bits.frombytes(data)
    return bits


##################
# main functions #
##################

def encode(img: numpy.ndarray, data: bytes, **flags) -> numpy.ndarray:
    """
    Encodes binary data and header onto the least significant bits of colour channels in an image.
    :param img: The image in numpy array format.
    :param n_lsb: The number of bits to overwrite in each image channel.
    :param data: The binary data to encode within the image.
    :return:
    """
    bit_data = bytes_to_bitarray(data)

    flagbyte = 0
    if "n_lsb" in flags:
        flagbyte |= LSB
    if "extension" in flags:
        flagbyte |= EXT
    if "filename" in flags:
        flagbyte |= NAME

    n_lsb = flags["n_lsb"] if flagbyte & LSB else 1

    # no. of available bits (LSB per channel * width * height * channels)
    bits_available = n_lsb * (numpy.product(img.shape))

    if bit_data.length() > bits_available - (40 * 8):  # take off header size
        raise ValueError("Image not big enough for data, either increase image size or bits encoded per channel.")

    byte_length = bitarray.bits2bytes(bit_data.length())  # size of the actual data in bytes
    height, width, channels = img.shape  # image dimensions
    indexes = product(range(width), range(height), range(channels))  # iterator of all indexes in the image

    # create header
    # First 8 bits: number of bits being encoded in each channel.
    # Next 32 bits: number bytes of data being encoded)
    header = bitarray.bitarray(endian="little")
    header.frombytes(flagbyte.to_bytes(1, byteorder="little"))
    if flagbyte & LSB:
        header.frombytes(n_lsb.to_bytes(1, byteorder="little"))

    # write header to image
    write_to_img(img, islice(indexes, header.length()), 1, header)

    subheader = bitarray.bitarray(endian="little")
    if flagbyte & EXT:
        ext = bytes(flags["extension"], "utf-8")
        subheader.frombytes(len(ext).to_bytes(1, byteorder="little"))
        subheader.frombytes(ext)

    if flagbyte & NAME:
        name = bytes(flags["filename"], "utf-8")
        subheader.frombytes(len(name).to_bytes(1, byteorder="little"))
        subheader.frombytes(name)

    subheader.frombytes(byte_length.to_bytes(4, byteorder="little"))

    # write header to image
    write_to_img(img, islice(indexes, subheader.length() // n_lsb), n_lsb, subheader)

    # write data to image
    write_to_img(img, indexes, n_lsb, bit_data)

    return img


def write_to_img(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: bitarray.bitarray):
    """
    Writes chunked bits of data to the least significant bit of an image.
    :param img: Numpy Array of image data.
    :param indexes: Indexes and ordering of pixel locations in the image to write the data to.
    :param n_lsb: The number of bits in the image to be overwritten in each channel
    :param chunked_data: Smaller bitarrays of length n_lsb or less to be written directly to the image channels.
    """

    chunked_data = (data[i:i + n_lsb] for i in range(0, data.length(), n_lsb))

    # bit depth of the image (number of bits in each pixel channel
    bit_depth = img.dtype.itemsize * 8

    # check each channel has enough bit depth to accommodate using that many bits to encode with.
    if bit_depth < n_lsb:
        raise ValueError("Image bit depth not big enough for encoding with that many bits per channel")

    # calculate the bit mask to erase least significant bits on each pixel channel so they can be overwritten.
    mask = ((2 ** bit_depth) - 1) - ((2 ** (n_lsb)) - 1)  # e.g. 10111010 AND 11111100 (mask) = 10111000

    for (x, y, c), d in zip(indexes, chunked_data):
        colour = img.item(x, y, c)
        encoded = (colour & mask) | int.from_bytes(d.tobytes(), byteorder="little")
        print(f"Pixel@({x},{y})(c{c}) Data: {d.to01()}, Colour: {colour}, Encoded: {encoded}")
        img.itemset(x, y, c, encoded)


def decode_img(img: numpy.ndarray) -> bytes:
    """
    Decodes data stored in an image.
    :param img: The image data has been stored in.
    :return: The data stored in thhe image.
    """
    height, width, channels = img.shape  # image dimensions
    indexes = product(range(width), range(height), range(channels))  # iterator of all indexes in the image

    # read header data
    flags = int.from_bytes(read_from_img(img, islice(indexes, 8), 1), byteorder="little")
    print(flags)
    n_lsb = 1
    if flags & LSB:
        n_lsb = int.from_bytes(read_from_img(img, islice(indexes, 8), 1), byteorder="little")
        print("LSB =", n_lsb),

    if flags & EXT:
        ext_len = int.from_bytes(read_from_img(img, islice(indexes, 8), n_lsb), byteorder="little")
        print(ext_len)

    # read actual data
    data = read_from_img(img, islice(indexes, (byte_size * 8) // n_lsb), n_lsb)
    return data.tobytes()


def read_from_img(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int) -> bitarray:
    """
    Reads the least significant bits of image channels and returns them as a continuous bitarray
    :param img: The image to extract from.
    :param indexes: The indexes of channels in the image to extract from.
    :param n_lsb: The number of bits to extract from each channel
    :return: Continuous bitarray of extracted bits
    """
    data = bitarray.bitarray(endian="little")
    bytes_size = bitarray.bits2bytes(n_lsb)

    # bit depth of the image (number of bits in each pixel channel
    bit_depth = img.dtype.itemsize * 8

    # check each channel has enough bit depth to accommodate using that many bits to encode with.
    if bit_depth < n_lsb:
        raise ValueError("Image bit depth not big enough for decoding that many bits per channel")

    # calculate the bit mask to get only the least significant bits on each pixel channel..
    mask = ((2 ** n_lsb) - 1)  # e.g. 10111010 AND 00000011 (mask) = 00000010

    for (x, y, c) in indexes:
        chunk = bitarray.bitarray(endian="little")
        chunk.frombytes((img.item(x, y, c) & mask).to_bytes(bytes_size, byteorder="little"))
        data += chunk[:n_lsb]

    return data
