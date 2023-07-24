#include <cs50.h>
#include <stdio.h>
#include <string.h>


const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Array of value BITS_IN_BYTE
    int bit[BITS_IN_BYTE];
    // Input for message
    string text = get_string("Message: ");
    // Count string lenght
    int lenght = strlen(text);


    for (int j = 0; j < lenght; j++)
    {
        // Itarate through each array for BITS_IN_BYTE times, which is set to 8
        for (int i = 0; i < BITS_IN_BYTE; i++)
        {
            // If is divisible by 2 store 0 into array number i, and update value of checked array
            if (text[j] % 2 == 0)
            {
                bit[i] = 0;
                text[j] = text[j] / 2;
            }
            // If not divisible by 2 store 0 into array number i, and update value of checked array
            else if (text[j] % 2 != 0)
            {
                bit[i] = 1;
                text[j] = text[j] / 2;
            }
        }

        // Print arrays in reverse order
        for (int i = BITS_IN_BYTE; i >= 0; i--)
        {
            print_bulb(bit[i]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
