// Helper functions

#include <cs50.h>
#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "helpers.h"

// Returns true if value is in array of n values, else false
bool search(int value, int values[], int n)
{
    // Set a start and end to the array that needs to be searched
    int start = 0;
    int end = n - 1;

    while (start <= end)
    {
        // Determine the middle of the array
        int mid = (start + end) / 2;

        // Check whether the value you are looking for is on the left or the right of the middle and modify end/start
        if (value < values[mid])
        {
            end = mid - 1;
        }
        else if (value > values[mid])
        {
            start = mid + 1;
        }
        // If the value is in the middle, this means the value has been found
        else if (value == values[mid])
        {
            return true;
        }
    }
    // If the value was not found after the previous loop, value is not in the array
    return false;
}

// Sorts array of n values using selection sort
void sort(int values[], int n)
{
    int minvalue = values[0];
    int minplace = 0;

    // Create a start of the array that shifts one place each time the loop executes
    for(int start = 0; start < (n - 2); start++)
    {
        // Set default minimum value to the start of the array
        minvalue = values[start];
        minplace = start;

        // Change minimum value if a lower value has been found elsewhere in the array
        for(int i = start; i < n; i++)
        {
            if (values[i] < minvalue)
            {
                minvalue = values [i];
                minplace = i;
            }
            // Make sure the place of the minimum stays the start place if the value is in the right place already
            else if (values[minplace] > values[start])
            {
                minplace = start;
            }
        }
        // Swap value at start of array to the lowest value in the remaining array
        int k = values[start];
        values[start] = values[minplace];
        values[minplace] = k;
    }
    return;
}