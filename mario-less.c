#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Set height of the pyramid
    int size;
    do
    {
        size = get_int("Height between 1 - 8: ");
    }
    while ((size >= 9) || (size <= 0));

    // Print pyramid
    for (int i = 0; i < size; i++)
    {
        // Add spaces in front of the #
        for (int x = 2; x > i; x++)
        {
            printf(" ");
        }

        // Print #
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}