import os, numpy, cv2, bitarray
from itertools import product, islice
from typing import Iterable, Tuple

##################
# util functions #
##################


def read_img(img_filepath: str) -> numpy.ndarray:
    assert os.path.isfile(img_filepath), "Not a valid path"
    assert img_filepath.split(".")[-1].lower() in ["bmp"], "Not an accepted file extension"
    return cv2.imread(img_filepath)


def write_img(img_filepath: str, img: numpy.ndarray):
    cv2.imwrite(img_filepath, img)


def string_to_bitarray(text: str) -> bitarray.bitarray:
    data = bitarray.bitarray(endian="little")
    data.frombytes(bytes(text, "utf-8"))
    return data

##################
# main functions #
##################


def encode(img: numpy.ndarray, n_lsb: int, data: bitarray.bitarray) -> numpy.ndarray:
    # no. of available bits (LSB per channel * width * height * channels)
    bits_available = n_lsb * (numpy.product(img.shape))

    if data.length() > bits_available - (40 * 8):  # take off header size
        raise ValueError("Image not big enough for data, either increase image size or bits encoded per channel.")

    byte_length = bitarray.bits2bytes(data.length())  # size of the actual data in bytes
    height, width, channels = img.shape  # image dimensions
    indexes = product(range(width), range(height), range(channels))  # iterator of all indexes in the image

    # create header
    # First 8 bits: number of bits being encoded in each channel.
    # Next 32 bits: number bytes of data being encoded)
    header = bitarray.bitarray(endian="little")
    header.frombytes(n_lsb.to_bytes(1, byteorder="little"))
    header.frombytes(byte_length.to_bytes(4, byteorder="little"))

    # write header to image
    write_to_img(img, islice(indexes, 40), 1, (header[i:i + 1] for i in range(header.length())))

    # write data to image
    write_to_img(img, indexes, n_lsb, (data[i:i + n_lsb] for i in range(0, data.length(), n_lsb)))

    return img


def write_to_img(img: numpy.ndarray, indexes: Iterable[Tuple], n_lsb: int, data: Iterable[bitarray.bitarray]):
    """
    Writes chunked bits to the image.
    :param img:
    :param indexes:
    :param n_lsb:
    :param data:
    :return:
    """
    # bit depth of the image (number of bits in each pixel channel
    bit_depth = img.dtype.itemsize * 8

    # check each channel has enough bit depth to accommodate using that many bits to encode with.
    if bit_depth < n_lsb:
        raise ValueError("Image bit depth not big enough for encoding with that many bits per channel")

    # calculate the bit mask to erase least significant bits on each pixel channel so they can be overwritten.
    mask = ((2 ** bit_depth) - 1) - ((2 ** (n_lsb)) - 1)  # e.g. 10111010 AND 11111100 (mask) = 10111000

    for (x, y, c), d in zip(indexes, data):
        colour = img.item(x, y, c)
        encoded = (colour & mask) | int.from_bytes(d.tobytes(), byteorder="little")
        print(bin(mask))
        print(f"Pixel@({x},{y})(c{c}) Data: {d.to01()}, Colour: {colour}, Encoded: {encoded}")
        img.itemset(x, y, c, encoded)
