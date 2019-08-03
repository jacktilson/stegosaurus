# The Header
The Header is the section of the encoded image which will tell the decoder what bits of the image contain the actual 
encoded data

## Layout
**_The first 16 bits are stored at a depth of 1 LSB_** across the first 16 available channels, which (in an 24 bit
 image) would be across the first ~5 pixels, as each pixel has three colour channels (1 bit per channel).

Flag Bits | Flag Name |Purpose
------|------ | -------------
0 | LSB|If the number of LSB is > 1
1 | EXT |Set if a file extension is present
2 | NAME |  Set if a filename is present
3-7 | |Reserved for future use


Size | Required | Purpose | Bit Depth
---|---|---|---
1 byte | Yes | Flag bits | 1
1 byte | When LSB | Number of LSB (when LSB) | 1
1 byte | When EXT | Length of file ext in bytes (when EXT) | nLSB
1 byte | When NAME | Length of filename in bytes (when NAME) | nLSB
4 bytes | Yes | Length of data in bytes | nLSB
 

# Example Data Structure
Byte | Value | Purpose
----|-------|------------
1 | 11100000 | Sets the flags (LSB, EXT, NAME)
2 | 00000010 | 2 LSB
3 | 00000011 | Extension is 3 bytes long .txt
4-6 | "txt" | Extension Name
7 | 00000111 | Filename is 7 bytes long "My File"
8-14 | "My File" | File name
15 | 00000000 | 
16 | 00000000 | 
17 | 00000001 | 
18 | 00010100 | Data size is 276 bytes long
19-294 | Data | The data






