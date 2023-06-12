from Bot.shared.constants import *
from Bot.Parsers.lineParsers import ParseUsername


def CheckPosition(fileName, chatId, place):
    """
    Checks is position valid

    :param message: message from user
    :param place: position in random
    :return: -1 invalid position, -2 His own position 0 Normal
    """
    try:
        place = int(place)
    except:
        return -1
    if place < 1:
        return -1
    with open(botDirectory + botTicketsDirectory + fileName, "r") as file:
        lines = file.readlines()
    for num, i in enumerate(lines):
        if num == 0:
            continue
        if num == int(place) and str(chatId) != ParseUsername(i, 2):
            return 0
    return 1


def SwapUsers(ticketName, asker, acceptor, acceptorId):
    if not os.path.exists(botDirectory + botTicketsDirectory + ticketName):
        return -1
    with open(botDirectory + botTicketsDirectory + ticketName, "r") as file:
        lines = file.readlines()
    accept = acceptor + ":" + acceptorId
    with open(botDirectory + botTicketsDirectory + ticketName, "w") as file:
        for i in lines:
            if i == "randomized\n":
                file.write(i)
                continue
            if i[:-1] == asker:
                file.write(accept + "\n")
                continue
            if i[:-1] == accept:
                file.write(asker + "\n")
                continue
            file.write(i)
    return 0


def DeleteRequest(mode, data):
    """
    Delete request line based on mode number:\n
    1 - delete all lines with such ticket name
    2 - delete all lines with this user

    :param mode: int value
    :param data: string value, data in it is based on chosen mode
    """
    with open(botDirectory + botSwapFile, "r") as file:
        lines = file.readlines()
    with open(botDirectory + botSwapFile, "w") as file:
        for i in lines:
            ticketName = i[:i.find("~")]
            i = i[i.find("~") + 1:]
            userOne = i[:i.find("~")]
            i = i[i.find("~") + 1:]
            userTwo = i[:i.find("\n")]
            if mode == 1 and data == ticketName:
                continue
            elif mode == 2 and (ParseUsername(userOne, 2) == data or ParseUsername(userTwo, 2)):
                continue
            file.write(ticketName + "~" + userOne + "~" + userTwo + "\n")


def ParsingSwapFile(message):
    """
    Parses swap file

    :param message: message from user
    :return: list, that first element is a value of:
    0 - no requests
    1 - current user active request
    2 - active request from another user
    then in case 1 and 2 also sends data about swap
    """
    with open(botDirectory + botSwapFile, "r") as file:
        for i in file.readlines():
            ticketName = i[:i.find("~")]
            # checking if ticket exist
            if not os.path.exists(botDirectory + botTicketsDirectory + ticketName):
                DeleteRequest(1, ticketName)
                return ParsingSwapFile(message)
            i = i[i.find("~") + 1:]
            userOne = i[:i.find("~") + 1]
            i = i[i.find("~") + 1:]
            userTwo = i[:i.find("\n") + 1]
            if str(message.chat.id) == ParseUsername(userOne, 2):
                return [1, ticketName, userTwo[:-1]]
            elif str(message.chat.id) == ParseUsername(userTwo, 2):
                return [2, ticketName, userOne[:-1]]
    return [0]
