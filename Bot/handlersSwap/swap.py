from Bot.shared.constants import *
from Bot.shared.functions import GetUserStatus, SetUserStatus, SecurityFileCheck
from Bot.Keyboards.dynamic import GetTicketsMenuKeyboard
from Bot.Keyboards.static import answerIncomingSwap, answerUserSwapRequest, requestingSwap
from Bot.Parsers.lineParsers import ParseUsername
from Bot.Parsers.statements import IsThereTickets
from Bot.Parsers.userProperties import IsUserInRandom
from Bot.handlersSwap.processingFunctions import ParsingSwapFile, CheckPosition, DeleteRequest, SwapUsers
from Bot.handlersTicket.processingFunctions import ShowUserTicketFile



@bot.message_handler(func=lambda message: message.text == "Check swap requests" and GetUserStatus(message.chat.id) == user_idle)
def CheckSwapRequestsHandler(message):
    result = ParsingSwapFile(message)
    if result[0] == 0:
        bot.send_message(
            message.chat.id, "You are not waiting for a swap and no one asking you for a swap", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    elif result[0] == 1:
        bot.send_message(message.chat.id, "You are asking to swap, info:\nTicket - " +
                         result[1] + "\n" + message.from_user.username + " <-> " + ParseUsername(result[2], 1), reply_markup=answerUserSwapRequest)
        SetUserStatus(message.chat.id, user_requested_swap)
    elif result[0] == 2:
        bot.send_message(message.chat.id, "Active request, info:\nTicket - " + result[1] + "\n" + ParseUsername(
            result[2], 1) + " <-> " + message.from_user.username, reply_markup=answerIncomingSwap)
        SetUserStatus(message.chat.id, user_requested_swap_with_you)


@bot.message_handler(func=lambda message: message.text == "Request swap" and GetUserStatus(message.chat.id) == user_idle)
def RequestSwapHandler(message):
    checkIfLocked = ParsingSwapFile(message)
    if checkIfLocked[0] == 1:
        bot.send_message(message.chat.id, "You are already created swap request, delete it to unlock (in "
                                          "check swap request)", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        return
    elif checkIfLocked[0] == 2:
        bot.send_message(
            message.chat.id, "You have active request, check *check swap request*", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        return
    bot.send_message(
        message.chat.id, "Write *TicketName:Place to ask swap\nExample -- testing:3", reply_markup=requestingSwap)
    SetUserStatus(message.chat.id, user_writing_swap_rule)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_writing_swap_rule)
def SwapHandler(message):
    if SecurityFileCheck(message) == 1:
        return
    elif message.text == "Show tickets":
        if IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=requestingSwap)
        return
    elif message.text.find(":") == -1:
        bot.send_message(message.chat.id, "Invalid format")
        return
    elif not os.path.exists(botDirectory + botTicketsDirectory + ParseUsername(message.text, 1)):
        bot.send_message(message.chat.id, "Ticket does not exist")
        return
    with open(botDirectory + botTicketsDirectory + ParseUsername(message.text, 1)) as check:
        if check.readline() != "Randomized\n":
            bot.send_message(
                message.chat.id, "This ticket was not randomized")
            return
    # N is needed to be added due incompatibility to parsing function
    place = message.text + "N"
    place = ParseUsername(place, 2)
    tempMes = message
    tempMes.text = ParseUsername(message.text, 1)
    if IsUserInRandom(tempMes) == 0:
        bot.send_message(
            message.chat.id, "You didn't anticipate in this random")
        return
    if CheckPosition(tempMes.text, message.chat.id, place) != 0:
        bot.send_message(message.chat.id, "Invalid position")
        return
    # getting info about user with whom we want to swap
    swUsername = str()
    swChatid = str()
    with open(botDirectory + botTicketsDirectory + tempMes.text, "r") as tempFile:
        for num, i in enumerate(tempFile.readlines()):
            if num == int(place):
                swUsername = ParseUsername(i, 1)
                swChatid = ParseUsername(i, 2)
                break
    # writing info to a swap file
    # tempMes.text = tempMes.text.replace("\n", "\\n") currently have bug with \n
    with open(botDirectory + botSwapFile, "a+") as swap:
        swap.write(tempMes.text + "~" + message.from_user.username + ":" +
                   str(message.chat.id) + "~" + swUsername + ":" + swChatid + "\n")
    bot.send_message(message.chat.id, "Swapped request added",
                     reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_requested_swap)
def SwapAcceptHandler(message):
    if ParsingSwapFile(message)[0] == 0:
        bot.send_message(
            message.chat.id, "your swap request was deleted by user", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Show tickets":
        if IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=answerUserSwapRequest)
    elif message.text == "Cancel request":
        bot.send_message(message.chat.id, "Okay, canceled",
                         reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        DeleteRequest(2, message.chat.id)
        SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_requested_swap_with_you)
def SwapDeclineHandler(message):
    if ParsingSwapFile(message)[0] == 0:
        bot.send_message(
            message.chat.id, "your swap request was deleted by user", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Show tickets":
        if IsThereTickets() == 0:
            bot.send_message(message.chat.id, "There is no tickets\nIf you see this, it's probably a bug, contact "
                                              "with admins", reply_markup=GetTicketsMenuKeyboard(message.chat.id))
            return
        for i in os.listdir(botDirectory + botTicketsDirectory):
            bot.send_message(message.chat.id, ShowUserTicketFile(
                str(i), message), reply_markup=answerIncomingSwap)
    elif message.text == "Deny swap":
        bot.send_message(message.chat.id, "Okay denied",
                         reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        DeleteRequest(2, message.chat.id)
        SetUserStatus(message.chat.id, "-1")
    elif message.text == "Accept swap":
        result = ParsingSwapFile(message)
        if result == 0:
            bot.send_message(message.chat.id, "error")
        SwapUsers(
            result[1], result[2], message.from_user.username, str(message.chat.id))
        bot.send_message(message.chat.id, "Okay, swapped",
                         reply_markup=GetTicketsMenuKeyboard(message.chat.id))
        DeleteRequest(
            2, ParseUsername(str(message.chat.id), 2))
        SetUserStatus(message.chat.id, "-1")