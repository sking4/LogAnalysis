from tabulate import tabulate


def tabulate_all_message_lines(all_message_lines):
    headers_list = ["Line", "Time", "Host", "App", "PID", "Thread", "Body"]
    return tabulate(all_message_lines, headers=headers_list)


def tabulate_pid_change_message_lines(pid_change_message_lines):
    headers_list = ["Line", "Host", "PID", "App", "First", "Last", "Thread", "Body"]
    return tabulate(pid_change_message_lines, headers=headers_list)


def print_to_file(file_content, file_name):
    with open(file_name, 'w', encoding="utf-8") as f:
        print(file_content, file_name, file=f)
