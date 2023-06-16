# TODO
from cs50 import get_int

while True:
    # prompt user for height
    height = get_int("Height: ")
    # number between 1 and 8
    if height > 0 and height < 9:
        break
k = 1

# 2D loop
for i in range(height):
    for j in range(height + 2 + k):
        # create spaces between pyramids
        if j == height or j == height + 1:
            print(" ", end="")
        elif j + i >= height - 1:
            print("#", end="")
        else:
            print(" ", end="")
    k += 1
    print()
