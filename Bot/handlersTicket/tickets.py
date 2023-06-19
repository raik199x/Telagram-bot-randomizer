from Bot.shared.constants import *
from Bot.shared.functions import *
from Bot.Parsers.statements import IsThereTickets
from Bot.Parsers.userProperties import IsUserInRandom, IsUserAdmin
from Bot.Parsers.lineParsers import ParseUsername
from Bot.Keyboards.dynamic import GetTicketsMenuKeyboard, GetTicketsKeyboard, GetWaitingInputKeyboard
from Bot.handlersTicket.processingFunctions import ShowUserTicketFile
from Bot.randomFunctions.randoms import PerformingRandom
from Bot.logger.setup import logger, BasicUserInfo


@bot.message_handler(func=lambda message: message.text == "Show tickets" and GetUserStatus(message.chat.id) == user_idle)
def ShowTicketsHandler(message):
    if IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "There is no tickets", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        return
    for i in os.listdir(botDirectory + botTicketsDirectory):
        bot.send_message(message.chat.id, ShowUserTicketFile(
            str(i), message), reply_markup=GetTicketsMenuKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: message.text == "Join random" and GetUserStatus(message.chat.id) == user_idle)
def JoinRandomHandler(message):
    if IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "There is no tickets", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        return
    bot.send_message(message.chat.id, "Choose ticket (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 2))
    SetUserStatus(message.chat.id, user_joining_ticket)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_joining_ticket)
def ActivateTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    if not os.path.exists(botDirectory + botTicketsDirectory + message.text):
        bot.send_message(message.chat.id, "No such ticket")
        return
    if IsUserInRandom(message) == 1:
        bot.send_message(message.chat.id, "You are already in this random")
        return
    with open(botDirectory + botTicketsDirectory + message.text, "r") as file:
        if file.readline() == "Randomized\n":
            bot.send_message(
                message.chat.id, "This random was already randomized")
            return
    with open(botDirectory + botTicketsDirectory + message.text, "a+") as file:
        file.write(message.from_user.username +
                   ":" + str(message.chat.id) + "\n")
    bot.send_message(message.chat.id, "You entered random",
                     reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Create ticket (adm)" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def CreateTicketHandler(message):
    logger.info("User " + BasicUserInfo(message) + " started creating ticket")

    bot.send_message(
        message.chat.id, "Enter name of the event or use keyboard", reply_markup=GetWaitingInputKeyboard(message.chat.id))
    SetUserStatus(message.chat.id, admin_creating_ticket)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_creating_ticket)
def CreateTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        logger.critical("User " + BasicUserInfo(message) + " tried to create ticket with forbidden symbols")
        return
    elif os.path.exists(botDirectory + botTicketsDirectory + str(message.text)):
        logger.info("User " + BasicUserInfo(message) + " tried to create ticket with existing name")
        bot.send_message(
            message.chat.id, "Sorry, such event is already exist")
        return
    with open(botDirectory + botTicketsDirectory + message.text, "w") as ticketFile:
        ticketFile.write("Active\n")
    bot.send_message(message.chat.id, "Created!", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    SetUserStatus(message.chat.id, user_idle)
    logger.info("User " + BasicUserInfo(message) + " created ticket '" + str(message.text) + "'")


@bot.message_handler(func=lambda message: message.text == "Delete ticket (adm)" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def DeleteTicketHandler(message):
    logger.info("User " + BasicUserInfo(message) + " started deleting ticket")

    if IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "no tickets found", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        return
    bot.send_message(message.chat.id, "Enter ticket to delete or choose cancel (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 1))
    SetUserStatus(message.chat.id, admin_deleting_ticket)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_deleting_ticket)
def DeleteTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        logger.critical("User " + BasicUserInfo(message) + " tried to delete ticket with forbidden symbols (possible attack)")
        return
    if os.path.exists(botDirectory + botTicketsDirectory + str(message.text)):
        logger.warning("User " + BasicUserInfo(message) + " deleted ticket '" + str(message.text) + "'")
        os.remove(botDirectory + botTicketsDirectory + str(message.text))
        bot.send_message(message.chat.id, "Deleted!",
                         reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        SetUserStatus(message.chat.id, user_idle)
        return
    else:
        bot.send_message(message.chat.id, "File not found")
        logger.info("User " + BasicUserInfo(message) + " tried to delete ticket which not exist")


@bot.message_handler(func=lambda message: message.text == "Start random (adm)" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def StartRandomHandler(message):
    if IsThereTickets() == 0:
        bot.send_message(message.chat.id, "There is no tickets")
        logger.info("User " + BasicUserInfo(message) + " tried to start random with no tickets")
        return
    SetUserStatus(message.chat.id, admin_starting_random)
    bot.send_message(message.chat.id, "Select ticket which you should activate (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 3))
    logger.info("User " + BasicUserInfo(message) + " starting random")


# TODO: make another notifications and create for them another folder
def Notification(fileName):
    """
    sends message about position in the random

    :param fileName: path to ended random file
    """
    with open(botDirectory + botTicketsDirectory + fileName, "r") as file:
        content = file.readlines()
    content.remove(content[0])
    for num, i in enumerate(content):
        bot.send_message(int(ParseUsername(i, 2)), "Random \"" +
                         fileName + "\" is ended\nYour place - " + str(num + 1))


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_starting_random)
def RandomTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        logger.critical("User " + BasicUserInfo(message) + " tried to start random with forbidden symbols (possible attack)")
        return
    elif not os.path.exists(botDirectory + botTicketsDirectory + message.text):
        logger.info("User " + BasicUserInfo(message) + " tried to start random with not existing ticket")
        bot.send_message(message.chat.id, "Ticket does not exist")
        return
    # checking some conditions
    with open(botDirectory + botTicketsDirectory + message.text, "r") as preRandom:
        if not preRandom.readline() == "Active\n":
            logger.info("User " + BasicUserInfo(message) + " tried to start random with not active ticket")
            bot.send_message(
                message.chat.id, "This ticket is already randomized")
            return
        if preRandom.readline() == "":
            logger.info("User " + BasicUserInfo(message) + " tried to start random with empty ticket")
            bot.send_message(
                message.chat.id, "there is no users for random")
            return
    with open(botDirectory + botTicketsDirectory + message.text, "r") as gettingUsers:
        usersInRandom = gettingUsers.readlines()
        usersInRandom.remove(usersInRandom[0])
    PerformingRandom(message.text, usersInRandom)
    bot.send_message(message.chat.id, "Random successfully done!",
                     reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    Notification(message.text)
    SetUserStatus(message.chat.id, user_idle)
    logger.info("User " + BasicUserInfo(message) + " started random for ticket '" + str(message.text) + "'")
