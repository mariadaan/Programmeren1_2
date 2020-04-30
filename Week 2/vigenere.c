/**
 * Name: Maria Daan
 * Student number: 11243406
 * Encrypts text into cyphertext by using a textual keyword
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
        string key = argv[1];
        int keylength = strlen(key);
        int nonalphacount = 0;

        // Check if a usable key has been implemented
        for (int j = 0; j < keylength; j++)
        {
            if (!isalpha(key[j % keylength]))
            {
                printf("Usage: ./vigenere k\n");
                return 1;
            }
        }

        // Get input from user: the text that needs to be encrypted and get ready to print the ciphertext
        string input = get_string("plaintext: ");
        int inputlength = strlen(input);
        printf("ciphertext: ");

        // Encrypt each letter from the input to an encrypted letter. Repeat the loop as many times as the length of the input
        for (int i = 0; i < inputlength; i++)
        {
            // Convert the key to upper case and make sure non-alpha characters do not effect which letter in the key is used to encrypt
            int upperkey = toupper(key[(i - nonalphacount) % keylength]);
            int alphkey = (upperkey - 65);

            // Make sure each lower case in the input encrypts and stays a lower case
            if (islower(input[i]))
            {
                int alphinput = (input[i] - 97);
                char cipher = ((alphinput + alphkey) % 26 + 97);
                printf("%c", cipher);
            }

            // Do the same for each upper case in the input
            else if (isupper(input[i]))
            {
                int alphinput = (input[i] - 65);
                char cipher = ((alphinput + alphkey) % 26 + 65);
                printf("%c", cipher);
            }

            // Keep track of spaces and print other characters than letters directly
            else if (!isalpha(input[i]))
            {
                nonalphacount++;
                printf("%c", input[i]);
            }
        }
        printf("\n");
    }

    // Make clear how the user is supposed to use the program when this hasn't been done right
    else
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }

    return 0;
}