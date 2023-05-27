import os

def ParseUsername(line, mode):
    """
    function uses to parse usernames from ticket files

    :param line: string line from file
    :param mode: 1 -- raik199x:1111 -> raik199x  2 -- raik199x:1111 -> 1111
    :return: string value
    """
    for num, i in enumerate(line):
        if i == ":":
            if mode == 1:
                return line[0:num]
            elif mode == 2:
                return line[num + 1:-1]


def IsUserAdmin(chatId):
    with open("mods.txt", "r") as file:
        mods = file.read()
        mods = mods.split("\n")
        admin_access = False
        for i in mods:
            if i == str(chatId):
                admin_access = True
    return admin_access


def IsThereTickets():
    """
    :return: int value, 0 if no ticket, 1 if opposite
    """
    for _ in os.listdir('tickets'):
        return 1
    return 0
