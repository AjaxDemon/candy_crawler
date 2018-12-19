# coding: utf-8

import os
import datetime


class Log:

    def __init__(self):
        self.buffer = []

    def record(self, *msgs):
        msgstr = ''
        for msg in msgs:
            msgstr += str(msg) + ' '
        self.buffer.append(msgstr + '\r\n')

    def write(self, *msgs):
        self.write_to_file()
        msgstr = ''
        for msg in msgs:
            msgstr += str(msg) + ' '
        self.buffer.append(msgstr + '\r\n')
        self.write_to_file()

    def write_to_file(self):
        if not os.path.exists('logs'):
            os.mkdir('logs', 755)
        filename = 'logs/%s.log' % datetime.datetime.now().strftime('%Y%m%d%H')
        with open(filename, 'ab+') as log_file:
            for log in self.buffer:
                log_file.write(log.encode('utf8'))
            log_file.close()
        self.buffer.clear()


class Logger:

    LOG_BUFFER = []

    @staticmethod
    def write_log_file():
        if not os.path.exists('logs'):
            os.mkdir('logs', 755)
        filename = 'logs/%s.log' % datetime.datetime.now().strftime('%Y%m%d%H')
        with open(filename, 'ab+') as log_file:
            for log in Logger.LOG_BUFFER:
                log_file.write(log.encode('utf8'))
            log_file.close()
        Logger.LOG_BUFFER.clear()

    @staticmethod
    def record_log(*msgs, is_print=True):
        if is_print:
            print(*msgs)
        msgstr = ''
        for msg in msgs:
            msgstr += str(msg) + ' '
        Logger.LOG_BUFFER.append(msgstr + '\r\n')

    @staticmethod
    def write(*msgs, is_print=True):
        Logger.write_log_file()
        if is_print:
            print(*msgs)
        msgstr = ''
        for msg in msgs:
            msgstr += str(msg) + ' '
        Logger.LOG_BUFFER.append(msgstr + '\r\n')
        Logger.write_log_file()


