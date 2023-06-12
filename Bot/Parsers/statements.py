from os import listdir
from Bot.shared.constants import *


def IsThereTickets():
    """
    :return: int value, 0 if no ticket, 1 if opposite
    """
    for _ in listdir(botDirectory + botTicketsDirectory):
        return 1
    return 0
