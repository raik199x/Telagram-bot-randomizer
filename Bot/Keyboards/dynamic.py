from telebot import types
from Bot.Parsers.userProperties import IsUserAdmin
from Bot.shared.constants import *
from Bot.Parsers.lineParsers import ParseUsername


def GetTicketsMenuKeyboard(chatId):
    ticketMenu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ticketMenu_keyboard.add("Show tickets", "Join random")
    ticketMenu_keyboard.add("Check swap requests", "Request swap")
    if IsUserAdmin(chatId):
        ticketMenu_keyboard.add("Create ticket (adm)",
                                "Delete ticket (adm)", "Start random (adm)")
    ticketMenu_keyboard.add("Back")
    return ticketMenu_keyboard


def GetTicketsKeyboard(message, mode):
    """
    Collects needed data and create keyboard for user\n
    Modes: 1 - get all, 2 - without user, 3 - with Active state, 4 with randomized state

    :param message: message from user
    :param mode: set condition for creating keyboard
    :return: keyboard markup
    """
    existingTickets = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if mode == 1:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            existingTickets.add(types.KeyboardButton(i))
    elif mode == 2:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            isInTheTicket = 0
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                file.readline()
                while (tempLine := file.readline()) != "":
                    if ParseUsername(tempLine, 1) == message.from_user.username:
                        isInTheTicket = 1
                        break
            if isInTheTicket == 0:
                existingTickets.add(types.KeyboardButton(i))
    elif mode == 3:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                if file.readline() == "Active\n":
                    existingTickets.add(types.KeyboardButton(i))
    elif mode == 4:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                if file.readline() == "randomized\n":
                    existingTickets.add(types.KeyboardButton(i))
    existingTickets.add("Back to ticket menu")
    return existingTickets


def GetWaitingInputKeyboard(chatId):
    waitingInput = types.ReplyKeyboardMarkup(resize_keyboard=True)
    waitingInput.add("Waiting Input")
    if IsUserAdmin(chatId):
        waitingInput.add("Back to ticket menu", "Back to admin menu", "Back to basic randoms")
    else:
        waitingInput.add("Back to ticket menu", "Back to basic randoms")
    return waitingInput


def GetMainKeyboard(chatId):
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_keyboard.add("Tickets", "Basic randoms")
    main_keyboard.add("Contacts")
    if IsUserAdmin(chatId):
        main_keyboard.add("Admin Panel")
    return main_keyboard