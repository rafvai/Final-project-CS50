#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //accept only 1 CLA
    if (argc != 2)
    {
        //print error message
        printf(". /Usage: substitution KEY\n");

        //break
        return 1;
    }

    //look inside the string
    for (int i = 0, l = strlen(argv[1]); i < l; i++)
    {
        //exclude if not 26 charac
        if (l != 26)
        {
            //error message
            printf("Key must contain 26 characters\n");

            return 1;
        }

        //accept only alphab charac
        else if (isalpha(argv[1][i]) == false)
        {
            //error message
            printf ("Key must contain only alphabetical characters\n");

            return 1;
        }

        //compare each character
        for (int t = i - 1; t >= 0; t--)
        {
            if (argv[1][t] == argv[1][i])
            {
                printf("Each character must be included only once\n");

                return 1;
            }
        }
    }

    //prompt for plaint
    string s = get_string("Plaintext: ");

    printf("ciphertext: ");

    //look inside prompt txt
    for (int j = 0, n = strlen(s); j < n; j++)
    {
        //cipher upper
        if (isupper(s[j]))
        {
            printf("%c", toupper(argv[1][s[j] - 65]));
        }

        else if (islower(s[j]))
        {
            //cipher lower
            printf("%c", tolower(argv[1][s[j] - 97]));
        }

        else
        {
            printf("%c", s[j]);
        }
    }

    printf("\n");
}

