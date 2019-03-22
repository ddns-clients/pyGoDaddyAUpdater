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
from argparse import ArgumentParser
from logging import getLogger
from sys import argv
from time import sleep

from pyGoDaddyUpdater.logging import LoggingHandler
from pyGoDaddyUpdater.logging import setup_logging
from pyGoDaddyUpdater.network import GoDaddy
from pyGoDaddyUpdater.network import get_machine_public_ip
from pyGoDaddyUpdater.preferences import UserPreferences
from pyGoDaddyUpdater.values import description

arguments = {"domain": "",
             "name": "",
             "time": 300,
             "key": "",
             "secret": "",
             "latest_ip": "0.0.0.0",
             "no_daemonize": False,
             "pid_file": "",
             "log_file": "/var/log/pygodaddy.log"}
preferences = UserPreferences()


def main():
    try:
        loop_continuation = True
        log = LoggingHandler(logs=[getLogger("appLogger")])
        net = GoDaddy(arguments["domain"], arguments["name"], arguments["key"], arguments["secret"])
        while loop_continuation:
            current_ip = get_machine_public_ip()
            log.info("Current machine IP: \"{0}\"".format(current_ip))
            if arguments["latest_ip"] == "0.0.0.0":
                arguments["latest_ip"] = net.get_godaddy_latest_ip()
                log.warning("Latest IP not updated - saving GoDaddy stored value: \"{0}\""
                            .format(arguments["latest_ip"]))
            if arguments["latest_ip"] != current_ip:
                log.info("IP needs an upgrade: OLD: {0} | NEW: {1}".format(arguments["latest_ip"], current_ip))
                result = net.set_goddady_ip(current_ip)
                log.info("IP updated correctly! - Operation return code: {0}".format(result))
            if not arguments["daemonize"]:
                loop_continuation = False
            else:
                sleep(arguments["time"])
    except KeyboardInterrupt:
        print("Received SIGINT - exiting...")
        exit(1)


def parser():
    is_first_execution = UserPreferences.are_preferences_stored()
    args = ArgumentParser(description=description,
                          allow_abbrev=False)
    args.add_argument("--domain",
                      type=str,
                      required=is_first_execution,
                      help="GoDaddy domain to be updated.")
    args.add_argument("--name",
                      type=str,
                      required=is_first_execution,
                      help="GoDaddy 'A' Record name.")
    args.add_argument("--time",
                      type=int,
                      default=5,
                      required=is_first_execution,
                      help="Time (in minutes) to check for updated IP (defaults: 5 min.) - must be higher than 0.")
    args.add_argument("--key",
                      type=str,
                      required=is_first_execution,
                      help="GoDaddy developer key.")
    args.add_argument("--secret",
                      type=str,
                      required=is_first_execution,
                      help="GoDaddy developer secret.")
    args.add_argument("--no_daemonize",
                      action="store_true",
                      required=False,
                      help="By default, the program runs as a daemon in background. With this option enabled, "
                           "the program will run only once and then exit.")
    args.add_argument("--pid",
                      type=str,
                      default="/var/run/pygoddady/app.pid",
                      required=False,
                      metavar="PID FILE",
                      help="Specifies a custom PID file for storing current daemon PID.")
    args.add_argument("--log",
                      type=str,
                      default="/var/log/pygodaddy.log",
                      required=False,
                      metavar="LOG FILE",
                      help="Specifies a custom LOG file for storing current daemon logs.")
    p_args = args.parse_args()
    if p_args.domain:
        arguments["domain"] = p_args.domain
        preferences.set_domain(p_args.domain)
    if p_args.name:
        arguments["name"] = p_args.name
        preferences.set_domain(p_args.name)
    if p_args.time:
        arguments["time"] = p_args.time * 60
        preferences.set_domain(p_args.time)
    if p_args.key:
        arguments["key"] = p_args.key
        preferences.set_domain(p_args.key)
    if p_args.secret:
        arguments["secret"] = p_args.secret
        preferences.set_domain(p_args.secret)
    if p_args.no_daemonize:
        arguments["no_daemonize"] = p_args.no_daemonize
    if p_args.pid:
        arguments["pid_file"] = p_args.pid
    if p_args.log:
        arguments["log_file"] = p_args.log
    if len(argv) >= 1:
        preferences.save_preferences()
    setup_logging("appLogger", arguments["log_file"])


if __name__ == '__main__':
    parser()
