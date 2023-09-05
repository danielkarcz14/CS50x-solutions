#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("usage: ./recover IMAGE\n");
        return 1;
    }

    // open card
    FILE *inptr = fopen(argv[1], "r");

    if (inptr == NULL)
    {
        printf("Couldn't open file\n");
        return 2;
    }

    // define varables
    char *filename = malloc(8);
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];
    int jpg_counter = 0;
    FILE *image = NULL;

    // repeat until reaching end of the card
    // read 512 bytes into buffer
    while (fread(buffer, BLOCK_SIZE, 1, inptr) == 1)
    {
        // start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if not first jpeg close file
            if (jpg_counter != 0)
            {
                fclose(image);
            }

            // create new jpg file
            sprintf(filename, "%03i.jpg", jpg_counter);
            image = fopen(filename, "w");
            fwrite(buffer, BLOCK_SIZE, 1, image);
            jpg_counter++;
        }
        // else if jpeg is opened just write the bytes inside currently opened jpeg
        else if (jpg_counter != 0)
        {
            fwrite(buffer, BLOCK_SIZE, 1, image);
        }
    }

    // close all files
    if (image != NULL)
    {
        fclose(image);
    }

    fclose(inptr);

    // free memory
    free(filename);
    return 0;
}