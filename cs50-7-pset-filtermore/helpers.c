#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average = 0;

    //loop through each row
    for (int i = 0; i < height; i++)
    {
        //loop through each pixel
        for (int j = 0; j < width; j++)
        {
            //calculating the average
            average = (int) round ((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            //swapping to gray scale
            image[i][j].rgbtRed = average;

            image[i][j].rgbtGreen = average;

            image[i][j].rgbtBlue = average;

            //set average to 0
            average = 0;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // creating temp
    RGBTRIPLE temp;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            //swap
            temp = image[i][j];

            image[i][j] = image[i][width - 1 - j];

            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int count = 0;

    int sumred = 0;

    int sumgreen = 0;

    int sumblue = 0;

    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int z = i - 1; z < i + 2; z++)
            {
                for (int k = j - 1; k < j + 2; k++)
                {
                    if (z >= 0 && z < height)
                    {
                        if (k >= 0 && k < width)
                        {
                            count++;

                            sumred += image[z][k].rgbtRed;

                            sumgreen += image[z][k].rgbtGreen;

                            sumblue += image[z][k].rgbtBlue;
                        }
                    }
                }
            }
            copy[i][j].rgbtRed = (int) round (sumred / (float)count);

            copy[i][j].rgbtGreen = (int) round (sumgreen / (float)count);

            copy[i][j].rgbtBlue = (int) round (sumblue / (float)count);

            count = 0;

            sumred = 0;

            sumgreen = 0;

            sumblue = 0;

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    //creating a 2d array for kernell formula
    int kergx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    int kergy[3][3] = {
         {-1, -2, -1},
         {0, 0, 0},
         {1, 2, 1}
    };

   //sobel variable: gx e gy together
   int  sobelred = 0;
   int  sobelgreen = 0;
   int  sobelblue = 0;

   //creating a copy array
   for (int i = 0; i < height; i++)
   {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    //looping through each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //colors' sum for vertical borders
            int sumbluegx = 0;
            int  sumgreengx = 0;
            int  sumredgx = 0;

            //colors' sum for horizontal borders
            int  sumbluegy = 0;
            int  sumgreengy = 0;
            int  sumredgy = 0;

            //loop in the 3x3 grid
            for (int k = -1; k < 2; k++)
            {
                for (int x = -1; x < 2; x++)
                {
                    if (i + k < 0 || i + k > height - 1 || j + x < 0 || j + x > width - 1)
                    {
                        continue;
                    }

                    //applying kernel formula for vertical borders
                    sumredgx += image[i + k][j + x].rgbtRed * kergx[k + 1][x + 1];
                    sumgreengx += image[i + k][j + x].rgbtGreen * kergx[k + 1][x + 1];
                    sumbluegx += image[i + k][j + x].rgbtBlue * kergx[k + 1][x + 1];

                    //applying kernel formula for horizontal borders
                    sumredgy += image[i + k][j + x].rgbtRed * kergy[k + 1][x + 1];
                    sumgreengy += image[i + k][j + x].rgbtGreen * kergy[k + 1][x + 1];
                    sumbluegy += image[i + k][j + x].rgbtBlue * kergy[k + 1][x + 1];
                }
            }

            //applying sobel formula
            sobelred = round(sqrt(pow(sumredgx,2) + pow(sumredgy,2)));
            sobelgreen = round(sqrt(pow(sumgreengx,2) + pow(sumgreengy,2)));
            sobelblue = round (sqrt(pow(sumbluegx,2) + pow(sumbluegy,2)));

            if (sobelred > 255)
            {
                sobelred = 255;
            }

            if (sobelgreen > 255)
            {
                sobelgreen = 255;
            }

            if (sobelblue > 255)
            {
                sobelblue = 255;
            }

            //assign the value into image's colors
            copy[i][j].rgbtRed = sobelred;
            copy[i][j].rgbtGreen = sobelgreen;
            copy[i][j].rgbtBlue = sobelblue;
        }
    }

     //copy the copy array into image array
     for (int i = 0; i < height; i++)
     {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
     }
    return;
}
