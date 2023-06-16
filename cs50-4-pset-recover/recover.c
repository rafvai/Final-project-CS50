#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // check if the namefile was specified
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // check if memory card is successfully opened
    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open file.\n");

        return 1;
    }

    //create vars that we gonna use and allocate memory for them
    FILE *img;

    char name[8];

    unsigned char *buffer = malloc(512);

    int count = 0;

    while (fread(buffer, BLOCK_SIZE, 1, input))
    {
        // new jpg file found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close previous jpg file if it exists
            if (count != 0)
            {
                fclose(img);
            }

            // create filename
            sprintf(name, "%03d.jpg", count);

            count++;

            // open new image file
            img = fopen(name, "w");

            // check if jpg file is successfully created
            if (img == NULL)
            {
                fclose(input);

                free(buffer);

                printf("Could not create output JPG.\n");

                return 3;
            }
        }

        //if any jpg file exists writes on the file currently opened
        if (count > 0)
        {
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    //frees memory and closes files
    fclose(img);

    fclose(input);

    free(buffer);

    return 0;
}