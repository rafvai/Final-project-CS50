// Implements a dictionary's functionality
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

 //creating variable to count word
unsigned int counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    //hash the word
    unsigned int i = hash(word);

    //creating cursor
    node *cursor = table[i];

    //compare word to dictionary
    if (strcasecmp(cursor -> word, word) == 0)
    {
        return true;
    }

    //loop through SLL
    while (cursor -> next != NULL)
    {
        //move cursor forward
        cursor = cursor -> next;

        //compare word to dictionary
        if (strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hashnum;

    //find hash number if is lowercase
    if (islower(word[0]) != 0)
    {
        //hash number
        hashnum = word[0] - 97;

        return hashnum;
    }

    //assign a hash number to word
    hashnum = word[0] - 65;

    return hashnum;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //open FILE
    FILE *ptr = fopen(dictionary, "r");

    //creating an array to read file REMEMBER TO FREE MEMORY
    char *buffer = malloc(LENGTH + 1);

    //safety check
    if (buffer == NULL)
    {
        return false;
    }

    //repeat until end of dictionary
    while (fscanf(ptr, "%s", buffer) != EOF)
    {
        //allocate memory for each word REMEMBER TO FREE MEMORY
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        //copy word into node's word space
        strcpy (n -> word, buffer);

        counter++;

        //hash word and get a int back
        int hashindex = hash(buffer);

        //coping the old head of SLL into new node
        n -> next = table[hashindex];

        //changing the head to the new word
        table[hashindex] = n;
    }
    fclose(ptr);

    //free memory
    free(buffer);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    //creating variables cursor and temp
    node *cursor;

    node *tmp;

    //loop through the hash list
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }
        //set cursor to point to the first element of the SLL
        cursor = table[i];

        //set temp to point at hash head
        tmp = cursor;

        //loop through the SLL until end
        while (cursor -> next != NULL)
        {
            //move cursor to the next element of SLL
            cursor = cursor -> next;

            //free the element SLL
            free(tmp);

            tmp = cursor;
        }
        free(cursor);
    }
    return true;
}
