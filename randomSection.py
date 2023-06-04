import random
import string
from sharedVariables import *


def GenerateRegKey():
    newKey = str()
    for i in range(0, 101):
        newKey += random.choice(string.ascii_letters)
    with open(botDirectory + botRegKeyFile, "a+") as file:
        file.write(newKey + "\n")
    return newKey


def PerformingRandom(fileName, users):
    """
    Randoms users and then writes results in the file

    :param fileName: file which will be replaced with randomized version
    :param users: list of users
    """
    with open(botDirectory + botTicketsDirectory + fileName, "w") as file:
        file.write("Randomized\n")
        temp = len(users)
        for i in range(temp):
            j = random.randint(0, temp - i - 1)
            file.write(users[j])
            users.remove(users[j])
