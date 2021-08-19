from tabulate import tabulate


def tabulate_all_message_lines(all_message_lines):
    headers_list = ["Line", "Time", "Host", "App", "PID", "Thread"]
    return tabulate(all_message_lines, headers=headers_list)


def tabulate_pid_change_message_lines(pid_change_message_lines, host):
    headers_list = ["Line", "Host", "PID", "Thread", "App", "First", "Last", "Body"]

    return tabulate(pid_change_message_lines, headers=headers_list)


def print_to_file(file_content, file_name):
    with open(file_name, 'w') as f:
        print(file_content, file_name, file=f)
