#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

bool only_digits (string s);

int main (int argc, string argv[])
{
    //exclude if more than 1 clia
    if (argc != 2)
    {
        //print error
        printf("Usage: ./caesar key\n");

        //break
        return 1;
    }

    string s = argv[1];

    //use the function to receive a bool from string after checking for digits
    bool c = only_digits(s);

    if (c == false)
    {
        //print error
        printf("Usage: ./caesar key\n");

        //break
        return 1;
    }

    //converting the string after we checked that is a number into integer
    int k = (atoi(s));

    if (k < 0)
    {
        //print error
        printf("Usage: ./caesar key\n");

        //break
        return 1;
    }

    //prompt user for plaintxtt
    string x = get_string("Plaintext: ");

    //decide where to print
    printf("ciphertext: ");

    //look inside plaintext char by char
    for( int j = 0, m = strlen(x); j < m; j++)
    {
        if(isupper(x[j]))
        {
            //convert into cyper
            printf("%c",(x[j] - 65 + k) % 26 + 65);
        }

        else if(islower(x[j]))
        {
            //convert into cyper
            printf("%c",(x[j] - 97 + k) % 26 + 97);
        }

        else
        {
            printf("%c", x[j]);
        }
    }

    printf("\n");
}

bool only_digits (string s)
{
    //look char by char of the string
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        //check for digits
        if (isdigit(s[i]) == false)
        {
            return false;
        }
    }
    return true;
}


