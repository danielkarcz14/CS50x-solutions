#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>



bool only_digits(string s);
char rotate(int key, char c);

int main(int argc, string argv[])
{
    // Only two arguments allowed
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    string s = argv[1];

    // Argument has to be digit
    if (only_digits(s) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Convert argv[1] to an integer
    int key = atoi(argv[1]);

    // Input from user
    string plaintext = get_string("plaintext:  ");
    printf("ciphertext: ");
    // Count string lenght
    int len2 = strlen(plaintext);
    // Iterate through each array in string
    for (int i = 0; i < len2; i++)
    {
        // Call rotate function of each arrau in plaintext
        char c = rotate(key, plaintext[i]);
        printf("%c", c);
    }
    printf("\n");
}


bool only_digits(string s)
{
    int len = strlen(s);
    for (int i = 0; i < len; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(int key, char c)
{
    // Check if array in string plaintext is alphabetical and lowercase
    if (isalpha(c) && islower(c))
    {
        c = (c - 97 + key) % 26 + 97;

    }
    // Check if array in string plaintext is alphabetical and uppercase
    else if (isalpha(c) && isupper(c))
    {
        c = (c - 65 + key) % 26 + 65;
    }
    // If conditions are not met function returns what user typed
    else
    {
        return c;
    }
    return c;
}