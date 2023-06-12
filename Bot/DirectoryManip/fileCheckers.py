from Bot.shared.constants import *
import os


def CreateWorkingDirectory():
    os.mkdir(botDirectory)
    with open(botDirectory + botMasterKeyFile, "w+") as file:
        file.write("created_by_raik199x")
    os.mkdir(botDirectory + botStatusDirectory)
    os.mkdir(botDirectory + botTicketsDirectory)
    open(botDirectory + botModeratorsFile, "w").close
    open(botDirectory + botRegKeyFile, "w").close
    open(botDirectory + botBannedFile, "w").close
    open(botDirectory + botSwapFile, "w").close
    with open(botDirectory + botSwapFile, "w+") as file:
        file.write(
            "https://github.com/raik199x/Bot-randomizer \n\nMade with enthusiasm by @raik199x")


def CheckWorkingDirectory():
    """
    Checks if bot directory exists and creates it if not

    Returns:
        "Setup" if bot is running for the first time
        "OK" if bot directory fully exists
    """
    botDirectories = [botDirectory + botStatusDirectory,
                      botDirectory + botTicketsDirectory]
    botFiles = [botDirectory + botMasterKeyFile, botDirectory + botModeratorsFile, botDirectory +
                botRegKeyFile, botDirectory + botBannedFile, botDirectory + botSwapFile, botDirectory + botContactsFile]
    # this means that bot is running for the first time
    if not os.path.exists(botDirectory):
        CreateWorkingDirectory()
        return "Setup"
    for directory in botDirectories:
        if not os.path.exists(directory):
            os.mkdir(directory)
    for file in botFiles:
        if not os.path.exists(file):
            open(file).close
    return "OK"
