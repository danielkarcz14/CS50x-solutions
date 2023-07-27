// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
string replace(string s, int len, int argc, string argv[]);
int check_cmd(int argc, string argv[]);

int main(int argc, string argv[])
{
    // Command-line check
    if (check_cmd(argc, argv) == 0)
    {
        return 0;
    }

    // String lenght
    int len = strlen(argv[1]);
    string s = argv[1];

    printf("%s\n", replace(s, len, argc, argv));

}


int check_cmd(int argc, string argv[])
{
    for (int i = 0; i < 1; i++)
    {
        if (argv[1] == 0)
        {
            printf("Missing command-line argument\n");
            return 0;
        }
        else if (argv[i + 2] > 0)
        {
            printf("Only one command-line argument allowed\n");
            return 0;
        }
    }
    return 1;
}

string replace(string s, int len, int argc, string argv[])
{
     for (int i = 0; i < len; i++)
    {
        if (s[i] == 'a')
        {
            s[i] = '6';

        }
        else if (s[i] == 'e')
        {
            s[i] = '3';

        }
        else if (s[i] == 'i')
        {
            s[i] = '1';

        }
        else if (s[i] == 'o')
        {
            s[i] = '0';

        }
    }
    return s;
}