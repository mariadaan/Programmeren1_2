#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{

    long long c;

    // get input from user: creditcard number
    do
    {
        c = get_long_long("Number:  ");
    }
    while (c < 0);

    long long d = c;
    long long g = c;
    int a = a;
    long long k = d;
    int b = b;
    int e = e;
    int f = f;
    int h = h;
    int j = j;
    int m = m;
    long long n = n;
    long long o = o;

    // check conditions of creditcard number
    while (d >= 10)
    {
        (d = d / 10);
        (k = d % 10);

        (a = k * 2);

        (b = a % 10);

        if (a - b == 10)
        {
            (e = b + 1);
        }
        else
        {
            (e = b);
        }

        (f = f + e);

        (d = d / 10);
    }

    while (g >= 1)
    {
        (h = g % 10);
        (g = g / 100);

        (j = j + h);
    }

    (m = j + f);

    // end program if number doesn't satisfy the conditions
    if (m % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        // 15 digits -> American Express if first digits are 34 or 37
        n = c / (pow(10, 13));

        if (c > (pow(10, 14) - 1) && c < pow(10, 15) && ((n == 34) || (n == 37)))
        {
            printf("AMEX\n");
        }
        else
        {


            // 16 digits -> Mastercard if first digits are 51, 52, 53, 54 or 55, Visa if first digit is 4
            o = c / (pow(10, 14));

            if (c > (pow(10, 15) - 1) && c < pow(10, 16))
            {
                if (o >= 51 && o <= 55)
                {
                    printf("MASTERCARD\n");
                }
                else
                {
                    if (o / 10 == 4)
                    {
                        printf("VISA\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                }
            }
            else
            {

                // 13 digits -> Visa if first digit is 4
                if (c > (pow(10, 12) - 1) && c < pow(10, 13) && (o / 10 == 4))
                {
                    printf("VISA\n");
                }

                // if number doesn't meet any of these conditions, card still invalid
                else
                {
                    printf("INVALID\n");
                }
            }
        }

    }

}