<template lang="pug">
b-container
  b-row
    b-col(sm="12")
      b-card.mt-3(img-src="@/assets/about_lsb.svg" img-right)
        b-card-title What is Stegosaurus?
        b-card-text Stegosaurus is a steganography tool designed to allow users to encode data within image files.
          |  We are using a method of steganography known as LSB (Least significant bit) steganography. This involves
          | using the least significant bits of each channel of each pixel. For example, with a 24 bit, 3 channel image.
          | each colour channel has 8 bits. eg. 10110000, in this example the least most significant bit is on the far
          | right side and the decimal of this would be 176. If we were to use 2 LSB for our data file, this would effectively 
</template>
