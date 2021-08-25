from message_objects import LineObject, HostObject
import re
from datetime import datetime


def gather_by_host(lines):
    host_list = []
    for i in lines:  # for each message line
        found_host = False
        for hostObj in host_list:
            if lines[i].host == hostObj.getHost():
                hostObj.appendEntry(lines[i].line, lines[i].pid, lines[i].thread)
                found_host = True
                break
        if not found_host:
            host_list.append(HostObject(lines[i].host, [(lines[i].line, lines[i].pid, lines[i].thread)]))
    return host_list


def gather_from_file(file_path):
    lines = {}
    # Open file
    with open(str(file_path), encoding='ISO-8859-1') as my_file:
        # For each line in the file
        message_line = [False, 0]
        line_num = 0
        for line in my_file:
            line_num += 1

            # Check if the line being read is actually a line entry or part of a previous line due to parsing errors
            if re.match('^[0-9]{4}-$', line[:5]): # Just checking to see that the first part is the year and a dash, full date took too long
                message_line[0] = False
                # If line contains "IncomingApp"
                if "IncomingApp" in line:
                    # If line contains "Message.py 78 Incoming Message"
                    if "Message.py 78 Incoming Message" in line:
                        message_line = [True, line_num]
                        # Create an object with the line number as the identifier and add fields as attributes
                        pieces = line.split()
                        time = datetime.strptime(pieces[0], "%Y-%m-%dT%H:%M:%S")
                        host = pieces[2]
                        app = pieces[3][:pieces[3].find('[')]
                        pid = int((pieces[3][pieces[3].find('['):])[1:-1])
                        thread = pieces[7]

                        lines[line_num] = LineObject(line_num, time, host, app, pid, thread)
                        continue
            else:
                if message_line[0]:
                    lines[message_line[1]].body = lines[message_line[1]].body + line
                    line_num -= 1
                else:
                    line_num -= 1
                continue
    return lines


