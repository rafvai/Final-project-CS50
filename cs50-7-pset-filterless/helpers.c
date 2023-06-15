#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //loop through each row
    for (int i = 0; i < height; i++)
    {
        //loop through each column
        for (int j = 0; j < width; j++)
        {
            //find the average value of the 3 colors
            int x = (int) round ((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / (float)3);

            //assign the average value to each color
            image[i][j].rgbtRed = x;

            image[i][j].rgbtGreen = x;

            image[i][j].rgbtBlue = x;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //loop through each row
    for (int i = 0; i < height; i++)
    {
        //loop through each column
        for (int j = 0; j < width; j++)
        {
            //cretaing the sepiared colour
            int sepiared = (int) round (image[i][j].rgbtRed * 0.393 + image[i][j].rgbtGreen * 0.769 + image[i][j].rgbtBlue * 0.189);

            //creating the sepiagreen colour
            int sepiagreen = (int) round (image[i][j].rgbtRed * 0.349 + image[i][j].rgbtGreen * 0.686 + image[i][j].rgbtBlue * 0.168);

            //creating sepiablue
            int sepiablue = (int) round (image[i][j].rgbtRed * 0.272 + image[i][j].rgbtGreen * 0.534 + image[i][j].rgbtBlue * 0.131);

            //if it's bigger than 255 set to 255
            if (sepiared > 255)
            {
                sepiared = 255;
            }

            if (sepiagreen > 255)
            {
                sepiagreen = 255;
            }

            if (sepiablue > 255)
            {
                sepiablue = 255;
            }

            //apply sepia effect
            image[i][j].rgbtRed = sepiared;

            image[i][j].rgbtGreen = sepiagreen;

            image[i][j].rgbtBlue = sepiablue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;

    //loop through each row
    for (int i = 0; i < height; i++)
    {
        //loop through each pixel
        for (int j = 0; j < width / 2; j++)
        {
            int k = width - j - 1;

            //storing values into temp variables
            temp = image[i][j];

            //swap 1
            image[i][j] = image[i][k];

            //swap 2
            image[i][k] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //creating copy image
    RGBTRIPLE copy[height][width];

    float sumred = 0;

    float sumgreen = 0;

    float sumblue = 0;

    int count = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //creating a copy 2d array
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //loop through pixels in the adjacent rows
            for (int k = i - 1; k < i + 2; k++)
            {
                //loop through pixels in the adjacent columns
                for (int z = j - 1; z < j + 2; z++)
                {
                    if (k < height && k >= 0)
                    {
                        if (z < width && z >= 0)
                        {
                            count ++;

                            sumred += image[k][z].rgbtRed;

                            sumgreen += image[k][z].rgbtGreen;

                            sumblue += image[k][z].rgbtBlue;
                        }
                    }
                }
            }
            //assign the average score color to copy array
            copy[i][j].rgbtRed = (int) round(sumred / (float)count);

            copy[i][j].rgbtGreen = (int) round(sumgreen / (float)count);

            copy[i][j].rgbtBlue = (int) round(sumblue / (float)count);

            //set count to 0
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
