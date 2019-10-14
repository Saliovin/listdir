import argparse
import os
import csv
import hashlib
import zipfile


def listdir(directory, nonrecursive):
    """
    Return a string containing a list of each file in a directory. Uses CSV format.

    :param directory: Directory to be checked for file listing.
    :param nonrecursive: List files non-recursively if True.
    :return: String containing a list of each file in a directory.
    """
    csv_output = []
    file_list = os.listdir(directory)

    for file in file_list:
        file_path = f"{directory}/{file}"
        if os.path.isfile(file_path):
            csv_output.append(csv_row(directory, file, file_path))
        elif not nonrecursive:
            csv_output += listdir(file_path, nonrecursive)

    return csv_output


def csv_row(directory, file, file_path):
    """
    Return a list of five values, namely, directory, file, path, md5, and sha1.
    :param directory: Parent directory of the file.
    :param file: File name.
    :param file_path: Full path of the file.
    :return: Directory, file, path, md5, and sha1.
    """
    block_size = 65536
    md5_hasher = hashlib.md5()
    sha1_hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        block = f.read(block_size)
        while len(block) > 0:
            md5_hasher.update(block)
            sha1_hasher.update(block)
            block = f.read(block_size)

    return directory, file, os.stat(file_path).st_size, md5_hasher.hexdigest(), sha1_hasher.hexdigest()


def zip_output(filename):
    with zipfile.ZipFile(f"{filename}.zip", "w") as zip_file:
        zip_file.write(filename)

    os.remove(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory for file listing.")
    parser.add_argument("filename", help="Name of the csv file output.")
    parser.add_argument("-n", "--nonrecursive", action="store_true", help="Lists files non-recursively.")
    args = parser.parse_args()

    with open(args.filename, "w+", newline='') as csv_file:
        abs_path = os.path.abspath(args.path)
        csv_file.write("parent path,filename,file size, md5, sha1\n")
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(listdir(abs_path, args.nonrecursive))

    zip_output(args.filename)
