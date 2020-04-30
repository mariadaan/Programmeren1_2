// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    char num = 0;
    char denum = 0;

    // Determine the numerator and the denumerator
    num = fraction[0];
    denum = fraction[2];

    // Convert (de)numerator to non-ASCII values
    num -= '0';
    denum -= '0';

    // Multiply both by 2 until the division in represented in eights
    while (denum != 8)
    {
        num *= 2;
        denum *= 2;
    }

    return num;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // Set the default frequency to 440 (note A4)
    float freq = 440;
    char letter = note[0];

    // Calculate the frequency of each note in the 4th octave by moving up or down a certain number of semitones from A4
    if (letter == 'C')
    {
        freq /= pow(2.0, (9.0 / 12.0));
    }
    else if (letter == 'D')
    {
        freq /= pow(2.0, (7.0 / 12.0));
    }
    else if (letter == 'E')
    {
        freq /= pow(2.0, (5.0 / 12.0));
    }
    else if (letter == 'F')
    {
        freq /= pow(2.0, (4.0 / 12.0));
    }
    else if (letter == 'G')
    {
        freq /= pow(2.0, (2.0 / 12.0));
    }
    else if (letter == 'B')
    {
        freq *= pow(2.0, (2.0 / 12.0));
    }

    char octave = note[1];

    // If there is an accidental in the note, go up or go down 1 semitone
    if (strlen(note) == 3)
    {
        char accidental = note[1];
        octave = note[2];

        if (accidental == 'b')
        {
            freq = freq / pow(2.0, (1.0 / 12.0));
        }
        else if (accidental == '#')
        {
            freq = freq * pow(2.0, (1.0 / 12.0));
        }
    }

    // Calculate frequency on the basis of how much octaves the octave is removed from the default octave 4
    int value = '4'- octave;
    freq /= (pow(2, value));

    // Convert the float value to an integer by rounding it
    int frequen = round(freq);
    return frequen;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // Compare line to blank line, which is represented as "" in a string
    if (strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
