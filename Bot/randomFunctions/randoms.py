import random
import string
from Bot.shared.constants import *


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
    coins = ["CoinHead.png", "CoinTail.png"]
    return coins[0] if random.randint(0, 1) == 0 else coins[1]


def DiceRoll(amount):
    """
    Randomly throws a dice

    @param amount amount of dices to throw
    @return: string with dices
    """
    dices = ["d1.png", "d2.png", "d3.png", "d4.png", "d5.png", "d6.png"]
    result = []
    for i in range(amount):
        result.append(dices[random.randint(0, 5)])
    return result


def RandomNumber(numberFrom, numberTo):
    """
    Randomly generates a number

    @param numberFrom: number from
    @param numberTo: number to
    @return: string with number
    """
    return str(random.randint(int(numberFrom), int(numberTo)))
