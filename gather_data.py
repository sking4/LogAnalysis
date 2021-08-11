from message_object import MessageObject


def gather_data(file_path):
    lines = {}
    # Open file
    with open(str(file_path), encoding='ISO-8859-1') as my_file:
        # For each line in the file
        message_line = [False, 0]
        for line_num, line in enumerate(my_file):
            # If line contains "IncomingApp"
            if "IncomingApp" in line:
                # If line contains "Message.py 78 Incoming Message"
                if "Message.py 78 Incoming Message" in line:
                    message_line = [True, line_num]
                    # Create an object with the line number as the identifier and add fields as attributes
                    pieces = line.split()
                    time = pieces[0]
                    host = pieces[2]
                    app = pieces[3][:pieces[3].find('[')]
                    pid = (pieces[3][pieces[3].find('['):])[1:-1]
                    thread = pieces[7]

                    lines[line_num] = MessageObject(line_num, time, host, app, pid, thread)
                    continue
            elif message_line[0]:
                if line[:4] == '<nl>':
                    lines[message_line[1]].body = lines[message_line[1]].body + line
                else:
                    message_line[0] = False
                continue
    return lines

