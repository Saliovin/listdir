# listdir

## What is it?
This is a Python program that creates list of files in a directory and outputs it to a csv file.

## Requirements
- [Python 3](https://www.python.org/downloads/)

## How to use?
```
python listdir.py [-h] [-r] path filename
```

## Arguments
```
positional arguments:
  path             Directory for file listing.
  filename         Name of the csv file output.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Lists files recursively.
```

## Example
List all the files in /etc including subdirectories and output it to etc_output.csv
```
python listdir.py /etc etc_output -r
```
