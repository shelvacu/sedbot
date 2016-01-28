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

import sys
import os
import re
import collections

from . import network
from . import irc

def run(args):
    if len(args) < 4:
        print("Usage: sedbot <server> <port> <channel>")
        sys.exit(-1)

    host, port, channel = args[1:]
    port = int(port)

    if not host or not port or not channel:
        print("Did not specify any of host or port or channel.")
        sys.exit(-1)

    if not network.connect(host, port):
        sys.exit(-1)

    irc.set_nick("underscores_sed")
    irc.set_user("sedbot 0 * :Sedbot IRC Bot")
    irc.join_channel(channel)

    in_buffer = ""

    msg_buffer = collections.deque([], 50)

    while True:
        in_buffer = in_buffer + network.receive()

        pending_lines = in_buffer.split("\n")

        # Take the last element which likely isn't a line
        in_buffer = pending_lines.pop()

        for line in pending_lines:
            print(line)

            # Remove anything past the \r
            line = line.rstrip("\r")
            # Tokenize
            tokens = line.split(" ")

            if tokens[0] == "PING":
                irc.resp_ping(tokens[1])

            if tokens[1] == "PRIVMSG":
                who, where, msg = irc.parse_privmsg(tokens)

                if re.search("I(['\"]m| am) hitler",msg,re.IGNORECASE):
                    irc.send_msg("Are you sure {}?".format(who))
                    continue

                if msg[0:2] == "s/": # Start of a regex
                    regex = re.findall("(?<=/).*?(?=/)", msg)

                    if len(regex) < 2:
                        irc.send_msg("Regex is incomplete. No can do. :(")
                        continue

                    try:
                        to_replace = re.compile(regex[0])

                        for m in reversed(msg_buffer):
                            if re.search(regex[0], m["msg"]): break

                        regexed_msg = to_replace.sub(regex[1], m["msg"])

                        print("sedbot: replace '{} -> {}' for {} on message '{}'"
                              "from {}".format(regex[0], regex[1], who,
                              m["msg"], m["who"]))

                        fixed_line = "<{}> {}".format(m["who"], regexed_msg)
                    except re.error as e:
                        fixed_line = "Sorry, couldn't do the regex - {}".format(e)

                    irc.send_msg(fixed_line)

                msg_buffer.append({"who":who, "where":where, "msg":msg})
