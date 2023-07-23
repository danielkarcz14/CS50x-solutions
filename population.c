#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int start_size;
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);

    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);

    // Years counter, set to -1 so when start = end it prints 0
    int years_counter = -1;
    do
    {
        start_size = start_size + (start_size / 3) - (start_size / 4);
        years_counter++;
    }
    while (start_size < end_size);
    printf("Years: %d\n", years_counter);
}