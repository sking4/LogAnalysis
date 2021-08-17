import argparse
from tabulate import tabulate

from gather_data import gather_from_file, gather_by_host
from message_object import PidObject


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

    headers_list = ["Line", "Time", "Host", "App", "PID", "Thread"]

    host_list = []
    for entry in line_data: # find hosts
        if not len(host_list) < 2: # assuming only 2 hosts
            break
        else:
            if not line_data[entry].host in host_list:
                host_list.append(line_data[entry].host)

    app_list = []
    for entry in line_data: # find apps
        if not len(app_list) < 3: # assuming only 3 apps
            break
        else:
            if not line_data[entry].app in app_list:
                app_list.append(line_data[entry].app)

    for host in host_list:
        table_list = []
        pids = {}
        for app in app_list:
            pids[app] = None

        messages = {}
        for entry in line_data:
            if line_data[entry].host != host:
                continue
            else:
                table_list.append([line_data[entry].line, line_data[entry].time, line_data[entry].host, line_data[entry].app, line_data[entry].pid, line_data[entry].thread])
                app, pid, time, body = line_data[entry].app, line_data[entry].pid, line_data[entry].time, line_data[entry].body

                if pids[app] == pid:
                    messages[pid].last = time
                else:
                    messages[pid] = PidObject(pid, app, time, time, body)
                    pids[app] = pid

        print("\n", tabulate(table_list, headers=headers_list),
              "\n")  # Print out the pretty table

        messages_list = []
        for entry in messages:
            messages_list.append([messages[entry].pid, messages[entry].app, messages[entry].first, messages[entry].last, messages[entry].body])

        headers_list2 = ["PID", "App", "First", "Last", "Body"]
        print("\n", tabulate(messages_list, headers=headers_list2),
              "\n")  # Print out the pretty table


if __name__ == '__main__':
    main()
