import random
from PIL import Image

number_of_images = 100
image_size = (16, 16)

print("Creating images with random colored pixels")
myList = []
for i in range(number_of_images):
    image = Image.new("RGB", image_size)
    for x in range(image_size[1]):
        for y in range(image_size[0]):
            rand_r = random.randint(0,255)
            rand_g = random.randint(0,255)
            rand_b = random.randint(0,255)
            random_color = (rand_r, rand_g, rand_b)
            image.putpixel((x,y), random_color)

    filename = "image_" + str(i) + ".bmp"
    print("Saving image", filename)
    image.save(f"./ImageSpam/{filename}")
    myList.append(filename)
    MyFile = open('ImageList.txt', 'w')
    for element in myList:
        MyFile.write(element)
        MyFile.write('\n')
    MyFile.close()

