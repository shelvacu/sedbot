# sedbot - simple IRC sed invocation bot
# Copyright (C) 2015 Robert Cochran
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket

__sock__ = None

def connect(addr, port):
    global __sock__

    try:
        __sock__ = socket.socket()
        __sock__.connect((addr, port))
    except OSError as e:
        print(e)
        __sock__ = None

    return __sock__ is not None

def receive():
    global __sock__

    try:
        data = __sock__.recv(4096)
    except socket.timeout:
        return ""

    return data.decode()

def send(msg):
    global __sock__
    __sock__.send(msg.encode())
