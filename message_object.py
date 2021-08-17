# class LineObject(object):
#     def __init__(self, line=None):
#         self.__line = int(line)
#
#     def getLine(self):
#         return self.__line


class LineObject(object):
    def __init__(self, line=0, time=None, host=None, app=None, pid=None, thread=None, body=""):
        self.line = int(line)
        self.time = time
        self.host = host
        self.app = app
        self.pid = pid
        self.thread = thread
        self.body = body


class HostObject(object):
    def __init__(self, host=None, entries=None):
        self.host = host
        self.__entries = entries

    def getHost(self):
        return self.host

    def appendEntry(self, line, pid, thread):
        if not self.__entries:
            self.__entries = []
        self.__entries.append((line, pid, thread))


class PidObject(object):
    def __init__(self, pid=None, app=None, first=None, last=None, body=None):
        self.pid = pid
        self.app = app
        self.first = first
        self.last = last
        self.body = body

