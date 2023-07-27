#include <stdio.h>

int main(void)
{
    char name[40];

    // Prompt for name
    printf("Your name? ");
    scanf("%s", name);

    // Print result
    printf("Hello, %s\n", name);
}