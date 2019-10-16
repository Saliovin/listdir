import argparse
import os
import csv
import hashlib
import zipfile
import configparser
from datetime import datetime


def ini_arguments():
    """
    Initialize and read arguments.

    :return: Parsed arguments.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Directory for file listing.", nargs="?", default=config["default"]["path"])
    parser.add_argument("filename", help="Name of the csv file output.", nargs="?",
                        default=config["default"]["output_file"])
    parser.add_argument("-n", "--nonrecursive", action="store_true", help="Lists files non-recursively.")
    return parser.parse_args()


def create_csv(filename, path, nonrecursive):
    """
    Create a csv file containing a list of files inside the path.

    :param filename: Output filename.
    :param path: Path to be checked for files.
    :param nonrecursive: Whether to check subdirectories or not.
    :return:
    """
    with open(final_filename, "w+", newline='') as csv_file:
        abs_path = os.path.abspath(path)
        csv_file.write("parent path,filename,file size, md5, sha1\n")
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(listdir(abs_path, nonrecursive))


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
    hashes = get_hash(file_path)
    return directory, file, os.stat(file_path).st_size, hashes[0], hashes[1]


def get_hash(file_path):
    """
    Return md5 and sha1 hashes of the file.

    :param file_path: Full path of the file.
    :return: md5 and sha1 hashes of the file.
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

    return md5_hasher.hexdigest(), sha1_hasher.hexdigest()


def zip_output(filename):
    """
    Creates a zip file and out of the input file.

    :param filename: Name of the file
    :return: none
    """
    with zipfile.ZipFile(f"{filename}.zip", "w") as zip_file:
        zip_file.write(filename)

    os.remove(filename)


if __name__ == "__main__":
    args = ini_arguments()
    final_filename = f"{args.filename}[{datetime.now().strftime('%m%d%y-%H%M')}]"
    create_csv(final_filename, args.path, args.nonrecursive)
    zip_output(final_filename)
