/**
 * Name: Maria Daan
 * Student number: 11243406
 * Prints the users initials
 */

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>


int main(void)
{
    // Prompt user for input: name
    string name = get_string("");

    // Convert first letter of name to upper case if needed and print it
    name[0] = toupper(name[0]);
    printf("%c", name[0]);

    // Do the same for the second name, third name, etc by localizing the spaces
    for (int i = 0; i < strlen(name); i++)
    {
        if (name[i] == ' ')
        {
            int place = (i + 1);
            name[place] = toupper(name[place]);
            printf("%c", name[place]);
        }
    }

    // End with a new line
    printf("\n");

}
