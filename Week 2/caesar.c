/**
 * Name: Maria Daan
 * Student number: 11243406
 * Encrypts text into cyphertext by using a numeral key
 */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    // Check if program is used correctly
    if (argc == 2)
    {
        // Get input from user: the text that needs to be encrypted and get ready to print the ciphertext
        string input = get_string("plaintext: ");
        int inputlength = strlen(input);
        int key = atoi(argv[1]);
        printf("ciphertext: ");

        // Encrypt each letter from the input to an encrypted letter. Repeat the loop as many times as the length of the input
        for (int i = 0; i < inputlength; i++)
        {
            int letter = input[i];
            int cipheraz = (letter + key);

            if isalpha(letter)
            {
                // Make sure each upper case wraps around from z to a (cipherza)
                if (isupper(letter) && (cipheraz > 90))
                {
                    int cipherza = cipheraz - 65;
                    cipherza %= 26;
                    cipherza += 65;
                    printf("%c", cipherza);
                }
                // Do the same for each lower case
                else if (islower(letter) && (cipheraz > 122))
                {
                    int cipherza = cipheraz - 97;
                    cipherza %= 26;
                    cipherza += 97;
                    printf("%c", cipherza);
                }
                // If a letter doesn't need to wrap around, just print cipheraz
                else
                {
                    printf("%c", cipheraz);
                }
            }

            // If the input character is non-alpha, print this character right away
            else
            {
                printf("%c", letter);
            }
        }
        printf("\n");
    }

    // Make clear how the user is supposed to use the program when this hasn't been done right
    else
    {
        printf("Usage: ./caesar 14\n");
        return 1;
    }

    return 0;

}