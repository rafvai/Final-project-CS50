#include <cs50.h>
#include <stdio.h>

int main(void)

{
    //the integer i want from the user and my variable k
    int n; int k = 0;

    do
    {
        // ask the user for size
         n = get_int("Height: ");
    }

    while(n < 1 || n > 8);

     //rows
    for (int i = 0; i < n ; i++)

         {
                    //columns
              for (int j = 0; j <= (n + 2) + k ; j++)

                    {
                         if ( j == n || j == (n + 1))

                          //spaces between pyramids
                            printf(" ");

                         else if ((i + j) >= (n - 1))

                            //blocks
                             printf("#");

                         else

                            //spaces
                             printf(" ");

                     }

                //move to the next row
                printf("\n");

                k++;

             }

}