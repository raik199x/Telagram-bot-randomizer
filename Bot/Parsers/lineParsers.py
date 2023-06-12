from Bot.shared.constants import *


def ParseUsername(line, mode):
    """
    function uses to parse usernames from ticket files

    :param line: string line from file
    :param mode: 1 -- raik199x:1111 -> raik199x  2 -- raik199x:1111 -> 1111
    :return: string value
    """
    for num, i in enumerate(line):
        if i == ":":
            return line[0:num] if mode == 1 else line[num + 1:-1]