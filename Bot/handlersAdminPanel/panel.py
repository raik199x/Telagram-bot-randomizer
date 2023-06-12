from Bot.shared.constants import *
from Bot.shared.functions import GetUserStatus, SetUserStatus
from Bot.Keyboards.static import waitingInput, main_keyboard, admin_keyboard
from Bot.randomFunctions.randoms import GenerateRegKey
from Bot.Parsers.userProperties import IsUserAdmin


@bot.message_handler(func=lambda message: message.text == "Change master key" and GetUserStatus(message.chat.id) == user_idle)
def ChangeMasterKey(message):
    SetUserStatus(message.chat.id, admin_changing_master_key)
    bot.send_message(
        message.chat.id, "Enter new master key", reply_markup=waitingInput)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_changing_master_key)
def ChangeMasterKeyHandler(message):
    bot.send_message(message.chat.id, "Successfully changed!",
                     reply_markup=main_keyboard)
    with open(botDirectory + botMasterKeyFile, "w") as file:
        file.write(message.text)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Create registration key" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def CreateRegistrationKeyHandler(message):
    newKey = GenerateRegKey()
    bot.send_message(
        message.chat.id, "Successfully generated key:\n" + newKey, reply_markup=admin_keyboard)


# TODO: add deleting reg key function
@bot.message_handler(func=lambda message: message.text == "Delete registration key" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def CreateRegistrationKeyHandler(message):
    pass


@bot.message_handler(func=lambda message: message.text == "Ban user" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def BanUserHandler(message):
    SetUserStatus(message.chat.id, admin_banning_user)
    bot.send_message(
        message.chat.id, "Enter user chat id", reply_markup=waitingInput)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_banning_user)
def BanUserHandler(message):
    with open(botDirectory + botBannedFile, "a+") as banning:
        banning.write(message.text + "\n")
    bot.send_message(message.chat.id, message.text +
                     " was added to a ban file", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)


# TODO: add unbanning user function
@bot.message_handler(func=lambda message: message.text == "Unban user" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def UnbanUserHandler(message):
    pass


@bot.message_handler(func=lambda message: message.text == "Modify contacts info" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def ModifyContactsHandler(message):
    with open(botDirectory + botContactsFile, "r") as file:
        contacts = file.read()
        bot.send_message(message.chat.id, "Current contacts:\n\n" +
                         contacts + "\n\nEnter new message", reply_markup=waitingInput),
    SetUserStatus(message.chat.id, admin_modifying_contacts)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == admin_modifying_contacts)
def ChangeContactsHandler(message):
    with open(botDirectory + botContactsFile, "w") as file:
        file.write(message.text)
    bot.send_message(
        message.chat.id, "Contacts successfully changed", reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)
