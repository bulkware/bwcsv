#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python imports
import re # Regular expression operations

# A function to find strings
def find_string(search, subject, ignorecase=False, wholeword=False):
    """ A function to find a string from another string. Complete with ignore
        text case and whole word search. """

    # Search or subject cannot be empty
    if search == "" or subject == "":
        return(False)

    # Escape search string
    search = re.escape(search)

    # Add word boundaries if using whole word search
    if wholeword:
        search = r"\b" + search + r"\b"

    # Search using regular expressions
    if ignorecase:
        if re.search(search, subject, re.IGNORECASE):
            return(True)
    else:
        if re.search(search, subject):
            return(True)

    # Not found
    return(False)
