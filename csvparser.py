#!/usr/bin/python
# -*- coding: utf-8 -*-

""" A class to handle CSV-files. """

# Imports
import csv # CSV File Reading and Writing
import os # Miscellaneous operating system interfaces

# A class to handle CSV-files
class CSVParser(object):

    # Initialization
    def __init__(self):

        # Declare class variables
        self.columncount = 0 # CSV-file column count
        self.filedata = [] # List for file data
        self.message = "" # Error/success message
        self.rowcount = 0 # CSV-file row count
        self.success = False # Successful file open


    # A method to load csv-file
    def load_file(self, filepath, fieldseparator=",", textdelimiter='"'):

        # Set the file opened to false
        self.success = False

        # Check if file path is not empty
        if filepath == "":
            self.message = "Error: filename is empty."
            return(False)

        # Check if file exists
        if not os.path.exists(filepath):
            self.message = "Error: file does not exist."
            return(False)

        # Check if path is an existing regular file
        if not os.path.isfile(filepath):
            self.message = "Error: not a file."
            return(False)

        # Extension check
        if not filepath.lower().endswith(".csv"):
            self.message = "Error: invalid file extension."
            return(False)

        # Try to load .csv-file
        try:

            # Clear list
            self.filedata = []

            # Create a file handle and open file using csv.reader
            filehandle = open(filepath, "r")
            csvfile = csv.reader(filehandle, delimiter=fieldseparator,
                quotechar=textdelimiter)

            # Count the number of columns
            self.columncount = len(next(csvfile))

            # Return position to zero
            filehandle.seek(0)

            # Loop lines and append them into a list
            for line in csvfile:
                listline = []
                for i in range(self.columncount):
                    listline.append(line[i])

                self.filedata.append(listline)
                del(listline)

            # Count the number of rows
            self.rowcount = sum(1 for line in self.filedata)

            # Discard variables
            del(csvfile)

            # Close file handle
            if filehandle:
                filehandle.close()

            # Successful file open
            self.success = True

        except IOError as e:
            self.message = "I/O error({0}): {1}".format(e.errno, e.strerror)

        except:
            self.message = "Error: unable to open file."

        finally:

            if self.success:
                self.message = "File opened successfully."
                return(True)
            else:
                return(False)
