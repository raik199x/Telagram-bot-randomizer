from Bot.shared.constants import *
from Bot.shared.functions import GetUserStatus
from Bot.Keyboards.static import admin_keyboard, basicRandomsMenu
from Bot.Keyboards.dynamic import GetTicketsMenuKeyboard
from Bot.Parsers.userProperties import IsUserAdmin


@bot.message_handler(func=lambda message: message.text == "Tickets" and GetUserStatus(message.chat.id) == user_idle)
def TicketsMenuHandler(message):
    bot.send_message(message.chat.id, "Showing tickets menu",
                     reply_markup=GetTicketsMenuKeyboard(message.chat.id))


@bot.message_handler(func=lambda message: message.text == "Basic randoms" and GetUserStatus(message.chat.id) == user_idle)
def BasicRandomsHandler(message):
    bot.send_message(message.chat.id, "Showing basic randoms",
                     reply_markup=basicRandomsMenu)


@bot.message_handler(func=lambda message: message.text == "Contacts" and GetUserStatus(message.chat.id) == user_idle)
def ContactsMenuHandler(message):
    with open(botDirectory + botContactsFile, "r") as file:
        bot.send_message(message.chat.id, file.read())


@bot.message_handler(func=lambda message: message.text == "Admin Panel" and GetUserStatus(message.chat.id) == user_idle and IsUserAdmin(message.chat.id))
def AdminPanelHandler(message):
    bot.send_message(message.chat.id, "Showing admin panel",
                     reply_markup=admin_keyboard)
