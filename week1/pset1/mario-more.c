#include <cs50.h>
#include <stdio.h>

void get_pyramid(int height);

int main(void)
{
    // Input height of the pyramid
    int height;
    do
    {
        height = get_int("Height of the pyramid: ");
    }
    while ((height >= 9) || (height <= 0));

    // Call function for pyramid height
    get_pyramid(height);

}


void get_pyramid(int height)
{

    //Loop for number of rows
    for (int i = 0; i < height; i++)
    {
        // Printing spaces in front of the hashtags
        for (int p = height - 1; p > i; p--)
        {
            printf(" ");
        }

        // Printing left side of the pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Print column of width 2 spaces on every row between the pyramids
        printf("  ");

        // Printing right side of the pyramid
        for (int n = 0; n <= i; n++)
        {
            printf("#");
        }

        // Printing new row after every iteration
        printf("\n");
    }
}