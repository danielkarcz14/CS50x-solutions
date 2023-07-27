#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Really cool project

bool key_check(int argc, string s);
int substitute(char c, string s);

int main(int argc, string argv[])
{
    string s = argv[1];
    bool n = key_check(argc, s);
    if (n == false)
    {
        return 1;
    }

    // Checks if key is alphabetic only, and makes the key uppecase letters, so the key works even if it is uppercase, lowercase letters combined
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(s[i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
        else if (islower(s[i]))
        {
            s[i] = toupper(s[i]);
        }
    }

    // Checks if there are repeated characters
    for (int i = 0; i < 26; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (s[i] == s[j])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

    // Input of plaintext
    string plaintext = get_string("plaintext:  ");
    printf("ciphertext: ");
    int len2 = strlen(plaintext);

    // Substitution
    for (int i = 0; i < len2; i++)
    {
        char c = substitute(plaintext[i], s);
        printf("%c", c);
    }
    printf("\n");
}

bool key_check(int argc, string s)
{
    // Checks if command line has only two arguments and contain 26 characters
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return false;
    }
    else if ((strlen(s)) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }
    return true;
}

int substitute(char c, string s)
{
    // c = (c - c + s[c - 'a']) this formula gets us to the desired position in the key string
    // Since the key is converted to uppercase we need to add 32 if the character is lowercase, so we are in lowercase characters interval
    if (islower(c))
    {
        c = (c - c + s[c - 'a']) + 32;
    }
    // If it is uppercase just use the formula
    else if (isupper(c))
    {
        c = (c - c + s[c - 'A']);
    }
    // If conditions are not met function returns the original value
    else
    {
        return c;
    }
    return c;
}
