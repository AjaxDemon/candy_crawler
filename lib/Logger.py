# coding: utf-8

import os
import datetime


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
