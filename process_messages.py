import time
import datetime
from message_objects import PidObject
from outputs import tabulate_all_message_lines, tabulate_pid_change_message_lines, print_to_file


def process_messages(line_data):
    all_message_lines = []
    pid_change_message_lines = []
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
    for host in host_list:
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
                                          line_data[entry].thread,
                                          line_data[entry].body])

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

        first = None
        last = None
        pid = None
        group = []
        for entry in messages:
            if pid is None:
                pid = messages[entry].pid
            if first is None:
                first = messages[entry].first
            if last is None:
                last = messages[entry].last

            if (messages[entry].pid - 3) <= pid <= (messages[entry].pid + 3):  # Talking about the same group
                # Could also judge by start time but the ranges on that were less reliable
                group.append(messages[entry])
            else:  # Not talking about the same group
                group.clear()
                pid = messages[entry].pid
                first = messages[entry].first
                last = messages[entry].last

            if len(group) == 3:
                minimum = min(item.last for item in group)
                last_range = max(item.last for item in group) - minimum
                if last_range > datetime.timedelta(minutes=1):  # If the lines don't all die within the same minute
                    for item in group:
                        if item.last == minimum:  # If that one is the first to die
                            # then keep it
                            pid_change_message_lines.append([item.line,
                                                             item.host,
                                                             item.pid,
                                                             item.app,
                                                             item.first,
                                                             item.last,
                                                             item.thread,
                                                             item.body])
                first, last, pid = None, None, None
                group.clear()










        # message_lines_table = tabulate_pid_change_message_lines(pid_change_message_lines, host)
        # print("Host: ", host)
        # print(message_lines_table, "\n")

    # print("\n", tabulate_all_message_lines(all_message_lines), "\n")

    file_name = "Log_Entries_by_Host_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    test = tabulate_all_message_lines(all_message_lines)
    print_to_file(test, file_name)

    file_name = "Failing_Messages_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
    print_to_file(tabulate_pid_change_message_lines(pid_change_message_lines), file_name)
