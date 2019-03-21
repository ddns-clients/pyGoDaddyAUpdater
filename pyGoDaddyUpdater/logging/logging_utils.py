#                             pyGoDaddyAUpdater
#                  Copyright (C) 2019 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
import logging


def cleanup_old_logs(log_file: str):
    import tarfile
    import os

    tar_log_filename = log_file + ".tar.gz"

    if os.path.exists(log_file):
        if os.path.exists(tar_log_filename):
            os.remove(tar_log_filename)
        with tarfile.open(tar_log_filename, "w:gz") as tar:
            tar.add(log_file, arcname=os.path.basename(log_file))
            tar.close()
            os.remove(log_file)


def setup_logging(logger_name: str, log_file: str, level=logging.DEBUG,
                  formatter: str = "%(asctime)s | [%(levelname)s]: %(message)s"):
    cleanup_old_logs(log_file)
    new_logging = logging.getLogger(logger_name)
    logging_formatter = logging.Formatter(formatter)
    logging_file_handler = logging.FileHandler(log_file, mode="w")

    logging_file_handler.setFormatter(logging_formatter)

    new_logging.setLevel(level)
    new_logging.addHandler(logging_file_handler)


class LoggingHandler(object):
    class __LoggingHandler(object):
        def __init__(self, logs: list):
            self.__logs = logs

        def debug(self, msg):
            for log in self.__logs:
                log.debug(msg)

        def info(self, msg):
            for log in self.__logs:
                log.info(msg)

        def error(self, msg):
            for log in self.__logs:
                log.error(msg)

        def warning(self, msg):
            for log in self.__logs:
                log.warning(msg)

        def critical(self, msg):
            for log in self.__logs:
                log.critical(msg)

        def exception(self, msg, *args, exc_info: bool = True, **kwargs):
            for log in self.__logs:
                log.exception(msg, args, exc_info, kwargs)

        def get_loggers(self) -> list:
            return self.__logs

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not LoggingHandler.__instance:
            logs = kwargs.get("logs")
            if not logs or len(logs) == 0:
                raise AttributeError("At least kwarg \"log\" (a list of the loggers) must be provided")
            LoggingHandler.__instance = LoggingHandler.__LoggingHandler(logs)
        return LoggingHandler.__instance

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def __setattr__(self, key, value):
        return setattr(self.__instance, key, value)

    def debug(self, msg):
        self.__instance.debug(msg)

    def info(self, msg):
        self.__instance.info(msg)

    def error(self, msg):
        self.__instance.error(msg)

    def warning(self, msg):
        self.__instance.warning(msg)

    def critical(self, msg):
        self.__instance.critical(msg)

    def exception(self, msg, *args, exc_info: bool = True, **kwargs):
        self.__instance.exception(msg, args, exc_info, kwargs)

    def get_loggers(self) -> list:
        return self.__instance.get_loggers()
