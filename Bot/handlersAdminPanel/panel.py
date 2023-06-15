from Bot.shared.constants import *
from Bot.shared.functions import GetUserStatus, SetUserStatus
from Bot.Keyboards.static import admin_keyboard
from Bot.Keyboards.dynamic import GetWaitingInputKeyboard, GetMainKeyboard
from Bot.randomFunctions.randoms import GenerateRegKey
from Bot.Parsers.userProperties import IsUserAdmin
from os.path import getsize


@bot.message_handler(func=lambda message: message.text == "Change master key" and GetUserStatus(message.chat.id) == user_idle)
def ChangeMasterKey(message):
    SetUserStatus(message.chat.id, admin_changing_master_key)
    bot.send_message(
        message.chat.id, "Enter new master key", reply_markup=GetWaitingInputKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_changing_master_key)
def ChangeMasterKeyHandler(message):
    bot.send_message(message.chat.id, "Successfully changed!",
                     reply_markup=GetMainKeyboard(message.chat.id))
    with open(botDirectory + botMasterKeyFile, "w") as file:
        file.write(message.text)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Create registration key" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def CreateRegistrationKeyHandler(message):
    newKey = GenerateRegKey()
    bot.send_message(
        message.chat.id, "Successfully generated key:\n" + newKey, reply_markup=admin_keyboard)


@bot.message_handler(func=lambda message: message.text == "Show registration keys" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def ShowingRegistrationKeysHandler(message):
    if getsize(botDirectory + botRegKeyFile) == 0:
        bot.send_message(message.chat.id, "There are no registration keys")
    with open(botDirectory + botRegKeyFile, "r") as file:
        sendMessage = "Registration keys:\n\n"
        while (line := file.readline()) != "":
            sendMessage += line + "\n"
    bot.send_message(message.chat.id, sendMessage, reply_markup=admin_keyboard)


@bot.message_handler(func=lambda message: message.text == "Delete registration key" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def AskDeletingRegistrationKeyHandler(message):
    # First, check if any key exist
    if getsize(botDirectory + botRegKeyFile) == 0:
        bot.send_message(message.chat.id, "There are no registration keys")
        return
    # Otherwise we ask user to write key
    SetUserStatus(message.chat.id, admin_deleting_reg_key)
    bot.send_message(
        message.chat.id, "Enter registration key to delete", reply_markup=GetWaitingInputKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_deleting_reg_key)
def DeletingRegistrationKeyHandler(message):
    # First, check if any key exist
    if getsize(botDirectory + botRegKeyFile) == 0:
        bot.send_message(
            message.chat.id, "At the moment, there is no registration keys")
        SetUserStatus(message.chat.id, user_idle)
        return
    # Now we check if such key in file
    with open(botDirectory + botRegKeyFile, "r") as file:
        if message.text not in file.read():
            bot.send_message(message.chat.id, "There is no such key")
            SetUserStatus(message.chat.id, user_idle)
            return
    # If key exist, we delete it
    with open(botDirectory + botRegKeyFile, "r") as file:
        lines = file.readlines()
    with open(botDirectory + botRegKeyFile, "w") as file:
        for line in lines:
            if line.strip("\n") != message.text:
                file.write(line)
    bot.send_message(message.chat.id, "Successfully deleted key",
                     reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Ban user" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def BanUserHandler(message):
    SetUserStatus(message.chat.id, admin_banning_user)
    bot.send_message(
        message.chat.id, "Enter user chat id", reply_markup=GetWaitingInputKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_banning_user)
def BanUserHandler(message):
    with open(botDirectory + botBannedFile, "a+") as banning:
        banning.write(message.text + "\n")
    bot.send_message(message.chat.id, message.text +
                     " was added to a ban file", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Unban user" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def AskUnbanUserHandler(message):
    # First check if there banned users
    if getsize(botDirectory + botBannedFile) == 0:
        bot.send_message(message.chat.id, "There are no banned users")
        return
    # Now we send all banned users
    with open(botDirectory + botBannedFile, "r") as file:
        sendMessage = "Banned users:\n\n"
        while (line := file.readline()) != "":
            sendMessage += line + "\n"
    bot.send_message(message.chat.id, sendMessage)
    # Now we ask user to write id
    SetUserStatus(message.chat.id, admin_unbanning_user)
    bot.send_message(message.chat.id, "Enter user chat id",
                     reply_markup=GetWaitingInputKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_unbanning_user)
def UnbanUserHandler(message):
    # First check if there banned users
    if getsize(botDirectory + botBannedFile) == 0:
        bot.send_message(message.chat.id, "Now there are no banned users")
        SetUserStatus(message.chat.id, user_idle)
        return
    # Now we check if such user in file
    with open(botDirectory + botBannedFile, "r") as file:
        if message.text not in file.read():
            bot.send_message(message.chat.id, "There is no such user")
            SetUserStatus(message.chat.id, user_idle)
            return
    # If user exist, we delete it
    with open(botDirectory + botBannedFile, "r") as file:
        lines = file.readlines()
    with open(botDirectory + botBannedFile, "w") as file:
        for line in lines:
            if line.strip("\n") != message.text:
                file.write(line)
    bot.send_message(message.chat.id, "Successfully unbanned user",
                     reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Modify contacts info" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def ModifyContactsHandler(message):
    with open(botDirectory + botContactsFile, "r") as file:
        contacts = file.read()
        bot.send_message(message.chat.id, "Current contacts:\n\n" +
                         contacts + "\n\nEnter new message", reply_markup=GetWaitingInputKeyboard(message.chat.id)),
    SetUserStatus(message.chat.id, admin_modifying_contacts)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_modifying_contacts)
def ChangeContactsHandler(message):
    with open(botDirectory + botContactsFile, "w") as file:
        file.write(message.text)
    bot.send_message(
        message.chat.id, "Contacts successfully changed", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)
