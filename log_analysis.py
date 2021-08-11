import argparse

from tabulate import tabulate

from gather_data import gather_data


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
    line_data = gather_data(file_path)

    headers_list = ["Thread", "Host", "App", "PID", "Thread"]
    table_list = []
    for entry in line_data:
        table_list.append([entry, line_data[entry].time, line_data[entry].host, line_data[entry].app, line_data[entry].pid, line_data[entry].thread])

    print("\n", tabulate(table_list, headers=headers_list, sort="Host"),
          "\n")  # Print out the pretty table


if __name__ == '__main__':
    main()
