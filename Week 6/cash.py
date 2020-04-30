# Problem Set 6
# Name: Maria Daan
# Student Number: 11243406
#
# This program calculates the minimum number
# of coins required to give a user change.

from cs50 import get_float

# check for valid input
while True:
    n = get_float("Change owed: ")
    if n > 0:
        break

# convert to cents and define cointypes
cents = round(n * 100)
types = (25, 10, 5, 1)
coins = 0

# count how many coins are used
for i in range(len(types)):
    coins += cents // types[i]
    cents = cents % types[i]

print(f"{coins}")
