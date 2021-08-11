# class LineObject(object):
#     def __init__(self, line=None):
#         self.__line = int(line)
#
#     def getLine(self):
#         return self.__line


class MessageObject(object):
    def __init__(self, num=0, time=None, host=None, app=None, pid=None, thread=None, body=""):
        self.__num = int(num)
        self.time = time
        self.host = host
        self.app = app
        self.pid = pid
        self.thread = thread
        self.body = body

