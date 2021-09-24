import os

from tabulate import tabulate
from io import open


def tabulate_all_message_lines(all_message_lines):
    headers_list = ["Line", "Time", "Host", "App", "PID", "Thread", "Body"]
    return tabulate(all_message_lines, headers=headers_list)


def tabulate_pid_change_message_lines(pid_change_message_lines):
    headers_list = ["Line", "Host", "PID", "App", "First", "Last", "Thread", "Body"]
    return tabulate(pid_change_message_lines, headers=headers_list)


def print_to_file(file_content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(file_content)


def output_individual_failed_messages(pid_change_message_lines_item, now):
    item = pid_change_message_lines_item
    message = "Line: " + str(item.hang_line) \
              + "\nHost: " + str(item.host) \
              + "\nPID: " + str(item.pid) \
              + "\nApp: " + str(item.app) \
              + "\nFirst: " + str(item.first) \
              + "\nLast: " + str(item.last) \
              + "\nThread: " + str(item.thread) \
              + "\nBody: " + str(item.hang_body)
    line_file_name = str(item.hang_line) + "_" + str(item.host) + "_" + str(item.pid) + "_" + str(item.thread) + "_" + now + ".txt"
    print_to_file(unicode(message), line_file_name)


def output_compiled_message_data(all_message_lines, pid_change_message_lines, folder_path, now):
    os.chdir(folder_path)  # Move back to original file path

    # Print data for all log entries as one file
    file_name = "Log_Entries_by_Host_" + now + ".txt"
    print_to_file(tabulate_all_message_lines(all_message_lines), file_name)

    # Print failing messages as one file
    file_name = "Failing_Messages_" + now + ".txt"
    print_to_file(tabulate_pid_change_message_lines(pid_change_message_lines), file_name)
