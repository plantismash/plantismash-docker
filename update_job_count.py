#!/bin/python3

from shutil import copy
from requests import get
from argparse import ArgumentParser
from pathlib import Path
from json import loads


def prompt():
    print("Continue? [y/n]")
    answer = input()
    if answer.lower() != "y":
        print("Aborting")
        exit(0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--url", "-u", type=str)
    parser.add_argument("--settings-file", "-s", type=Path)
    parser.add_argument("--prompt", "-p", type=bool, default=True)
    args = parser.parse_args()

    # get current job count
    response = get("https://plantismash.bioinformatics.nl/server_status")

    if response.status_code != 200:
        print(
            f"HTTP Error: {response.status_code} when trying to get job count from plantismash server"
        )
        print("The old count was not upated")
        exit(1)

    parsed = loads(response.text)

    new_job_count = parsed["total_jobs"]

    print(f"Found new job count: {new_job_count}")

    old_lines = []
    old_job_count = 0

    with open(args.settings_file, "r") as f:
        for line in f:
            old_lines.append(line)
            if not line.startswith("OLD_JOB_COUNT"):
                continue

            old_job_count = int(line.split("=")[1].strip())

    if old_job_count == 0:
        print("Could not find old job count in settings file")
        print("The old count was not updated")
        exit(1)

    print(f"Found old job count: {old_job_count}")

    if old_job_count == new_job_count:
        print("Old job count is the same as new job count")
        prompt()

    # copy old file as backup
    if args.prompt:
        print(f"Copying {args.settings_file} to {args.settings_file}.bak")
        prompt()

    copy(args.settings_file, args.settings_file.with_suffix(".bak"))

    if args.prompt:
        print(
            f"Replacing old job count ({old_job_count}) with new job count ({new_job_count})"
        )
        prompt()

    # update old job count
    with open(args.settings_file, "w") as f:
        for line in old_lines:
            if line.startswith("OLD_JOB_COUNT"):
                f.write(f"OLD_JOB_COUNT = {new_job_count}\n")
            else:
                f.write(line)
