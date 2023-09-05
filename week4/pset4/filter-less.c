#include "helpers.h"
#include <math.h>
void swap(RGBTRIPLE *a, RGBTRIPLE *b);
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // average
            float average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            // change color of pixel
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // store original values for current pixel
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            // store sepia values
            int sepia_red = round(.393 * red + .769 * green + .189 * blue);
            int sepia_green = round(.349 * red + .686 * green + .168 * blue);
            int sepia_blue = round(.272 * red + .534 * green + .131 * blue);

            // check if it the color is in 8 bit range
            if (sepia_red > 255)
            {
                sepia_red = 255;
            }
            if (sepia_green > 255)
            {
                sepia_green = 255;
            }
            if (sepia_blue > 255)
            {
                sepia_blue = 255;
            }

            // change original values to sepia values
            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // set opossite value
            int opposite_value = width - 1 - j;
            // call swap function
            swap(&image[i][j], &image[i][opposite_value]);
        }
    }
    return;
}

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    // Make a copy of original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    // Loop trough every pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // set counters for total red, green and blue
            int red = 0;
            int green = 0;
            int blue = 0;
            // set division counter
            int division = 0;
            // Loop through box
            for (int k = i - 1; k <= i + 1; k++)
            {
                // check for top and bottom edge case
                if (k < 0 || k > height - 1)
                {
                    continue;
                }
                for (int p = j - 1; p <= j + 1; p++)
                {
                    // check for let and right edge case
                    if (p < 0 || p > width - 1)
                    {
                        continue;
                    }
                    red = red + copy[k][p].rgbtRed;
                    green = green + copy[k][p].rgbtGreen;
                    blue = blue + copy[k][p].rgbtBlue;
                    division++;
                }
            }
            // Calculate average and update with new color
            image[i][j].rgbtRed = round((float) red / division);
            image[i][j].rgbtGreen = round((float) green / division);
            image[i][j].rgbtBlue = round((float) blue / division);
        }
    }
    return;
}
