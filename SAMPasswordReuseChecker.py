#!/usr/bin/python3
# Author: Dylan Evans (@fin3ss3g0d)
import os
import re
import argparse
import pandas as pd
from collections import Counter, defaultdict

def parse_args():
    parser = argparse.ArgumentParser(description='SAM Password Reuse Checker')
    parser.add_argument('directory', help='Directory containing .sam files.')
    parser.add_argument('-b', '--blacklist', help='Blacklist file with usernames to exclude.')
    parser.add_argument('-e', '--excel', help='Base name for Excel output file.')
    parser.add_argument('-s', '--sanitize', action='store_true', help='Sanitize hashes in Excel output.')
    return parser.parse_args()

def parse_sam_file(file_path, blacklist):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r'(.*):(.*):(.*):(.*):::', line)
            if match:
                username = match.group(1)
                hash = match.group(4)
                # Skip users on the blacklist.
                if username not in blacklist:
                    yield username, hash

def sanitize_hash(hash, sanitize):
    if sanitize:
        # Replace the middle part of the hash with asterisks.
        return hash[:5] + '*' * len(hash[5:-5]) + hash[-5:]
    else:
        return hash

def main():
    args = parse_args()
    counter = Counter()
    file_dict = defaultdict(list)
    blacklist = set()

    # Load the blacklist if it was provided.
    if args.blacklist:
        with open(args.blacklist, 'r') as f:
            blacklist = set(line.strip() for line in f)

    # Go through all the files in the specified directory.
    for filename in os.listdir(args.directory):
        if filename.endswith('.sam'):
            file_path = os.path.join(args.directory, filename)
            for username, hash in parse_sam_file(file_path, blacklist):
                counter[hash] += 1
                file_dict[hash].append((os.path.splitext(filename)[0], username))

    results = []
    # Print the hash, count, and the file names where it is found.
    for hash, count in counter.items():
        if count > 1:
            print(f"Hash: {hash}, Count: {count}")
            for file_name, username in file_dict[hash]:
                print(f"  {file_name}, Username: {username}")
                results.append({'Hash': sanitize_hash(hash, args.sanitize), 'Count': count, 'File': file_name, 'Username': username})

    # Save to Excel if required
    if args.excel:
        df = pd.DataFrame(results)
        df.to_excel(args.excel + '.xlsx', index=False)

if __name__ == "__main__":
    main()
