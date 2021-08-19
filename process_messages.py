import time
from message_objects import PidObject
from outputs import tabulate_all_message_lines, tabulate_pid_change_message_lines, print_to_file


def process_messages(line_data):
    host_list = []
    for entry in line_data:  # find hosts
        if not len(host_list) < 2:  # assuming only 2 hosts
            break
        else:
            if not line_data[entry].host in host_list:
                host_list.append(line_data[entry].host)

    app_list = []
    for entry in line_data:  # find apps
        if not len(app_list) < 3:  # assuming only 3 apps
            break
        else:
            if not line_data[entry].app in app_list:
                app_list.append(line_data[entry].app)

    # Separate the messages by host
    pid_change_message_lines = []
    for host in host_list:
        all_message_lines = []
        pids = {}
        for app in app_list:
            pids[app] = None

        messages = {}
        for entry in line_data:
            if line_data[entry].host != host:
                continue
            else:
                all_message_lines.append([line_data[entry].line,
                                   line_data[entry].time,
                                   line_data[entry].host,
                                   line_data[entry].app,
                                   line_data[entry].pid,
                                   line_data[entry].thread])

                if pids[line_data[entry].app] == line_data[entry].pid:  # if the PID for that app has NOT changed
                    messages[line_data[entry].pid].last = line_data[
                        entry].time  # time of last occurrence updated to current entry
                else:  # if the PID for that app HAS changed
                    messages[line_data[entry].pid] = PidObject(line_data[entry].line,
                                                               line_data[entry].host,
                                                               line_data[entry].pid,
                                                               line_data[entry].app,
                                                               line_data[entry].time,
                                                               line_data[entry].time,
                                                               line_data[entry].thread,
                                                               line_data[entry].body)
                    pids[line_data[entry].app] = line_data[entry].pid

        print("\n", tabulate_all_message_lines(all_message_lines), "\n")

        for entry in messages:
            pid_change_message_lines.append([messages[entry].line,
                                             messages[entry].host,
                                             messages[entry].pid,
                                             messages[entry].thread,
                                             messages[entry].app,
                                             messages[entry].first,
                                             messages[entry].last,
                                             messages[entry].body])

        message_lines_table = tabulate_pid_change_message_lines(pid_change_message_lines, host)
        print("Host: ", host, message_lines_table, "\n")

        file_name = "Log_Messages_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
        print_to_file(message_lines_table, file_name)
