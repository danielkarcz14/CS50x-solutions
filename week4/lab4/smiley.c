#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (image[i][j].rgbtBlue == 0x00 && image[i][j].rgbtBlue == 0x00 && image[i][j].rgbtBlue == 0x00)
            {
                image[i][j].rgbtBlue = 0x4F;
                image[i][j].rgbtRed = 0x2A;
                image[i][j].rgbtGreen = 0xAA;
            }
        }
    }
}
