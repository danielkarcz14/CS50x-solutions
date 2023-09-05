#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("usage: ./reverse INPUT.wav OUTPUT.wav \n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    char *input_file = argv[1];
    FILE *inptr = fopen(input_file, "r");
    if (inptr == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Read header
    // TODO #3

    WAVHEADER buffer;
    fread(&buffer, 44, 1, inptr);

    // Use check_format to ensure WAV format
    // TODO #4
    if (!(check_format(buffer)))
    {
        printf("Wrong file format!\n");
        return 1;
    }

    // Open output file for writing
    // TODO #5
    char *output_file = argv[2];
    FILE *outptr = fopen(output_file, "w");
    if (outptr == NULL)
    {
        printf("Wrong file format\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&buffer, 44, 1, outptr);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(buffer);
    // Write reversed audio to file
    // TODO #8
    int reverse[block_size];
    // move to the end of the last block
    fseek(inptr, block_size, SEEK_END);

    // read trhough all audio data
    while (ftell(inptr) - block_size > 44)
    {
        fseek(inptr, -2 * block_size, SEEK_CUR);
        fread(reverse, block_size, 1, inptr);
        fwrite(reverse, block_size, 1, outptr);
    }
    return 0;
}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return true;
    }
    return false;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    int size = header.numChannels * (header.bitsPerSample / 8);
    return size;
}