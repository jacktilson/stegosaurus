import os, numpy, cv2, bitarray, pathlib
from itertools import product, islice
from typing import Iterable, Tuple, Dict
from math import floor


# Magic flag numbers
LSB = 1
EXT = 2
NAME = 4

##################
# util functions #
##################


def read_img(img_filepath: str) -> numpy.ndarray:
    # raise error if bad filepath is given
    if not os.path.isfile(img_filepath): raise ValueError(f"File path given is not valid. ({img_filepath})")

    # raise error if unsupported filetype
    extension = pathlib.Path(img_filepath).suffix[1:].lower() #get the file extension of the file
    if not extension in ("bmp", "png"): raise(ValueError(f"Extension '{extension}' is not an a supported type'"))

    # try and read the image
    img = cv2.imread(img_filepath, flags=cv2.IMREAD_UNCHANGED)

    # raise error if image could not be read
    if img is None: raise(ValueError(f"The data could not be read. Is it an image? ({img_filepath})"))

    return img


def read_img_binary(bin_img: bytes) -> numpy.ndarray:

    # try and read the image
    img = cv2.imdecode(bin_img, flags=cv2.IMREAD_UNCHANGED)

    # raise error if image could not be read
    if img is None: raise(ValueError(f"The data could not be read. Is it an image?"))

    return img

def write_img(img_filepath: str, img: numpy.ndarray):
    cv2.imwrite(img_filepath, img)

def string_to_bitarray(text: str) -> bitarray.bitarray:
    return bytes_to_bitarray(bytes(text, "utf-8"))


def bytes_to_bitarray(data: bytes) -> bitarray.bitarray:
    bits = bitarray.bitarray(endian="little")
    bits.frombytes(data)
    return bits

def get_img_meta(img: numpy.ndarray) -> Tuple:
    return (*img.shape, img.dtype.itemsize * 8) if len(img.shape) == 3 else (*img.shape, 1, img.dtype.itemsize)

def space_available(img: numpy.ndarray, **flags) -> int:
    width, height, channels, bitdepth = get_img_meta(img)

    header_size = 8 # encoded at 1LSB. Measured in bits. 8 initialy because of the flag byte
    subheader_size = 32 # Measured in bits. Everything encoded at n_lsb
    n_lsb = flags["n_lsb"] if "n_lsb" in flags else 1
    if n_lsb > 1:
        header_size += 8

    if "extension" in flags:
        subheader_size += 8 + (len(bytes(flags["extension"], "utf-8")) * 8)
    if "filename" in flags:
        subheader_size += 8 + (len(bytes(flags["filename"], "utf-8")) * 8)
    
    indexes = width * height * channels

    # Return in bytes.
    return ((indexes - header_size - ciel_div(subheader_size, n_lsb)) * n_lsb) // 8

def ciel_div(a: int, b: int):
    return -(-a//b)
    

##################
# main functions #
##################


'''
Typical Flags Object:
{
    filename,
    filextension,
    n_lsb
}

'''

def encode(img: numpy.ndarray, data: bytes, **flags) -> numpy.ndarray:
    """
    Encodes binary data and header onto the least significant bits of colour channels in an image.
    :param img: The image in numpy array format.
    :param data: The binary data to encode within the image.
    :return:
    """

    # construct the flag byte that comes at the first part of the file.
    flagbyte = 0
    if "n_lsb" in flags and flags["n_lsb"] > 1:
        flagbyte |= LSB
    if "extension" in flags:
        flagbyte |= EXT
    if "filename" in flags:
        flagbyte |= NAME

    n_lsb = flags["n_lsb"] if flagbyte & LSB else 1

    if len(data) * 8 > space_available(img, **flags):
        raise ValueError("Image not big enough for data, either increase image size or bits encoded per channel.")

    # image dimensions
    width, height, channels, bit_depth = get_img_meta(img)
    # iterator of all indexes in the image
    indexes = product(range(width), range(height), range(channels)) if channels > 1 else product(range(width), range(height))

    # write flagbyte to image
    write_int(img, indexes, 1, flagbyte, 1)

    if flagbyte & LSB: write_int(img, indexes, n_lsb=1, data=n_lsb, byte_length=1)
    if flagbyte & EXT: write_data_frame(img, indexes, n_lsb, bytes(flags["extension"], "utf-8"))
    if flagbyte & NAME: write_data_frame(img, indexes, n_lsb, bytes(flags["filename"], "utf-8"))

    # write actual data frame
    write_data_frame(img, indexes, n_lsb, data, size_byte_length=4)

    return img

def write_data_frame(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: bytes, size_byte_length: int=1):
    """
    Writes a frame of data to the image. First encodes the length and then encodes the data onto the image.
    :param img: The image in numpy array format.
    :param indexes: The indexes to write at. Indexes are removed as they are used.
    :param n_lsb: The number of bits to write over at each index. Directly affects the number of indexes used.
    :param size_byte_length: The number of bytes used to write the length of the data.
    """
    write_int(img, indexes, n_lsb=n_lsb, data=len(data), byte_length=size_byte_length)
    write_bytes(img, indexes, n_lsb=n_lsb, data=data)

def write_int(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: int, byte_length: int):
    write_bits(
        img,
        islice(indexes, ciel_div(byte_length * 8, n_lsb)),
        n_lsb,
        bytes_to_bitarray(data.to_bytes(byte_length, byteorder="little")))

def write_bytes(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: bytes):
    write_bits(
        img,
        islice(indexes, ciel_div(len(data) * 8, n_lsb)),
        n_lsb,
        bytes_to_bitarray(data))

def write_bits(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: bitarray.bitarray):
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

    for index, d in zip(indexes, chunked_data):
        colour = img.item(*index)
        encoded = (colour & mask) | int.from_bytes(d.tobytes(), byteorder="little")
        img.itemset(*index, encoded)


def decode_img(img: numpy.ndarray) -> Tuple[bytes, Dict[str, str]]:
    """
    Decodes data stored in an image.
    :param img: The image data has been stored in.
    :return: The data stored in the image.
    """
    width, height, channels = img.shape  # image dimensions
    indexes = product(range(width), range(height), range(channels))  # iterator of all indexes in the image

    meta = dict()  # meta object to store header data

    # read header data
    flags = int.from_bytes(read_from_img(img, islice(indexes, 8), 1, 8).tobytes(), byteorder="little")
    n_lsb = 1
    if flags & LSB:
        n_lsb = int.from_bytes(read_from_img(img, islice(indexes, 8), 1, 8).tobytes(), byteorder="little")

    if flags & EXT:
        ext_len = int.from_bytes(read_from_img(img, islice(indexes, -(-8 // n_lsb)), n_lsb, 8).tobytes(), byteorder="little") * 8 # extension length in bits
        print(ext_len)
        ext = (read_from_img(img, islice(indexes, -(-ext_len // n_lsb)), n_lsb, ext_len).tobytes()).decode("utf-8")
        meta["extension"] = ext

    if flags & NAME:
        name_len = int.from_bytes(read_from_img(img, islice(indexes, 8 // n_lsb), n_lsb, 8).tobytes(), byteorder="little") * 8 # name lenth in bits
        name = (read_from_img(img, islice(indexes, -(-name_len // n_lsb)), n_lsb, name_len).tobytes()).decode("utf-8")
        meta["filename"] = name

    data_len = int.from_bytes(read_from_img(img, islice(indexes, -(-32 // n_lsb)), n_lsb, 32).tobytes(), byteorder="little") * 8 # data length in bits
    data = read_from_img(img, islice(indexes, -(-data_len // n_lsb)), n_lsb, data_len).tobytes()

    return data, meta


def read_from_img(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, bits: int) -> bitarray:
    """
    Reads the least significant bits of image channels and returns them as a continuous bitarray
    :param img: The image to extract from.
    :param indexes: The indexes of channels in the image to extract from.
    :param n_lsb: The number of bits to extract from each channel
    :param bits: The number of bits to extract in total.
    :return: Continuous bitarray of extracted bits
    """
    data = bitarray.bitarray(endian="little")
    bytes_size = ciel_div(n_lsb, 8)

    # bit depth of the image (number of bits in each pixel channel
    bit_depth = get_img_meta(img)[3]

    # check each channel has enough bit depth to accommodate using that many bits to encode with.
    if bit_depth < n_lsb:
        raise ValueError("Image bit depth not big enough for decoding that many bits per channel")

    # calculate the bit mask to get only the least significant bits on each pixel channel..
    mask = ((2 ** n_lsb) - 1)  # e.g. 10111010 AND 00000011 (mask) = 00000010
    
    # total bits extracted so far
    total = 0
    
    for (x, y, c) in indexes:
        chunk = bitarray.bitarray(endian="little")
        chunk.frombytes((img.item(x, y, c) & mask).to_bytes(bytes_size, byteorder="little"))
        data += chunk[:(n_lsb if total + n_lsb <= bits else bits - total)]
        total += n_lsb
    return data
