# SAM Password Reuse Checker

This Python script helps to identify local admin password reuse in an Active Directory environment. It searches through SAM dump files produced by Impacket's secretsdump.py and identifies hash duplicates, which indicate reused passwords.

## Features

- Searches all .sam files in a given directory
- Supports a blacklist to exclude specific usernames
- Optional output to an Excel file
- Optional hash sanitization for Excel output

## Requirements

- Python 3.7 or above
- pandas library (`pip install pandas`)
- openpyxl library (`pip install openpyxl`)

## Usage

```bash
python SAMPasswordReuseChecker.py [directory] -b [blacklist_file] -e [excel_file] -s
```

### Arguments

- `directory`: (Required) The directory where the .sam files are located.
- `-b` / `--blacklist`: (Optional) A file containing usernames to exclude from the check. One username per line.
- `-e` / `--excel`: (Optional) If provided, results will be written to this Excel file. Please don't include the extension, .xlsx will be added automatically.
- `-s` /`--sanitize`: (Optional) If used, hashes in the Excel output will be partially obscured for privacy.

## Examples

Check for duplicate hashes in .sam files in the current directory and write results to `results.xlsx`, obscuring the hashes:

```bash
python SAMPasswordReuseChecker.py . -e results -s
```

Check for duplicate hashes in .sam files in the dumps directory, excluding usernames listed in `blacklist.txt`:

```bash
python SAMPasswordReuseChecker.py dumps -b blacklist.txt
```

## Note

This tool is meant to be used for legal purposes only. It is the user's responsibility to comply with all applicable laws.