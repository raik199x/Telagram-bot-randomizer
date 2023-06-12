from Bot.shared.constants import *


def CheckRegKey(regKey):
    with open(botDirectory + botRegKeyFile, "r") as file:
        existingKeys = file.read()
        existingKeys = existingKeys.split("\n")
        for i in existingKeys:
            if regKey == i:
                return True
        return False


def CheckMasterKey(masterKey):
    with open(botDirectory + botMasterKeyFile, "r") as file:
        key = file.readline()
        return True if key == masterKey else False