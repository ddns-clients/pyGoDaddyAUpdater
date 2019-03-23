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


def get_machine_public_ip():
    import urllib.request

    return urllib.request.urlopen('https://ident.me').read().decode('utf8')


class GoDaddy(object):
    def __init__(self, domain, name, key, secret):
        self.__domain = domain
        self.__name = name
        self.__headers = "sso-key {0}:{1}".format(key, secret)

    def get_godaddy_latest_ip(self):
        from urllib.request import Request, urlopen
        from re import search

        request = Request("https://api.godaddy.com/v1/domains/{0}/records/A/{1}".format(self.__domain, self.__name))
        request.add_header("Authorization", self.__headers)
        result = urlopen(request).read().decode('utf8')

        ip = search("([0-9]{1,3}\.){3}[0-9]{1,3}", result)
        return ip.group(0) if ip else "0.0.0.0"

    def set_goddady_ip(self, ip):
        from urllib.request import Request, urlopen
        try:
            from ujson import dumps
        except ImportError:
            from json import dumps

        data = dumps([{"data": ip, "ttl": 600, "name": self.__name, "type": "A"}])
        request = Request(url="https://api.godaddy.com/v1/domains/{0}/records/A/{1}".format(self.__domain, self.__name),
                          data=data,
                          headers={"Authorization": self.__headers, "Content-Type": "application/json"},
                          method="PUT")
        return urlopen(request).getcode()
