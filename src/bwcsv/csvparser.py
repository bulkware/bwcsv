# !/usr/bin/env python3

"""CSV-file loading support."""

# Imports
import csv
import os

# A class to handle CSV files
class CSVParser(object):

    # Initialization
    def __init__(self):

        # Declare class variables
        self.columncount = 0 # CSV file column count
        self.filedata = [] # List for file data
        self.message = "" # Error/success message
        self.rowcount = 0 # CSV file row count
        self.success = False # Successful file open


    # A method to load CSV file
    def load_file(self, file, fieldseparator=",", textdelimiter='"'):

        # Set the file opened to false
        self.success = False

        # Check if file path is None
        if not file:
            self.message = "Error: no file."
            return False

        # Check if file path is not empty
        if file == "":
            self.message = "Error: filename is empty."
            return False

        # Extension check
        ext = file.lower()
        if not ext.endswith(".csv"):
            self.message = "Error: invalid file extension."
            return False

        # Check if file exists
        if not os.path.exists(file):
            self.message = "Error: file does not exist."
            return False

        # Check if path is an existing regular file
        if not os.path.isfile(file):
            self.message = "Error: not a file."
            return False

        # Try to load CSV file
        try:

            # Clear list
            self.filedata = []

            # Read the CSV once so malformed rows can be rejected consistently.
            with open(file, "r", encoding="utf-8-sig", newline="") as filehandle:
                csvfile = csv.reader(
                    filehandle, delimiter=fieldseparator, quotechar=textdelimiter
                )
                self.filedata = list(csvfile)

            if not self.filedata:
                self.message = "Error: CSV file is empty."
                return False

            self.columncount = len(self.filedata[0])
            if any(len(line) != self.columncount for line in self.filedata):
                self.message = "Error: CSV rows do not have a consistent number of columns."
                self.filedata = []
                return False

            self.rowcount = len(self.filedata)

            # Successful file open
            self.success = True

        except OSError as e:
            self.message = "I/O error({0}): {1}".format(e.errno, e.strerror)

        except (csv.Error, TypeError, UnicodeError):
            self.message = "Error: unable to open file."

        if self.success:
            self.message = "File opened successfully."
            return True

        return False
