import random
import string
from sharedVariables import *

coins = ["CoinHead.png", "CoinTail.png"]
dices = ["d1.png", "d2.png", "d3.png", "d4.png", "d5.png", "d6.png"]

def GenerateRegKey():
    """
    Generates a new registration key and writes it in the file

    @return new registration key
    """
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


def CoinFlip():
    return coins[0] if random.randint(0, 1) == 0 else coins[1]


def DiceRoll(amount):
    """
    Randomly throws a dice

    @param amount amount of dices to throw
    @return: string with dices
    """
    result = []
    for i in range(amount):
        result.append(dices[random.randint(0, 5)])
    return result
