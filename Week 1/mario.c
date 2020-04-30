#include <cs50.h>
#include <stdio.h>

int main(void)
{

    // create integer variable and ask user for the height, which needs to be positive and no bigger than 23
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 0 || n > 23);

    // create a loop that repeats until height is achieved
    for (int i = 0; i < n; i++)
    {
        // print the spaces
        for (int s = 0; s < (n - (1 + i)); s++)
        {
            printf(" ");
        }

        // print the hashes
        for (int s = 0; s < (n + 1) - (n - (1 + i)); s++)
        {
            printf("#");
        }

        // print new row
        {
            printf("\n");
        }
    }

}