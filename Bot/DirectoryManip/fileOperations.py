from Bot.shared.constants import *


def AddAdmin(chatId):
    """
    Adds user to admin list

    Args:
        chatId: user's chat id

    Returns:
        "OK" if user was added
        "Already admin" if user is already admin
    """
    with open(botDirectory + botModeratorsFile, "r") as file:
        if str(chatId) in file.read():
            return "Already admin"
    with open(botDirectory + botModeratorsFile, "a") as file:
        file.write(str(chatId) + "\n")
    return "OK"


def DeleteAdmin(chatId):
    """
    Deletes user from admin list

    Args:
        chatId: user's chat id
    """
    with open(botDirectory + botModeratorsFile, "r") as file:
        lines = file.readlines()
    with open(botDirectory + botModeratorsFile, "w") as file:
        for line in lines:
            if line.strip("\n") != str(chatId):
                file.write(line)


def AddBanned(chatId):
    """
    Adds user to banned list

    Args:
        chatId: user's chat id

    Returns:
        "OK" if user was added
        "Already banned" if user is already banned
    """
    with open(botDirectory + botBannedFile, "r") as file:
        if str(chatId) in file.read():
            return "Already banned"
    with open(botDirectory + botBannedFile, "a") as file:
        file.write(str(chatId) + "\n")
    return "OK"


def DeleteBanned(chatId):
    """
    Deletes user from banned list

    Args:
        chatId: user's chat id
    """
    with open(botDirectory + botBannedFile, "r") as file:
        lines = file.readlines()
    with open(botDirectory + botBannedFile, "w") as file:
        for line in lines:
            if line.strip("\n") != str(chatId):
                file.write(line)
