// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    //creating an array to store the header
    uint8_t header[HEADER_SIZE];

    //read the header
    fread (header, HEADER_SIZE, 1, input);

    //write in the file output
    fwrite (header, HEADER_SIZE, 1, output);

    // TODO: Read samples from input file and write updated data to output file
    //creating a buffer value to store samples
    int16_t buffer;

    //read the input file
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        //multiply by the factor
        buffer *= factor;

        //write into output file
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
