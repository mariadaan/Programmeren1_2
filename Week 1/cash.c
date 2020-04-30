#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // get input from the user: the amount of change
    float n;
    do
    {
        n = get_float("Change owed: ");
    }
    while (n < 0);

    // convert dollars to cents
    float c = n * 100;
    c = round(c);
    int d = c;

    // new variable to count the amount of coins
    int e = e;

    // subtract 25 cents from the amount as many times as possible
    while (d >= 25)
    {
        (d = d - 25);
        (e = e + 1);
    }

    // subtract 10 cents from the remaining amount as many times as possible
    while (d >= 10)
    {
        (d = d - 10);
        (e = e + 1);

    }

    // subtract 5 cents from the remaining amount as many times as possible
    while (d >= 5)
    {
        (d = d - 5);
        (e = e + 1);
    }

    // subtract 1 cent from the remaining amount as many times as possible
    while (d >= 1)
    {
        (d = d - 1);
        (e = e + 1);
    }

    // Print e: the amount of coins used
    {
        printf("%i\n", e);
    }

}