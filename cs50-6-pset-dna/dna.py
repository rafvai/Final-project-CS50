import csv
import sys

def main():
    # TODO: Check for command-line usage
    # Accept only 2 CLA
    if len(sys.argv) != 3:
        print("Prompt only csv file and STR")
        exit()

    # TODO: Read database file into a variable
    # opening the first CLA to be read
    with open(sys.argv[1]) as file:
        # read into reader the file we previously opened
        reader = csv.DictReader(file)
        # save the sequence's names we want to compare later in a list
        field_names = reader.fieldnames
        database = {}
        # loop through the csv file
        for row in reader:
            # pop out the field name
            name = row.pop('name')
            # assign the name to each row
            database[name] = row
    # TODO: Read DNA sequence file into a variable
    # open the second CLA to be read
    with open(sys.argv[2]) as f:
        dna = f.read()
    #create a dict to store name of the subsequences and their frecuencies
    longest = {}
    # TODO: Find longest match of each STR in DNA sequence
    for field_name in field_names[1:]:
        # assign the frecuency of a subsequence into the corresponding field in the dict
        longest[field_name] = longest_match(dna, field_name)
    # TODO: Check database for matching profiles
    # compare each subsequence frecuency with the values of the file read
    for name in database:
        counter = 0
        for field_name in longest:
            if longest[field_name] == int(database[name][field_name]):
                if counter == len(field_names) - 2:
                    print(f"{name}")
                    exit()
                counter += 1
                continue
            else:
                break
    print("No match")
    return

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run
main()
