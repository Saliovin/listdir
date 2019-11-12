# listdir

## What is it?
This is a Python program that creates list of files in a directory. Can output to a CSV file, JSON file, database, 
or queue

## Requirements
- [Python 3](https://www.python.org/downloads/)

## How to use?
```
listdir.py [-h] (-c | -j | -s | -q) [path] [filename]
```

## Arguments
```
positional arguments:
  path        Directory for file listing.
  filename    Name of the output file.

optional arguments:
  -h, --help  show this help message and exit
  -c, --csv   Output in CSV.
  -j, --json  Output in JSON.
  -s, --sql   Output to a database.
  -q, --queue Output to a queue
```

## How To Test
Open terminal inside the tests directory
```
pytest --cov
```

## Example
List all the files in /etc and post it to a database
```
python listdir.py /etc -s
```
