from Bot.shared.constants import *
from Bot.Parsers.lineParsers import ParseUsername


def ShowUserTicketFile(fileName, message):
    """
    parses ticket file and sends info to user

    :param fileName: path to file
    :param message: message from user
    """
    botMessage = fileName + "\nStatus: "
    with open(botDirectory + botTicketsDirectory + fileName, "r") as file:
        status = file.readline()
        botMessage += status + "\nPeople:\n"
        if status[:-1] == "Active":
            isInTicket = int()
            while (tempLine := file.readline()) != "":
                botMessage += ParseUsername(tempLine, 1) + "\n"
                isInTicket = 1 if ParseUsername(
                    tempLine, 1) == message.from_user.username else 0
            botMessage += "\nYou are registered" if isInTicket == 1 else "\nYou are NOT registered"
        else:
            currentMan = 1
            isInTicket = 0
            while (tempLine := file.readline()) != "":
                botMessage += str(currentMan) + ". " + \
                    ParseUsername(tempLine, 1) + "\n"
                if ParseUsername(tempLine, 1) == message.from_user.username:
                    isInTicket = currentMan
                currentMan += 1
            botMessage += "\nYou didn't entered this random" if isInTicket == 0 else "\nYour place is " + \
                str(isInTicket)
    return botMessage