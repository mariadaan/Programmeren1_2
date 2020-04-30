# Problem Set 6
# Name: Maria Daan
# Student Number: 11243406
#
# This program encrypts messages using Vigenère’s cipher.

import sys
from cs50 import get_string

# check for (valid) key
if len(sys.argv) != 2 or not sys.argv[1].isalpha():
    print("Usage: ./vigenere key")
    exit(1)

# get/remember user input
key = sys.argv[1]
plaintext = get_string("plaintext: ")

ciphertext = ""
text_len = len(plaintext)
key_len = len(key)
alpha_len = 26
count = 0

# encrypt each letter from the plaintext to ciphertext
for i in range(text_len):

    # convert key to numeric value
    char_key = ord(key.upper()[(i - count) % key_len]) - ord('A')
    char_plain = plaintext[i]

    # make sure the plaintexts' case and non-alpha characters will be preserved
    if char_plain.isalpha():
        if char_plain.isupper():
            case = ord('A')
        else:
            case = ord('a')

        # convert plaintext to ciphertext by using the key
        cipher = (ord(char_plain) - case + char_key) % alpha_len + case
    else:
        count += 1
        cipher = ord(plaintext[i])

    ciphertext += chr(cipher)

print(f"ciphertext: {ciphertext}")