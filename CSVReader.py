# My CSV reader class to read in csv files in Main.py with less code.
import csv


# Method takes in a file location then reads in csv file.
# Returns list of data from file.
# Space - O(N)       Time - O(N)
def read_csv_file_to_list(location):
    data = []
    with open(location) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for row in read_csv:
            data.append(row)
    return data
