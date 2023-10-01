// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 7919;

// Hash table
node *table[N];

// word counter
int word_counter = 0;

// Default dictionary
#define DICTIONARY "dictionaries/large"

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// start with emtpy hash table
void null_hash_table()
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int len = strlen(word);
    unsigned int hash_value = 0;
    for (int i = 0; i < len; i++)
    {
        hash_value += toupper(word[i]);
    }

    unsigned int multiplication_sum = abs(toupper(word[0]) - toupper(word[1]));
    if (word[1] == '\0')
    {
        multiplication_sum = toupper(word[0]);
    }

    return (hash_value * multiplication_sum) % 7919;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary file
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        return false;
    }
    // read strings from file one at time
    char buffer[LENGTH];
    while ((fscanf(inptr, "%s", buffer)) != EOF)
    {
        // create a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // copy word into node
        strcpy(n->word, buffer);

        // hash the word
        int index = hash(buffer);

        // insert node into hash table at hashed index
        n->next = table[index];
        table[index] = n;

        // count words
        word_counter++;
    }
    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
