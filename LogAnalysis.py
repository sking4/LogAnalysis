# This is the main file for analyzing error logs. It finds hanging threads
# and outputs two files: one of all of the error lines, and one of the specific
# threads that cause the hangs and the full body of those error messages.

import argparse
from gather_data import gather_from_file, gather_by_host
from process_messages import process_messages


def collect_filename():
    parser = argparse.ArgumentParser(description='Process file name')
    parser.add_argument('file_path',
                        nargs='?',
                        type=str,
                        default=r"C:\Users\sking4\PycharmProjects\LogAnalysis\adc.log")
    p = parser.parse_args()
    file_path = p.file_path
    return file_path


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    line_data = gather_from_file(file_path)

    process_messages(line_data, file_path)


if __name__ == '__main__':
    main()
