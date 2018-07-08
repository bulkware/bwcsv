# bwcsv

A lightweight application to view CSV files.


## What are CSV-files?

A CSV-file would look something like this:

"One","Two","Three"
"Four","Five","Six"
"Seven","Eight","Nine"

[Wikipedia page](http://en.wikipedia.org/wiki/Comma-separated_values)


## Getting started

Open a file using the menu commands. File will be displayed on an Excel-like
grid. You can use the search to locate specific strings from the open file.


## Menu commands

### File > Open...
Opens a CSV-file.

### File > Exit
Exits the application.

### Settings > Field separator...
Set the field separator to use when opening CSV-files. Field separator is the
character that separates fields in CSV-files. The default is comma. Required.

### Settings > Text delimiter...
Set the text delimiter to use when opening CSV-files. Text delimiter is the
character that is used to surround the field in CSV-files. The default is
double-quote. Not required.

### Settings > Horizontal header
Enable/disable horizontal header of table.

### Settings > Vertical header
Enable/disable vertical header of table.

### Settings > Set header labels from first line
When enabled, the first line of CSV-file is used as labels for table.

### Help > About...
Application information.


## Running on Linux

### Installing dependencies (Debian-based systems)
Open your terminal application and type:
`sudo apt-get install python3 python3-pyqt4`

Hit enter. Enter your password when prompted. Answer yes to the question about
using additional disk space.

### Downloading the source
git clone https://github.com/bulkware/bwcsv.git

### Running the application
You can run the application from the source code using this command:
`python3 main.py`
