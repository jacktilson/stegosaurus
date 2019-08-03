""" This file is called to create a random string of characters
for use as a unique transaction ID to track pre and post encode
images, and the corresponding data files throughout the user
journey. """

from string import ascii_letters
from random import choice

# Define upper and lower bounds
u_bound = 64
l_bound = 32

def gen(): 
  return ''.join(choice(ascii_letters) for i in range(choice(range(l_bound, u_bound + 1))))