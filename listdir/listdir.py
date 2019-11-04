import argparse
import os
import csv
import hashlib
import zipfile
import configparser
import json
import db_manager
import logger
from datetime import datetime

logger = logger.ini_logger(__name__)


def ini_arguments():
    """
    Initialize and read arguments.

    :return: Parsed arguments.
    """
    config = configparser.ConfigParser()
    config_dir = os.path.abspath(os.path.dirname(__file__))
    config.read(config_dir + f"{os.sep}config.ini")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Directory for file listing.", nargs="?",
                        default=config["default"]["path"])
    parser.add_argument("filename", help="Name of the output file.", nargs="?",
                        default=config["default"]["output_file"])
    output_type = parser.add_mutually_exclusive_group(required=True)
    output_type.add_argument("-c", "--csv", action="store_true", help="Output in CSV.")
    output_type.add_argument("-j", "--json", action="store_true", help="Output in JSON.")
    output_type.add_argument("-s", "--sql", action="store_true", help="Output to a database.")
    return parser.parse_args(), config


def create_output(filename, abs_path, output_type):
    """
    Create an output(CSV/JSON/PostgreSQL) containing a list of files inside the path.

    :param filename: Output filename.
    :param abs_path: Path to be checked for files.
    :param output_type: Output type of the file list.
    :return:
    """
    logger.info("Creating output file")
    if output_type is 'j':
        with open(filename, "w+") as output_file:
            logger.info("Writing to JSON file")
            json.dump(listdir(abs_path), output_file, indent=4)
            logger.info("Writing to JSON file")
    elif output_type is 'c':
        with open(filename, "w+", newline='') as csv_file:
            logger.info("Writing to CSV file")
            writer = csv.DictWriter(csv_file, ["parent path", "file name", "file size", "md5", "sha1"], delimiter=',')
            writer.writeheader()
            writer.writerows(listdir(abs_path).values())
            logger.info(f"Finished writing to CSV file: {filename}")


def listdir(directory):
    """
    Return a list of each file in a directory.

    :param directory: Directory to be checked for file listing.
    :return: Dictionary containing a list of each file in a directory.
    """
    csv_output = {}
    keys = ["parent_path", "file_name", "file_size", "md5", "sha1"]

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
        else:
            csv_output.update(listdir(file_path))

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
    final_filename = f"({datetime.now().strftime('%m%d%y-%H%M')}){args[0].filename}"
    abs_path = os.path.abspath(args[0].path)

    if args[0].json:
        create_output(final_filename, abs_path, 'j')
        zip_output(final_filename, True)
    elif args[0].csv:
        create_output(final_filename, abs_path, 'c')
        zip_output(final_filename, True)
    elif args[0].sql:
        db_manager.write_to_db(listdir(abs_path).values(), args[1]['database']['username'],
                               args[1]['database']['hostname'])


if __name__ == "__main__":
    main()

