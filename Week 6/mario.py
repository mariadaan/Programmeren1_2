# Problem Set 6
# Name: Maria Daan
# Student Number: 11243406
#
# This program prints out a half-pyramid of a specified height.

from cs50 import get_int

max_height = 23

# check for valid input
while True:
    height = get_int("Height: ")
    if height >= 0 and height <= max_height:
        break

# print spaces and hashes until specified height is achieved
for i in range(height):
    print(" " * (height - i - 1), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1), end="")
    print()