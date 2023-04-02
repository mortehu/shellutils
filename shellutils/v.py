#!/bin/env python3

import os
import sys
import argparse
import subprocess

def find_files(filename, start_dir="."):
    found_files = []
    queue = [(start_dir, 0)]

    while queue:
        current_dir, depth = queue.pop(0)
        found = False

        for entry in os.scandir(current_dir):
            if entry.is_dir():
                queue.append((entry.path, depth + 1))
            elif entry.name.startswith(filename):
                found_files.append((entry.path, depth))
                found = True

        if found_files and not found:
            break

    return found_files

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Find and edit a file with the specified name.")
    parser.add_argument("filename", help="The name of the file to search and edit.")
    parser.add_argument("--complete", action="store_true", help="Output filenames for completion.")
    parsed_args = parser.parse_args(args)

    filename = parsed_args.filename
    found_files = find_files(filename)

    if parsed_args.complete:
        for path, _ in found_files:
            print(path)
    else:
        if len(found_files) == 1:
            editor = os.environ.get("EDITOR", "vi")
            subprocess.run([editor, found_files[0][0]])
        elif len(found_files) == 0:
            print("No files found with the specified name.", file=sys.stderr)
            sys.exit(1)
        else:
            print("Multiple files found at the same depth:", file=sys.stderr)
            for path, _ in found_files:
                print(path, file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
