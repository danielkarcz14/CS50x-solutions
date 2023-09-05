
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
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;
            float average = round((red + green + blue) / 3);

            // update values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
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
            swap(&image[i][j], &image[i][width - 1 - j]);
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
    // declare variables
    RGBTRIPLE copy[height][width];
    int counter = 0;
    float sum_red;
    float sum_green;
    float sum_blue;

    // make copy
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // reset counter and average values
            counter = 0;
            sum_red = 0;
            sum_green = 0;
            sum_blue = 0;
            // itareate through every 3x3 box
            for (int p = i - 1; p < i + 2; p++)
            {
                // edge case
                if (p < 0 || p >= height)
                {
                    continue;
                }
                for (int m = j - 1; m < j + 2; m++)
                {
                    // edge case
                    if (m < 0 || m >= width)
                    {
                        continue;
                    }
                    // sum color values
                    sum_red = round(sum_red + copy[p][m].rgbtRed);
                    sum_green = round(sum_green + copy[p][m].rgbtGreen);
                    sum_blue = round(sum_blue + copy[p][m].rgbtBlue);
                    counter++;
                }
            }
            // count average for each color value
            float average_red = round(sum_red / counter);
            float average_green = round(sum_green / counter);
            float average_blue = round(sum_blue / counter);
            // update pixel color
            image[i][j].rgbtRed = average_red;
            image[i][j].rgbtGreen = average_green;
            image[i][j].rgbtBlue = average_blue;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE copy[height][width];

    // define matrixes
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float gxR = 0, gxG = 0, gxB = 0;
            float gyR = 0, gyG = 0, gyB = 0;

            // itareate through 3x3 box
            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 3; col++)
                {
                    // edge cases
                    if (i + row - 1 < 0 || i + row - 1 >= height || j + col - 1 < 0 || j + col - 1 >= width)
                    {
                        continue;
                    }
                    // Gx
                    gxR += image[i + row - 1][j + col - 1].rgbtRed * Gx[row][col];
                    gxG += image[i + row - 1][j + col - 1].rgbtGreen * Gx[row][col];
                    gxB += image[i + row - 1][j + col - 1].rgbtBlue * Gx[row][col];
                    // Gy
                    gyR += image[i + row - 1][j + col - 1].rgbtRed * Gy[row][col];
                    gyG += image[i + row - 1][j + col - 1].rgbtGreen * Gy[row][col];
                    gyB += image[i + row - 1][j + col - 1].rgbtBlue * Gy[row][col];
                }
            }
            // sobel colors
            float sobel_red = round(sqrt(((gxR * gxR) + (gyR * gyR))));
            float sobel_green = round(sqrt(((gxG * gxG) + (gyG * gyG))));
            float sobel_blue = round(sqrt(((gxB * gxB) + (gyB * gyB))));

            // cap at 255
            if (sobel_red > 255)
            {
                sobel_red = 255;
            }
            if (sobel_green > 255)
            {
                sobel_green = 255;
            }
            if (sobel_blue > 255)
            {
                sobel_blue = 255;
            }
            // update
            copy[i][j].rgbtRed = sobel_red;
            copy[i][j].rgbtGreen = sobel_green;
            copy[i][j].rgbtBlue = sobel_blue;
        }
    }

    // copy back to original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }
    return;
}
