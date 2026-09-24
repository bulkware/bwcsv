# bwCSV

A lightweight desktop application to view CSV files.


## What are CSV-files?

A CSV-file would look something like this:

"One","Two","Three"
"Four","Five","Six"
"Seven","Eight","Nine"

[Wikipedia page](http://en.wikipedia.org/wiki/Comma-separated_values)


## Getting started

Open a file using the menu commands. File will be displayed on an Excel-like grid. You can use the
search to locate specific strings from the open file.


## Menu commands

### File > Open...
Opens a CSV-file.

### File > Quit
Quits the application.

### Settings > Field separator...
Set the field separator to use when opening CSV-files. Field separator is the character that
separates fields in CSV-files. The default is comma. Required.

### Settings > Text delimiter...
Set the text delimiter to use when opening CSV-files. Text delimiter is the character that is used
to surround the field in CSV-files. The default is double-quote. Not required.

### Settings > Horizontal header
Enable/disable horizontal header of table.

### Settings > Vertical header
Enable/disable vertical header of table.

### Settings > Set header labels from first line
When enabled, the first line of CSV-file is used as labels for table.

### Help > About...
Application information.


## Running from source

Install the project and its Python dependency:

`python3 -m pip install -e .`

Then run the application from a checkout:

`PYTHONPATH=src python3 -m bwcsv.main path/to/file.csv`

## Packages and releases

The project builds native packages from the same source metadata:

- Debian package: `make install-deb && make deb` (Debian/Ubuntu)
- RPM package: `make install-rpm && make rpm` (Fedora/RHEL)
- Windows MSI and portable ZIP: `make windows` on Windows

Native package builds require their platform's build dependencies. Windows builds use cx_Freeze and
produce an MSI plus a folder-based portable ZIP.

GitHub Actions builds unsigned Windows, Debian, and RPM artifacts for matching version tags. Future
SignPath integration will sign the Windows artifacts only.
See [the code signing policy template](docs/CODE_SIGNING_POLICY.md).

## Development

`make test` runs display-free parser and packaging-metadata tests. The Qt form is generated from
`src/bwcsv/mainwindow.ui`; run `scripts/generate-ui.sh` after editing it.
