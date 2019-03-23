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


class UserPreferences(object):
    def __init__(self, **kwargs):
        if kwargs:
            try:
                self.__domain = kwargs["domain"]
                self.__name = kwargs["name"]
                self.__time = kwargs["time"]
                self.__key = kwargs["key"]
                self.__secret = kwargs["secret"]
                self.__pid = kwargs["pid"]
                self.__log = kwargs["log"]
            except KeyError:
                raise AttributeError("Some value was not provided while creating user preferences\n"
                                     "Values are:\n"
                                     "  - Domain\n"
                                     "  - Name (of A Record)\n"
                                     "  - Time (update time)\n"
                                     "  - Key\n"
                                     "  - Secret\n")
        else:
            self.__domain = None
            self.__name = None
            self.__time = None
            self.__key = None
            self.__secret = None
            self.__pid = None
            self.__log = None
        self.__latest_ip = "0.0.0.0"
        self.__daemonize = True

    def load_preferences(self):
        import pickle
        import os

        from base64 import b64decode

        if os.path.exists("user.preferences"):
            with open("user.preferences", "rb") as fpreferences:
                preferences = pickle.load(fpreferences)
            self.__domain = preferences["domain"]
            self.__secret = b64decode(preferences["secret"]).decode("utf-8")
            self.__time = preferences["time"]
            self.__key = b64decode(preferences["key"]).decode("utf-8")
            self.__name = preferences["name"]
            self.__latest_ip = preferences["latest_ip"]
            self.__pid = preferences["pid"]
            self.__log = preferences["log"]
        else:
            raise FileNotFoundError("There are no saved user preferences. Call \"save_preferences\" the first time")

    def save_preferences(self):
        import pickle

        from base64 import b64encode

        preferences = {"domain": self.__domain,
                       "name": self.__name,
                       "time": self.__time,
                       "key": b64encode(bytes(self.__key, "utf-8")),
                       "secret": b64encode(bytes(self.__secret, "utf-8")),
                       "latest_ip": self.__latest_ip,
                       "pid": self.__pid,
                       "log": self.__log}
        with open("user.preferences", "wb") as fpreferences:
            pickle.dump(preferences, fpreferences, pickle.HIGHEST_PROTOCOL)

    def get_domain(self):
        return self.__domain

    def get_name(self):
        return self.__name

    def get_time(self):
        return self.__time

    def get_key(self):
        return self.__key

    def get_secret(self):
        return self.__secret

    def get_latest_ip(self):
        return self.__latest_ip

    def get_pid_file(self):
        return self.__pid

    def get_log_file(self):
        return self.__log

    def is_running_as_daemon(self):
        return self.__daemonize

    def set_domain(self, domain):
        self.__domain = domain

    def set_name(self, name):
        self.__name = name

    def set_time(self, time):
        self.__time = time

    def set_key(self, key):
        self.__key = key

    def set_secret(self, secret):
        self.__secret = secret

    def set_latest_ip(self, ip):
        self.__latest_ip = ip

    def set_pid_file(self, pid):
        self.__pid = pid

    def set_log_file(self, log):
        self.__log = log

    def run_as_daemon(self, daemonize: bool):
        self.__daemonize = daemonize

    @staticmethod
    def are_preferences_stored():
        import os

        return os.path.exists("user.preferences")
