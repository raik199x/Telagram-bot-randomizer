from Bot.shared.constants import *
from Bot.Parsers.lineParsers import ParseUsername


def IsUserAdmin(chatId):
    with open(botDirectory + botModeratorsFile, "r") as file:
        mods = file.read()
        mods = mods.split("\n")
        admin_access = False
        for i in mods:
            if i == str(chatId):
                admin_access = True
    return admin_access


def IsUserInRandom(message):
    """
    :param message: message from user, function will take text from it
    :return: 0 if user is not in random, 1 if opposite
    """
    with open(botDirectory + botTicketsDirectory + message.text, "r+") as file:
        file.readline()
        while (tempLine := file.readline()) != "":
            if ParseUsername(tempLine, 1) == message.from_user.username:
                return 1
        return 0
