#include <cs50.h>
#include <stdio.h>

int main(void)

{
    // the variable i want from the user
    int n;
//do while loop to obtain a number between 1 & 8
    do
    {
    n= get_int("Height: ");
    }
    while (n<1 || n>8);

//create rows
    for(int i=0; i<n; i++)
   {
    // columns
      for (int j = 0; j < n; j++)
      {
        //create blocks and spaces
         if((i + j)>=(n - 1))

            printf("#");
         else

            printf(" ");
       }
        //move to the next row
        printf("\n");
    }
}