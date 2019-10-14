import argparse
import os
import csv


def listdir(directory, nonrecursive):
    """
    Return a string containing a list of each file in a directory. Uses CSV format.

    :param directory: Directory to be checked for file listing.
    :param nonrecursive: List files recursively if True.
    :return: String containing a list of each file in a directory.
    """
    csv_output = []
    file_list = os.listdir(directory)

    for file in file_list:
        file_path = f"{directory}/{file}"
        if os.path.isfile(file_path):
            csv_output.append((directory, file, os.stat(file_path).st_size))
        elif not nonrecursive:
            csv_output += listdir(file_path, nonrecursive)

    return csv_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory for file listing.")
    parser.add_argument("filename", help="Name of the csv file output.")
    parser.add_argument("-n", "--nonrecursive", action="store_true", help="Lists files non-recursively.")
    args = parser.parse_args()

    with open(f"{args.filename}.csv", "w+", newline='') as csv_file:
        abs_path = os.path.abspath(args.path)
        csv_file.write("parent path,filename,file size\n")
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(listdir(abs_path, args.nonrecursive))
