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
import traceback
from argparse import ArgumentParser
from argparse import SUPPRESS
from logging import getLogger
from os import makedirs
from os import path
from time import sleep

from daemonize import Daemonize

from .logging_utils import LoggingHandler
from .logging_utils import setup_logging
from .network import GoDaddy
from .network import get_machine_public_ip
from .preferences import UserPreferences
from .values import description

preferences = UserPreferences()


def main():
    loop_continuation = True
    log = LoggingHandler(logs=[getLogger("appLogger")])
    try:
        net = GoDaddy(preferences.get_domain(), preferences.get_name(),
                      preferences.get_key(), preferences.get_secret())
        while loop_continuation:
            current_ip = get_machine_public_ip()
            log.info("Current machine IP: \"{0}\"".format(current_ip))
            if preferences.get_latest_ip() == "0.0.0.0":
                preferences.set_latest_ip(net.get_godaddy_latest_ip())
                log.warning("User saved latest IP is not up to date - downloading GoDaddy A Record value: \"{0}\""
                            .format(preferences.get_latest_ip()))
            if not current_ip:
                log.warning("Cannot obtain IP from ipfy")
            if current_ip and preferences.get_latest_ip() != current_ip:
                log.info("IP needs an upgrade - OLD IP: {0} | NEW IP: {1}"
                         .format(preferences.get_latest_ip(), current_ip))
                result = net.set_goddady_ip(current_ip)
                log.info("IP updated correctly! - Operation return code: {0}".format(result))
                log.debug("Updating saved IP...")
                preferences.set_latest_ip(current_ip)
            else:
                log.info("IP has not changed - skipping")
            if not preferences.is_running_as_daemon():
                log.info("This script is only executed once. Finishing...")
                loop_continuation = False
            else:
                log.info("Next check in about {0} minute{1}"
                         .format((preferences.get_time() / 60),
                                 's' if (preferences.get_time() / 60) > 1 else ''))
                sleep(preferences.get_time())
    except KeyboardInterrupt:
        log.warning("Received SIGINT - exiting...")
    except Exception as e:
        log.error("Exception registered! - " + str(e))
        log.error("Stacktrace: " + traceback.format_exc())
        log.error("Please, submit the stacktrace to: dev@javinator9889.com")
    finally:
        preferences.save_preferences()
        exit(0)


def parser():
    is_first_execution = not preferences.are_preferences_stored()
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
                      default=SUPPRESS,
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
                      default=False,
                      help="By default, the program runs as a daemon in background. With this option enabled, "
                           "the program will run only once and then exit.")
    args.add_argument("--pid",
                      type=str,
                      default=SUPPRESS,
                      required=False,
                      metavar="PID FILE",
                      help="Specifies a custom PID file for storing current daemon PID.")
    args.add_argument("--log",
                      type=str,
                      default=SUPPRESS,
                      required=False,
                      metavar="LOG FILE",
                      help="Specifies a custom LOG file for storing current daemon logs.")
    args.add_argument("--preferences",
                      type=str,
                      default="user.preferences",
                      required=False,
                      metavar="PREFERENCES FILE",
                      help="Provide a custom preferences file - useful for multiple running daemon for different 'A'"
                           "Records. NOTICE THAT YOU MUST PROVIDE ALL REQUIRED PARAMS FOR A NEW CONFIGURATION")
    args.add_argument("--user",
                      type=str,
                      default=None,
                      required=False,
                      metavar="USERNAME",
                      help="Run the daemon as the specified user.")
    args.add_argument("--group",
                      type=str,
                      default=None,
                      required=False,
                      metavar="GROUP NAME",
                      help="Run the daemon as the specified group.")
    p_args = args.parse_args()
    should_save_preferences = False
    if p_args.domain:
        preferences.set_domain(p_args.domain)
        should_save_preferences = True
    if p_args.name:
        preferences.set_name(p_args.name)
        should_save_preferences = True
    if "time" in p_args:
        preferences.set_time(p_args.time * 60)
        should_save_preferences = True
    else:
        if preferences.get_time() is None:
            preferences.set_time(300)
    if p_args.key:
        preferences.set_key(p_args.key)
        should_save_preferences = True
    if p_args.secret:
        preferences.set_secret(p_args.secret)
        should_save_preferences = True
    if p_args.no_daemonize:
        preferences.run_as_daemon(not p_args.no_daemonize)
    if "pid" in p_args:
        preferences.set_pid_file(p_args.pid)
        should_save_preferences = True
    else:
        if preferences.get_pid_file() is None:
            preferences.set_pid_file("/var/run/pygoddady.pid")
    if "log" in p_args:
        preferences.set_log_file(p_args.log)
        should_save_preferences = True
    else:
        if preferences.get_log_file() is None:
            preferences.set_log_file("/var/log/pygoddady.log")
    user = p_args.user
    group = p_args.group

    if p_args.preferences:
        if not (p_args.domain and p_args.name and p_args.key and p_args.secret):
            print("You must provide the required params for a new preferences file")
    if should_save_preferences:
        preferences.save_preferences(p_args.preferences)
    if not is_first_execution:
        preferences.load_preferences()
    file_handler = setup_logging("appLogger", preferences.get_log_file())
    fds = [file_handler.stream.fileno()]
    pid_dir = path.dirname(path.abspath(preferences.get_pid_file()))
    if not path.exists(pid_dir):
        makedirs(path=pid_dir, exist_ok=True)

    daemon = Daemonize(app="pyGoDaddyDaemon",
                       pid=preferences.get_pid_file(),
                       action=main,
                       keep_fds=fds,
                       user=user,
                       group=group,
                       logger=getLogger("appLogger"))
    daemon.start()


if __name__ == '__main__':
    parser()
