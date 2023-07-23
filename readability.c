#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int count_letter(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{
    string text = get_string("Text: ");
    //printf("%d letters\n", count_letter(text));       // check
    //printf("%d words\n", count_words(text));          // check
    //printf("%d sentences\n", count_sentences(text));  // check

    // Coleman-Liau index
    float L = ((float)count_letter(text) / (float)count_words(text)) * 100;
    float S = ((float)count_sentences(text) / (float)count_words(text)) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %1.f\n", index);
    }
}

// Function for counting number of letters
int count_letter(string text)
{
    int letter_counter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            letter_counter++;
        }
        else if (islower(text[i]))
        {
            letter_counter++;
        }
    }
    return letter_counter;
}

// Function for counting number of words
int count_words(string text)
{
    // Set the counter to 1, so it adds the last word as well
    int word_counter = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            word_counter++;
        }
    }
    return word_counter;
}

// Function for counting number of sentences
int count_sentences(string text)
{
    int sentence_counter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence_counter++;
        }
    }
    return sentence_counter;
}

