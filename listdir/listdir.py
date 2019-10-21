import argparse
import os
import csv
import hashlib
import zipfile
import configparser
import json
from . import logger
from datetime import datetime

logger = logger.ini_logger(__name__)


def ini_arguments():
    """
    Initialize and read arguments.

    :return: Parsed arguments.
    """
    logger.info("Initializing arguments")
    config = configparser.ConfigParser()
    config_dir = os.path.dirname(__file__)
    config.read(config_dir + f"{os.sep}config.ini")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Directory for file listing.", nargs="?",
                        default=config["default"]["path"])
    parser.add_argument("filename", help="Name of the output file.", nargs="?",
                        default=config["default"]["output_file"])
    parser.add_argument("-n", "--nonrecursive", action="store_true", help="Lists files non-recursively.")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON instead of CSV.")
    logger.info("Initializing arguments")
    return parser.parse_args()


def create_output(filename, path, nonrecursive, output_json):
    """
    Create an output(CSV/JSON) file containing a list of files inside the path.

    :param filename: Output filename.
    :param path: Path to be checked for files.
    :param nonrecursive: Whether to check subdirectories or not.
    :param output_json: Output JSON file instead of CSV file.
    :return:
    """
    logger.info("Creating output file")
    abs_path = os.path.abspath(path)
    if output_json:
        with open(filename, "w+") as output_file:
            logger.info("Writing to JSON file")
            json.dump(listdir(abs_path, nonrecursive), output_file, indent=4)
            logger.info("Writing to JSON file")
    else:
        with open(filename, "w+", newline='') as csv_file:
            logger.info("Writing to CSV file")
            writer = csv.DictWriter(csv_file, ["parent path", "file name", "file size", "md5", "sha1"], delimiter=',')
            writer.writeheader()
            writer.writerows(listdir(abs_path, nonrecursive).values())
            logger.info(f"Finished writing to CSV file: {filename}")


def listdir(directory, nonrecursive):
    """
    Return a list of each file in a directory.

    :param directory: Directory to be checked for file listing.
    :param nonrecursive: List files non-recursively if True.
    :return: Dictionary containing a list of each file in a directory.
    """
    csv_output = {}
    keys = ["parent path", "file name", "file size", "md5", "sha1"]

    try:
        file_list = os.listdir(directory)
    except Exception as e:
        logger.error("Exception occurred. Skipping directory", exc_info=True)
        return ["error", "error"]

    for file in file_list:
        logger.debug(f"Listing files in directory: {directory}")
        file_path = f"{directory}{os.sep}{file}"

        if os.path.isfile(file_path):
            row = output_row(directory, file, file_path)
            csv_output[file] = dict(zip(keys, row))
        elif not nonrecursive:
            csv_output.update(listdir(file_path, nonrecursive))

    return csv_output


def output_row(directory, file, file_path):
    """
    Return a list of five values, namely, directory, file, size, md5, and sha1.

    :param directory: Parent directory of the file.
    :param file: File name.
    :param file_path: Full path of the file.
    :return: Directory, file, size, md5, and sha1.
    """
    hashes = get_hash(file_path)
    row = directory, file, os.stat(file_path).st_size, hashes[0], hashes[1]
    logger.debug(f"{row}")
    return row


def get_hash(file_path):
    """
    Return md5 and sha1 hashes of the file.

    :param file_path: Full path of the file.
    :return: md5 and sha1 hashes of the file.
    """
    block_size = 65536
    md5_hasher = hashlib.md5()
    sha1_hasher = hashlib.sha1()
    logger.debug(f"Getting hashes of {file_path}")

    try:
        with open(file_path, 'rb') as f:
            block = f.read(block_size)
            while len(block) > 0:
                md5_hasher.update(block)
                sha1_hasher.update(block)
                block = f.read(block_size)
    except Exception as e:
        logger.error("Cannot open file")
        return "Error", "Error"

    return md5_hasher.hexdigest(), sha1_hasher.hexdigest()


def zip_output(filename, del_original):
    """
    Creates a zip file out of the input file.

    :param filename: Name of the file
    :return: none
    """
    with zipfile.ZipFile(f"{filename}.zip", "w", zipfile.ZIP_DEFLATED) as zip_file:
        logger.info("Writing to ZIP file")
        zip_file.write(filename)
        logger.info(f"Finished writing to ZIP file: {filename}.zip")

    if del_original:
        os.remove(filename)


def main():
    args = ini_arguments()
    final_filename = f"[{datetime.now().strftime('%m%d%y-%H%M')}]{args.filename}"
    create_output(final_filename, args.path, args.nonrecursive, args.json)
    zip_output(final_filename, True)


if __name__ == "__main__":
    main()
