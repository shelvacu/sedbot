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

import re

from sedbot import network

def resp_ping(who):
    network.send("PONG {}\r\n".format(who))

def set_nick(nick):
    network.send("NICK {}\r\n".format(nick))

def set_user(string):
    network.send("USER {}\r\n".format(string))

def join_channel(channel):
    global __channel__
    network.send("JOIN {}\r\n".format(channel))
    __channel__ = channel

def send_msg(msg):
    network.send("PRIVMSG {} :{}\r\n".format(__channel__, msg))

def parse_privmsg(tokens):
    who = re.search("(?<=:).*?(?=!)", tokens[0]).group(0)
    where = tokens[2]
    message = str.join(" ", tokens[3:])
    # Get rid of initial :
    message = message[1:]

    return who, where, message
