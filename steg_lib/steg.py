import os, numpy, cv2, bitarray, pathlib
from itertools import product, islice
from typing import Iterable, Tuple, Dict, NewType


# Magic flag numbers
LSB = 1
EXT = 2
NAME = 4

# Type aliases
ImgIndex = Tuple[int]
Img = NewType("Img", numpy.ndarray)
Bits = NewType("Bits", bitarray.bitarray)

##################
# util functions #
##################


def read_img(img_filepath: str) -> Img:
    """
    Reads an image from a file into the opencv numpy format. (Accepts .bmp and .png)

    :param img_filepath: The filepath of the image to be read
    :type img_filepath: str
    :raises ValueError: When there is an invalid filepath
    :raises ValueError: When there is an invalid extension
    :raises ValueError: When the file is unreadable (garbage)
    :return: Returns the image as a numpy array
    :rtype: Img
    """
    # raise error if bad filepath is given
    if not os.path.isfile(img_filepath): raise ValueError(f"File path given is not valid. ({img_filepath})")

    # raise error if unsupported filetype
    extension = pathlib.Path(img_filepath).suffix[1:].lower() #get the file extension of the file
    if not extension in ("bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp", "pbm", "pgm", "ppm", "sr", "ras", "tiff", "tif"):
      raise ValueError(f"Extension '{extension}' is not an a supported type'")

    # try and read the image
    img = cv2.imread(img_filepath, flags=cv2.IMREAD_UNCHANGED)

    # raise error if image could not be read
    if img is None: raise(ValueError(f"The data could not be read. Is it an image? ({img_filepath})"))

    return img


def read_img_binary(bin_img: bytes) -> Img:
    """
    Reads an image from memory into the opencv numpy array format

    :param bin_img: The encoded bytes of the image to be interpreted
    :type bin_img: bytes
    :raises ValueError: When the bytes are unreadable (garbage)
    :return: Returns the image as a numpy array
    :rtype: Img
    """

    # convert from bytes to numpy buffer required by imdecode
    data = numpy.frombuffer(bin_img, numpy.uint8)
    
    # try and read the image
    img = cv2.imdecode(data, flags=cv2.IMREAD_UNCHANGED)

    # raise error if image could not be read
    if img is None: raise ValueError(f"The data could not be read. Is it an image?")
    return img


def write_img(img_filepath: str, img: Img):
    """
    Writes a opencv numpy array image to the filepath given.
    
    :param img_filepath: The filepath to be written to.
    :type img_filepath: str
    :param img: The image to be written as a numpy array.
    :type img: Img
    """
    cv2.imwrite(img_filepath, img)


def bytes_to_string(data: bytes) -> str:
    """
    Converts a bytes object to a string using utf-8 encoding

    :type data: bytes
    :rtype: str
    """

    return data.decode("utf-8")


def string_to_bitarray(text: str) -> Bits:
    """
    Converts a string to an array of bits (utf-8 encoding)
    
    :type text: str
    :rtype: Bits
    """

    return bytes_to_bitarray(bytes(text, "utf-8"))


def bytes_to_bitarray(data: bytes) -> Bits:
    """
    Converts bytes to an array of bits.
    
    :type data: bytes
    :rtype: Bits
    """

    bits = bitarray.bitarray(endian="little")
    bits.frombytes(data)
    return bits


def get_img_meta(img: Img) -> Tuple:
    """
    Returns the width, height, channels and bitdepth of an image in opencv numpy format
    
    :type img: Img
    :rtype: Tuple
    """

    return (*img.shape, img.dtype.itemsize * 8) if len(img.shape) == 3 else (*img.shape, 1, img.dtype.itemsize * 8)


def space_available(img: Img, **flags) -> int:
    """
    [summary]
    
    :param img: [description]
    :type img: Img
    :raises ValueError: [description]
    :return: [description]
    :rtype: int
    """
    width, height, channels, bitdepth = get_img_meta(img)

    header_size = 8 # encoded at 1LSB. Measured in bits. 8 initi aly because of the flag byte
    subheader_size = 32 # Measured in bits. Everything encoded at n_lsb
    n_lsb = flags["n_lsb"] if "n_lsb" in flags else 1
    if n_lsb > 1: header_size += 8

    if bitdepth < n_lsb:
        raise ValueError("Number of LSB specified greater than bitdepth of image.")

    if "extension" in flags: subheader_size += 8 + (len(bytes(flags["extension"], "utf-8")) * 8)
    if "filename" in flags: subheader_size += 8 + (len(bytes(flags["filename"], "utf-8")) * 8)
    
    indexes = width * height * channels # the number of indexes available

    # Return in bytes. All applications of this function are working in bytes.
    free_indexes = indexes - header_size - ciel_div(subheader_size, n_lsb)
    free_bytes = (free_indexes * n_lsb) // 8
    return max(0, free_bytes)

def ciel_div(a: int, b: int):
    """Returns the cieling integer division of a and b"""
    return -(-a//b)
    

##################
# main functions #
##################

def encode(img: Img, data: bytes, **flags) -> Img:
    """
    Encodes binary data and header onto the least significant bits of colour channels in an image.
    :param img: The image in numpy array format.
    :param data: The binary data to encode within the image.
    :return:
    """

    # construct the flag byte that comes at the first part of the file.
    flagbyte = 0
    if "n_lsb" in flags and flags["n_lsb"] > 1: flagbyte |= LSB
    if "extension" in flags: flagbyte |= EXT
    if "filename" in flags: flagbyte |= NAME

    n_lsb = flags["n_lsb"] if flagbyte & LSB else 1

    if len(data) > space_available(img, **flags):
        raise ValueError("Image not big enough for data, either increase image size or bits encoded per channel.")

    # image dimensions
    w, h, c, bit_depth = get_img_meta(img)
    # iterator of all indexes in the image
    indexes = product(range(w), range(h), range(c)) if c > 1 else product(range(w), range(h))

    # write flagbyte to image
    write_int(img, indexes, 1, flagbyte, 1)

    if flagbyte & LSB: write_int(img, indexes, n_lsb=1, data=n_lsb, byte_length=1)
    if flagbyte & EXT: write_data_frame(img, indexes, n_lsb, bytes(flags["extension"], "utf-8"))
    if flagbyte & NAME: write_data_frame(img, indexes, n_lsb, bytes(flags["filename"], "utf-8"))

    # write actual data frame
    write_data_frame(img, indexes, n_lsb, data, size_byte_length=4)

    return img

def write_data_frame(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, data: bytes, size_byte_length: int=1):
    """
    Writes a frame of data to the image. First encodes the length and then encodes the data onto the image.
    :param img: The image in numpy array format.
    :param indexes: The indexes to write at. Indexes are removed as they are used.
    :param n_lsb: The number of bits to write over at each index. Directly affects the number of indexes used.
    :param size_byte_length: The number of bytes used to write the length of the data.
    """
    write_int(img, indexes, n_lsb=n_lsb, data=len(data), byte_length=size_byte_length)
    write_bytes(img, indexes, n_lsb=n_lsb, data=data)

def write_int(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, data: int, byte_length: int):
    write_bits(img, indexes, n_lsb, bytes_to_bitarray(data.to_bytes(byte_length, byteorder="little")))

def write_bytes(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, data: bytes):
    write_bits(img, indexes, n_lsb, bytes_to_bitarray(data))

def write_bits(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, data: Bits):
    """
    Writes chunked bits of data to the least significant bit of an image.
    :param img: Numpy Array of image data.
    :param indexes: Indexes and ordering of pixel locations in the image to write the data to.
    :param n_lsb: The number of bits in the image to be overwritten in each channel
    :param data: Bitarray of data
    """

    chunked_data = (data[i:i + n_lsb] for i in range(0, data.length(), n_lsb))

    # bit depth of the image (number of bits in each pixel channel
    bit_depth = img.dtype.itemsize * 8

    # check each channel has enough bit depth to accommodate using that many bits to encode with.
    if bit_depth < n_lsb:
        raise ValueError("Image bit depth not big enough for encoding with that many bits per channel")

    # calculate the bit mask to erase least significant bits on each pixel channel so they can be overwritten.
    mask = ((2 ** bit_depth) - 1) - ((2 ** (n_lsb)) - 1)  # e.g. 10111010 AND 11111100 (mask) = 10111000

    for index, d in zip(islice(indexes, ciel_div(data.length(), n_lsb)), chunked_data):
        colour = img.item(*index)
        encoded = (colour & mask) | int.from_bytes(d.tobytes(), byteorder="little")
        img.itemset(*index, encoded)


def decode_img(img: Img) -> Tuple[bytes, Dict[str, str]]:
    """
    Decodes data stored in an image.
    :param img: The image data has been stored in.
    :return: The data stored in the image.
    """
    w, h, c, bit_depth = get_img_meta(img) # image dimensions
    indexes = product(range(w), range(h), range(c)) if c > 1 else product(range(w), range(h))

    meta = dict()  # meta object to store header data

    # read header data
    flags = read_int(img, indexes, 1, 1)    
    n_lsb = read_int(img, indexes, 1, 1) if flags & LSB else 1
    if flags & EXT: meta["extension"] = bytes_to_string(read_data_frame(img, indexes, n_lsb, 1))
    if flags & NAME: meta["filename"] = bytes_to_string(read_data_frame(img, indexes, n_lsb, 1))

    # read data
    data = read_data_frame(img, indexes, n_lsb, 4)

    return data, meta

def read_data_frame(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, size_byte_length: int=1) -> bytes:
    return read_bytes(img, indexes, n_lsb, byte_length=read_int(img, indexes, n_lsb, byte_length=size_byte_length))    

def read_str(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, byte_length: int) -> str:
    return read_bytes(img, indexes, n_lsb, byte_length).decode("utf-8")

def read_int(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, byte_length: int) -> int:
    return int.from_bytes(read_bytes(img, indexes, n_lsb, byte_length), byteorder="little")

def read_bytes(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, byte_length: int) -> bytes:
    return read_bits(img, indexes, n_lsb, byte_length * 8).tobytes()

def read_bits(img: Img, indexes: Iterable[ImgIndex], n_lsb: int, bit_length: int) -> bitarray:
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
    
    for index in islice(indexes, ciel_div(bit_length, n_lsb)):
        chunk = bitarray.bitarray(endian="little")
        chunk.frombytes((img.item(*index) & mask).to_bytes(bytes_size, byteorder="little"))
        chunk_length = (n_lsb if total + n_lsb <= bit_length else bit_length - total)
        data += chunk[:chunk_length]
        total += chunk_length

    # check that the length of the extracted data is what was specified. If not then their were not enough indexes in
    # the image.
    if total < bit_length:
        raise ValueError("Ran out of indexes at which to extract data.")

    return data
