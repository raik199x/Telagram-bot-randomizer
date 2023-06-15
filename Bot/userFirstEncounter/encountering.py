from Bot.shared.constants import *
from Bot.shared.functions import *
from Bot.DirectoryManip.fileCheckers import CheckWorkingDirectory
from Bot.Parsers.keyVerification import CheckRegKey, CheckMasterKey
from Bot.Keyboards.dynamic import GetMainKeyboard
from Bot.DirectoryManip.fileOperations import AddAdmin


@bot.message_handler(commands=['start'])
def start(message):
    if CheckWorkingDirectory() == "Setup":
        SetUserStatus(message.chat.id, user_enter_master_key)
        bot.send_message(
            message.chat.id, "Enter master key (Check bot files):")
    elif GetUserStatus(message.chat.id) == user_not_found:
        SetUserStatus(message.chat.id, user_enter_reg_key)
        bot.send_message(message.chat.id, "Enter registration key:")
    else:
        bot.send_message(message.chat.id, "You are already registered!")


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 0)
def MasterKeyHandler(message):
    if CheckMasterKey(message.text):
        bot.send_message(
            message.chat.id, "Access granted as admin", reply_markup=GetMainKeyboard(message.chat.id))
        SetUserStatus(message.chat.id, user_idle)
        AddAdmin(message.chat.id)
    else:
        bot.send_message(
            message.chat.id, "Master key enter failed", reply_markup=None)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == 1)
def RegistrationKeyHandler(message):
    if CheckRegKey(message.text):
        bot.send_message(
            message.chat.id, "Access granted as user", reply_markup=GetMainKeyboard(message.chat.id))
        SetUserStatus(message.chat.id, user_idle)
    else:
        bot.send_message(message.chat.id, "Wrong reg key")
