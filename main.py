import telebot
import os
import randomSection
import swapFunctions
import Parsers
from sharedVariables import *

# TODO:
# > Deleting reg key: check if key exists, if not - send message, if yes - show existing keys
# > All keyboard: Create function for creating keyboards that will check if user admin and add admin buttons
# > Swap: add more user-friendly interface
# > add Unban user function
# > custom list random
# > random number generator
# > make more files for the project

"""
0 - entering master key
1 - entering registration key
----------------------------
ADMIN MENU
10 - changing master key
11 - deleting reg key
12 - banning user
13 - modifying contacts
14 - unbanning user
----------------------------
TICKETS
21 - creating ticket
22 - deleting ticket
23 - joining ticket (random)
24 - starting random
----------------------------
SWAPPING
31 - writing swap rule
33 - you requested swap
34 - someone requested swap with you
----------------------------
BASIC RANDOMS
41 - dice roll
----------------------------
-1 - nothing (AKA idle)
"""

# bot token (export TOKEN=your_token_value) or just hardcode it
bot = telebot.TeleBot(os.getenv("TOKEN"))


def SecurityFileCheck(message):
    """
    function to defend user from leaving folder (shortly, deny access to the system)

    :param message: message that come from user
    :return: 1 if problems were found, 0 if not
    """
    if message.text[0] == '.':
        bot.send_message(
            message.chat.id, "Nice try, the issue was reported to the administrator")

        with open(botDirectory + botModeratorsFile, "r") as file:
            for i in file.readlines():
                bot.send_message(i, "User " + message.from_user.username + " with chat id " + str(
                    message.chat.id) + " tried to get access to the filesystem")
        return 1
    elif not message.text.find("/") == -1:
        bot.send_message(message.chat.id, "restricted symbol '/'")
        return 1
    return 0


def CreateBotFiles():
    os.mkdir(botDirectory)
    with open(botDirectory + botMasterKeyFile, "w+") as file:
        file.write("created_by_raik199x")
    os.mkdir(botDirectory + botStatusDirectory)
    os.mkdir(botDirectory + botTicketsDirectory)
    os.touch(botDirectory + botModeratorsFile)
    os.touch(botDirectory + botRegKeyFile)
    os.touch(botDirectory + botBannedFile)
    os.touch(botDirectory + botSwapFile)
    with open(botDirectory + botSwapFile, "w+") as file:
        file.write(
            "https://github.com/raik199x/Bot-randomizer \n\nMade with enthusiasm by @raik199x")


def CheckBanned(message):
    """
    Check if user is in banned state.

    :param message: message that comes from user
    :return: 1 if banned, 0 if opposite
    """
    try:
        file = open(botDirectory + botBannedFile, "r")
    except FileNotFoundError:  # if file with bans is not found, we do not allow anyone to enter
        bot.send_message(
            message.chat.id, "Error occurred with bot database, please write to admin")
        return 1

    for i in file.readlines():
        if str(message.chat.id) == i[:-1]:
            return 1
    file.close()
    return 0


main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("Tickets", "Basic randoms")
main_keyboard.add("Contacts")
main_keyboard.add("Admin Panel")

ticketMenu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
ticketMenu_keyboard.add("Show tickets", "Join random")
ticketMenu_keyboard.add("Check swap requests", "Request swap")
ticketMenu_keyboard.add("Create ticket (adm)",
                        "Delete ticket (adm)", "Start random (adm)")
ticketMenu_keyboard.add("Back")

admin_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add("Change master key")
admin_keyboard.add("Create registration key", "Delete registration key")
admin_keyboard.add("Ban user", "Unban user")
admin_keyboard.add("Modify contacts info")
admin_keyboard.add("Back")

answerIncomingSwap = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
answerIncomingSwap.add("Show tickets")
answerIncomingSwap.add("Accept swap", "Deny swap")
answerIncomingSwap.add("Back to ticket menu")

answerUserSwapRequest = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
answerUserSwapRequest.add("Show tickets")
answerUserSwapRequest.add("Cancel request", "Back to ticket menu")

requestingSwap = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
requestingSwap.add("Waiting Input")
requestingSwap.add("Show tickets")
requestingSwap.add("Back to ticket menu")

basicRandomsMenu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
basicRandomsMenu.add("Coin flip", "Dice roll")
basicRandomsMenu.add("Random number", "Custom list random")
basicRandomsMenu.add("Back")

waitingInput = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
waitingInput.add("Waiting Input")
waitingInput.add("Back to ticket menu", "Back to admin menu")


def SetUserStatus(chatId, status):
    """
    sets users status into given one

    :param chatId: chat id from message
    :param status: status to set (int or str)
    """
    if type(status) == int:
        status = str(status)
    with open(botDirectory + botStatusDirectory + str(chatId) + ".txt", "w") as file:
        file.write(str(status))


def GetUserStatus(chatId):
    """
    gets users status

    :param chatId: chat id from message
    :return: status of user
    """
    try:
        file = open(botDirectory + botStatusDirectory +
                    str(chatId) + ".txt", "r")
    except FileNotFoundError:
        bot.send_message(chatId, "Error occurred, you are not found in this bot database, please write "
                         "command /start")
        return "BAD"
    status = file.readline()
    file.close()
    return int(status)


def CheckRegKey(regKey):
    with open(botDirectory + botRegKeyFile, "r") as file:
        existingKeys = file.read()
        existingKeys = existingKeys.split("\n")
        for i in existingKeys:
            if regKey == i:
                return True
        return False


def ShowUserTicketFile(fileName, message):
    """
    parses ticket file and sends info to user

    :param fileName: path to file
    :param message: message from user
    """
    botMessage = fileName + "\nStatus: "
    isInTicket = 0
    with open(botDirectory + botTicketsDirectory + fileName, "r") as file:
        status = file.readline()
        botMessage += status + "\nPeople:\n"
        if status[:-1] == "Active":
            while True:
                tempLine = file.readline()
                if tempLine == "":
                    break
                botMessage += Parsers.ParseUsername(tempLine, 1)
                botMessage += "\n"
                if Parsers.ParseUsername(tempLine, 1) == message.from_user.username:
                    isInTicket = 1
            if isInTicket == 0:
                botMessage += "\nYou are NOT registered"
            else:
                botMessage += "\nYou already registered there"
        else:
            currentMan = 1
            while True:
                tempLine = file.readline()
                if tempLine == "":
                    break
                botMessage += str(currentMan) + ". " + \
                    Parsers.ParseUsername(tempLine, 1) + "\n"
                if Parsers.ParseUsername(tempLine, 1) == message.from_user.username:
                    isInTicket = currentMan
                currentMan += 1
            if isInTicket == 0:
                botMessage += "\nYou didn't entered this random"
            else:
                botMessage += "\nYour place is " + str(isInTicket)
    return botMessage


def GetTicketsKeyboard(message, mode):
    """
    Collects needed data and create keyboard for user\n
    Modes: 1 - get all, 2 - without user, 3 - with Active state, 4 with randomized state

    :param message: message from user
    :param mode: set condition for creating keyboard
    :return: keyboard markup
    """
    existingTickets = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if mode == 1:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            existingTickets.add(telebot.types.KeyboardButton(i))
    elif mode == 2:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            isInTheTicket = 0
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                file.readline()
                while True:
                    tempLine = file.readline()
                    if tempLine == "":
                        break
                    if Parsers.ParseUsername(tempLine, 1) == message.from_user.username:
                        isInTheTicket = 1
                        break
            if isInTheTicket == 0:
                existingTickets.add(telebot.types.KeyboardButton(i))
    elif mode == 3:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                if file.readline() == "Active\n":
                    existingTickets.add(telebot.types.KeyboardButton(i))
    elif mode == 4:
        for i in os.listdir(botDirectory + botTicketsDirectory):
            with open(botDirectory + botTicketsDirectory + i, "r") as file:
                if file.readline() == "randomized\n":
                    existingTickets.add(telebot.types.KeyboardButton(i))
    existingTickets.add("Back to ticket menu")
    return existingTickets


def IsUserInRandom(message):
    """
    :param message: message from user, function will take text from it
    :return: 0 if user is not in random, 1 if opposite
    """
    with open(botDirectory + botTicketsDirectory + message.text, "r+") as file:
        file.readline()
        while True:
            tempLine = file.readline()
            if tempLine == "":
                return 0
            if Parsers.ParseUsername(tempLine, 1) == message.from_user.username:
                return 1


def Notification(fileName):
    """
    sends message about position in the random

    :param fileName: path to ended random file
    """
    with open(botDirectory + botTicketsDirectory + fileName, "r") as file:
        content = file.readlines()
    content.remove(content[0])
    for num, i in enumerate(content):
        bot.send_message(int(Parsers.ParseUsername(i, 2)), "Random \"" +
                         fileName + "\" is ended\nYour place - " + str(num + 1))


@bot.message_handler(commands=['start'])
def FirstEnter(message):
    # checking if bots is set upped
    if not os.path.exists(botDirectory):
        CreateBotFiles()
        SetUserStatus(message.chat.id, 0)
        bot.send_message(
            message.chat.id, "Seems bot runs for the first time\nCheck folder and enter *master key*")
    elif CheckBanned(message) == 1:
        return
    # check if user already registered
    elif os.path.exists(botDirectory + botStatusDirectory + str(message.chat.id) + ".txt"):
        bot.send_message(message.chat.id, "You have already run the bot")
        return
    # registering new user
    else:
        bot.send_message(
            message.chat.id, "Please, enter your registration key")
        SetUserStatus(message.chat.id, "1")

# Registration handlers (appears when user talk to bot for the first time)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 0)
def MasterKeyHandler(message):
    with open(botDirectory + botMasterKeyFile) as file:
        key = file.readline()
    if key == message.text:
        bot.send_message(
            message.chat.id, "Success, admin rights are granted", reply_markup=main_keyboard)
        with open(botDirectory + botModeratorsFile, "a+") as file:
            file.write(str(message.chat.id) + "\n")
        SetUserStatus(message.chat.id, "-1")
    else:
        bot.send_message(
            message.chat.id, "Master key enter failed", reply_markup=None)
        SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 1)
def RegistrationKeyHandler(message):
    if CheckRegKey(message.text):
        bot.send_message(
            message.chat.id, "Access granted as user", reply_markup=main_keyboard)
        SetUserStatus(message.chat.id, "-1")
    else:
        bot.send_message(message.chat.id, "Wrong reg key")

# Exception handlers (handle some input that uses only in specific situations)


@bot.message_handler(func=lambda message: CheckBanned(message))
def SendAwayBannedHandler(message):  # Banned users wont be able to use bot
    bot.send_message(
        message.chat.id, "You are banned, your requests would not be processed")


@bot.message_handler(func=lambda message: message.text == "Waiting Input")
def WaitingInputHandler(message):  # Waiting input from user
    bot.send_message(message.chat.id, "Bot is waiting for input from you")

# Menu handlers (return to specific menu and sets user status to -1 AK idle)


@bot.message_handler(func=lambda message: message.text == "Back")
def BackHandler(message):  # Always returns to main menu
    bot.send_message(message.chat.id, "Back", reply_markup=main_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: message.text == "Back to ticket menu")
def BackToTicketMenuHandler(message):  # Always returns to ticket menu
    bot.send_message(message.chat.id, "Back to ticket menu",
                     reply_markup=ticketMenu_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: message.text == "Back to admin menu" and Parsers.IsUserAdmin(message.chat.id))
def BackToAdminMenuHandler(message):  # Always returns to admin menu
    bot.send_message(message.chat.id, "Back to admin menu",
                     reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, "-1")

# Main menu handlers


@bot.message_handler(func=lambda message: message.text == "Tickets" and GetUserStatus(message.chat.id) == -1)
def TicketsMenuHandler(message):
    bot.send_message(message.chat.id, "Showing tickets menu",
                     reply_markup=ticketMenu_keyboard)


@bot.message_handler(func=lambda message: message.text == "Basic randoms" and GetUserStatus(message.chat.id) == -1)
def BasicRandomsHandler(message):
    bot.send_message(message.chat.id, "Showing basic randoms",
                     reply_markup=basicRandomsMenu)


@bot.message_handler(func=lambda message: message.text == "Contacts" and GetUserStatus(message.chat.id) == -1)
def ContactsMenuHandler(message):
    with open(botDirectory + botContactsFile, "r") as file:
        bot.send_message(message.chat.id, file.read())


@bot.message_handler(func=lambda message: message.text == "Admin Panel" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def AdminPanelHandler(message):
    bot.send_message(message.chat.id, "Showing admin panel",
                     reply_markup=admin_keyboard)

# Basic randoms menu handlers


@bot.message_handler(func=lambda message: message.text == "Coin flip" and GetUserStatus(message.chat.id) == -1)
def CoinFlipHandler(message):
    bot.send_photo(message.chat.id, open(
        filesDirectory + randomSection.CoinFlip(), "rb"))


@bot.message_handler(func=lambda message: message.text == "Dice roll" and GetUserStatus(message.chat.id) == -1)
def DiceRollHandler(message):
    SetUserStatus(message.chat.id, "41")
    diceKeyboard = telebot.types.ReplyKeyboardMarkup()
    for i in range(1, 10, 3):
        diceKeyboard.add(str(i), str(i+1), str(i+2))
    diceKeyboard.add("Back")
    bot.send_message(
        message.chat.id, "Enter number of dices to roll", reply_markup=diceKeyboard)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 41 and message.text.isdigit())
def DiceRollResultHandler(message):
    if int(message.text) < 0:
        bot.send_message(message.chat.id, "Number of dices cannot be negative")
    elif int(message.text) > 10:
        bot.send_message(
            message.chat.id, "Number of dices cannot be more than 10")

    dices = randomSection.DiceRoll(int(message.text))
    media = []

    for photoPath in dices:
        with open(filesDirectory + photoPath, 'rb') as photo:
            file_data = photo.read()
            media.append(telebot.types.InputMediaPhoto(file_data))

    bot.send_media_group(message.chat.id, media)


# Ticket menu handlers


@bot.message_handler(func=lambda message: message.text == "Show tickets" and GetUserStatus(message.chat.id) == -1)
def ShowTicketsHandler(message):
    if Parsers.IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "There is no tickets", reply_markup=ticketMenu_keyboard)
        return
    for i in os.listdir(botDirectory + botTicketsDirectory):
        bot.send_message(message.chat.id, ShowUserTicketFile(
            str(i), message), reply_markup=ticketMenu_keyboard)


@bot.message_handler(func=lambda message: message.text == "Join random" and GetUserStatus(message.chat.id) == -1)
def JoinRandomHandler(message):
    if Parsers.IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "There is no tickets", reply_markup=ticketMenu_keyboard)
        return
    bot.send_message(message.chat.id, "Choose ticket (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 2))
    SetUserStatus(message.chat.id, "23")

# Ticket menu: Swap handlers


@bot.message_handler(func=lambda message: message.text == "Check swap requests" and GetUserStatus(message.chat.id) == -1)
def CheckSwapRequestsHandler(message):
    result = swapFunctions.ParsingSwapFile(message)
    if result[0] == 0:
        bot.send_message(
            message.chat.id, "You are not waiting for a swap and no one asking you for a swap", reply_markup=ticketMenu_keyboard)
    elif result[0] == 1:
        bot.send_message(message.chat.id, "You are asking to swap, info:\nTicket - " +
                         result[1] + "\n" + message.from_user.username + " <-> " + Parsers.ParseUsername(result[2], 1), reply_markup=answerUserSwapRequest)
        SetUserStatus(message.chat.id, "33")
    elif result[0] == 2:
        bot.send_message(message.chat.id, "Active request, info:\nTicket - " + result[1] + "\n" + Parsers.ParseUsername(
            result[2], 1) + " <-> " + message.from_user.username, reply_markup=answerIncomingSwap)
        SetUserStatus(message.chat.id, "34")


@bot.message_handler(func=lambda message: message.text == "Request swap" and GetUserStatus(message.chat.id) == -1)
def RequestSwapHandler(message):
    checkIfLocked = swapFunctions.ParsingSwapFile(message)
    if checkIfLocked[0] == 1:
        bot.send_message(message.chat.id, "You are already created swap request, delete it to unlock (in "
                                          "check swap request)", reply_markup=ticketMenu_keyboard)
        return
    elif checkIfLocked[0] == 2:
        bot.send_message(
            message.chat.id, "You have active request, check *check swap request*", reply_markup=ticketMenu_keyboard)
        return
    bot.send_message(
        message.chat.id, "Write *TicketName:Place to ask swap\nExample -- testing:3", reply_markup=requestingSwap)
    SetUserStatus(message.chat.id, 31)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 31)
def SwapHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    elif message.text == "Show tickets":
        if Parsers.IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=ticketMenu_keyboard)
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=requestingSwap)
        return
    elif message.text.find(":") == -1:
        bot.send_message(message.chat.id, "Invalid format")
        return
    elif not os.path.exists(botDirectory + botTicketsDirectory + Parsers.ParseUsername(message.text, 1)):
        bot.send_message(message.chat.id, "Ticket does not exist")
        return
    with open(botDirectory + botTicketsDirectory + Parsers.ParseUsername(message.text, 1)) as check:
        if check.readline() != "Randomized\n":
            bot.send_message(
                message.chat.id, "This ticket was not randomized")
            return
    # N is needed to be added due incompatibility to parsing function
    place = message.text + "N"
    place = Parsers.ParseUsername(place, 2)
    tempMes = message
    tempMes.text = Parsers.ParseUsername(message.text, 1)
    if IsUserInRandom(tempMes) == 0:
        bot.send_message(
            message.chat.id, "You didn't anticipate in this random")
        return
    if swapFunctions.CheckPosition(tempMes.text, message.chat.id, place) != 0:
        bot.send_message(message.chat.id, "Invalid position")
        return
    # getting info about user with whom we want to swap
    swUsername = str()
    swChatid = str()
    with open(botDirectory + botTicketsDirectory + tempMes.text, "r") as tempFile:
        for num, i in enumerate(tempFile.readlines()):
            if num == int(place):
                swUsername = Parsers.ParseUsername(i, 1)
                swChatid = Parsers.ParseUsername(i, 2)
                break
    # writing info to a swap file
    # tempMes.text = tempMes.text.replace("\n", "\\n") currently have bug with \n
    with open(botDirectory + botSwapFile, "a+") as swap:
        swap.write(tempMes.text + "~" + message.from_user.username + ":" +
                   str(message.chat.id) + "~" + swUsername + ":" + swChatid + "\n")
    bot.send_message(message.chat.id, "Swapped request added",
                     reply_markup=ticketMenu_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 33)
def SwapAcceptHandler(message):
    if swapFunctions.ParsingSwapFile(message)[0] == 0:
        bot.send_message(
            message.chat.id, "your swap request was deleted by user", reply_markup=ticketMenu_keyboard)
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Show tickets":
        if Parsers.IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=ticketMenu_keyboard)
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=answerUserSwapRequest)
    elif message.text == "Cancel request":
        bot.send_message(message.chat.id, "Okay, canceled",
                         reply_markup=ticketMenu_keyboard)
        swapFunctions.DeleteRequest(2, message.chat.id)
        SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 34)
def SwapDeclineHandler(message):
    if swapFunctions.ParsingSwapFile(message)[0] == 0:
        bot.send_message(
            message.chat.id, "your swap request was deleted by user", reply_markup=ticketMenu_keyboard)
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Show tickets":
        if Parsers.IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=ticketMenu_keyboard)
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=answerIncomingSwap)
    elif message.text == "Deny swap":
        bot.send_message(message.chat.id, "Okay denied",
                         reply_markup=ticketMenu_keyboard)
        swapFunctions.DeleteRequest(2, message.chat.id)
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Accept swap":
        result = swapFunctions.ParsingSwapFile(message)
        if result == 0:
            bot.send_message(message.chat.id, "error")
        swapFunctions.SwapUsers(
            result[1], result[2], message.from_user.username, str(message.chat.id))
        bot.send_message(message.chat.id, "Okay, swapped",
                         reply_markup=ticketMenu_keyboard)
        swapFunctions.DeleteRequest(
            2, Parsers.ParseUsername(str(message.chat.id), 2))
        SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: message.text == "Change master key" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def ChangeMasterKeyHandler(message):
    SetUserStatus(message.chat.id, 10)
    bot.send_message(
        message.chat.id, "Enter new master key", reply_markup=waitingInput)


@bot.message_handler(func=lambda message: message.text == "Create registration key" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def CreateRegistrationKeyHandler(message):
    newKey = randomSection.GenerateRegKey()
    bot.send_message(
        message.chat.id, "Successfully generated key:\n" + newKey, reply_markup=admin_keyboard)


@bot.message_handler(func=lambda message: message.text == "Delete registration key" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def DeleteRegistrationKeyHandler(message):
    with open(botDirectory + botRegKeyFile, "r") as files:
        existingKeys = files.read().split("\n")
        existingKeys.pop()
        bot.send_message(
            message.chat.id, "Enter key that you want to delete", reply_markup=waitingInput)
        for i in existingKeys:
            bot.send_message(message.chat.id, i)
        SetUserStatus(message.chat.id, "11")


@bot.message_handler(func=lambda message: message.text == "Start random (adm)" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def StartRandomHandler(message):
    if Parsers.IsThereTickets() == 0:
        bot.send_message(message.chat.id, "There is no tickets")
        return
    SetUserStatus(message.chat.id, "24")
    bot.send_message(message.chat.id, "Select ticket which you should activate (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 3))


@bot.message_handler(func=lambda message: message.text == "Create ticket (adm)" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def CreateTicketHandler(message):
    bot.send_message(
        message.chat.id, "Enter name of the event or use keyboard", reply_markup=waitingInput)
    SetUserStatus(message.chat.id, "21")


@bot.message_handler(func=lambda message: message.text == "Delete ticket (adm)" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def DeleteTicketHandler(message):
    if Parsers.IsThereTickets() == 0:
        bot.send_message(
            message.chat.id, "no tickets found", reply_markup=ticketMenu_keyboard)
        return
    bot.send_message(message.chat.id, "Enter ticket to delete or choose cancel (keyboard)",
                     reply_markup=GetTicketsKeyboard(message, 1))
    SetUserStatus(message.chat.id, "22")


@bot.message_handler(func=lambda message: message.text == "Ban user" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def BanUserHandler(message):
    SetUserStatus(message.chat.id, "12")
    bot.send_message(
        message.chat.id, "Enter user chat id", reply_markup=waitingInput)


@bot.message_handler(func=lambda message: message.text == "Modify contacts info" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def ModifyContactsHandler(message):
    with open(botDirectory + botContactsFile, "r") as file:
        contacts = file.read()
        bot.send_message(message.chat.id, "Current contacts:\n\n" +
                         contacts + "\n\nEnter new message", reply_markup=waitingInput),
    SetUserStatus(message.chat.id, "13")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 10)
def ChangeMasterKeyHandler(message):
    bot.send_message(message.chat.id, "Successfully changed!",
                     reply_markup=main_keyboard)
    with open(botDirectory + botMasterKeyFile, "w") as file:
        file.write(message.text)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 11)
def DeleteRegistrationKeyHandler(message):
    with open(botDirectory + botRegKeyFile, "r") as file:
        existingKeys = file.read().split("\n")
    existingKeys.pop()
    try:
        existingKeys.remove(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Key not found")
        return
    with open(botDirectory + botRegKeyFile, "w") as file:
        for i in existingKeys:
            file.write(i + "\n")
    bot.send_message(message.chat.id, "Successfully deleted",
                     reply_markup=main_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 12)
def BanUserHandler(message):
    with open(botDirectory + botBannedFile, "a+") as banning:
        banning.write(message.text + "\n")
    bot.send_message(message.chat.id, message.text +
                     " was added to a ban file", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 21)
def CreateTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    elif os.path.exists(botDirectory + botTicketsDirectory + str(message.text)):
        bot.send_message(
            message.chat.id, "Sorry, such event is already exist")
        return
    with open(botDirectory + botTicketsDirectory + message.text, "w") as ticketFile:
        ticketFile.write("Active\n")
    bot.send_message(message.chat.id, "Created!")
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 22)
def DeleteTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    if os.path.exists(botDirectory + botTicketsDirectory + str(message.text)):
        os.remove(botDirectory + botTicketsDirectory + str(message.text))
        bot.send_message(message.chat.id, "Deleted!",
                         reply_markup=ticketMenu_keyboard)
        SetUserStatus(message.chat.id, "-1")
        return
    else:
        bot.send_message(message.chat.id, "File not found")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 23)
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
                     reply_markup=ticketMenu_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 24)
def RandomTicketHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    elif not os.path.exists(botDirectory + botTicketsDirectory + message.text):
        bot.send_message(message.chat.id, "Ticket does not exist")
        return
    # checking some conditions
    with open(botDirectory + botTicketsDirectory + message.text, "r") as preRandom:
        if not preRandom.readline() == "Active\n":
            bot.send_message(
                message.chat.id, "This ticket is already randomized")
            return
        if preRandom.readline() == "":
            bot.send_message(
                message.chat.id, "there is no users for random")
            return
    with open(botDirectory + botTicketsDirectory + message.text, "r") as gettingUsers:
        usersInRandom = gettingUsers.readlines()
        usersInRandom.remove(usersInRandom[0])
    randomSection.PerformingRandom(message.text, usersInRandom)
    bot.send_message(message.chat.id, "Random successfully done!",
                     reply_markup=ticketMenu_keyboard)
    Notification(message.text)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 13)
def ChangeContactsHandler(message):
    with open(botDirectory + botContactsFile, "w") as file:
        file.write(message.text)
    bot.send_message(
        message.chat.id, "Contacts successfully changed", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, "-1")


@bot.message_handler(func=lambda message: message.text == "Unban user" and GetUserStatus(message.chat.id) == -1 and Parsers.IsUserAdmin(message.chat.id))
def UnbanUserHandler(message):
    bans = Parsers.GetBannedUsers()
    if len(bans) == 1:
        bot.send_message(message.chat.id, "No banned users")
        return
    # creating keyboard
    bannedUsersKeyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True)
    for i in bans:
        bannedUsersKeyboard.add(i)
    bannedUsersKeyboard.add("Back to admin menu")
    bot.send_message(message.chat.id, "Choose user to unban",
                     reply_markup=bannedUsersKeyboard)
    SetUserStatus(message.chat.id, 14)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 14)
def UnbanConfirmationHandler(message):
    with open(botDirectory + botBannedFile, "r") as file:
        bannedUsers = file.readlines()
    bannedUsers.remove(message.text + "\n")
    with open(botDirectory + botBannedFile, "w") as file:
        file.writelines(bannedUsers)
    bot.send_message(message.chat.id, "User successfully unbanned",
                     reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, -1)


@bot.message_handler(content_types=['text'])
def Answering(message):
    bot.send_message(message.chat.id, "Unknown command",
                     reply_markup=main_keyboard)
    SetUserStatus(message.chat.id, -1)


bot.polling(none_stop=True)
