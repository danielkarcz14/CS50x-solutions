import csv
import sys
import os


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("python dna.py FILENAME1 FILENAME2")
    # check file extensions
    check_file_type()

    # TODO: Read database file into a variable
    with open(sys.argv[1]) as database:
        reader = csv.reader(database)
        data = []
        for row in reader:
            data.append(row)
    STR = []
    STR = data[0]
    STR.pop(0)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as sequence:
        dna = sequence.read()

    # TODO: Find longest match of each STR in DNA sequence
    sq_dict = {}
    for i in STR:
        if i in sq_dict:
            sq_dict[i].append(longest_match(dna, i))
        else:
            sq_dict[i] = longest_match(dna, i)
    # print(sq_dict)

    # TODO: Check database for matching profiles
    with open(sys.argv[1]) as check:
        reader = csv.DictReader(check)
        for row in reader:
            match = True
            for key, value in sq_dict.items():
                if key != "name" and int(row[key]) != value:
                    match = False
                    break
            if match:
                print(row["name"])
                break

        if match == False:
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


def check_file_type():
    file_1 = os.path.splitext(sys.argv[1])[1]
    file_2 = os.path.splitext(sys.argv[2])[1]
    if file_1 != ".csv" or file_2 != ".txt":
        sys.exit("python dna.py FILENAME.csv FILENAME.txt")



if __name__ == "__main__":
    main()
