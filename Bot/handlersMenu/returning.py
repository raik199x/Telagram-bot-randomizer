from Bot.shared.functions import *
from Bot.Keyboards.static import admin_keyboard, main_keyboard, basicRandomsMenu
from Bot.Keyboards.dynamic import GetTicketsMenuKeyboard
from Bot.Parsers.userProperties import IsUserAdmin


@bot.message_handler(func=lambda message: message.text == "Back")
def BackHandler(message):  # Always returns to main menu
    bot.send_message(message.chat.id, "Back", reply_markup=main_keyboard)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Back to ticket menu")
def BackToTicketMenuHandler(message):  # Always returns to ticket menu
    bot.send_message(message.chat.id, "Back to ticket menu",
                     reply_markup=GetTicketsMenuKeyboard(message.chat.id))
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Back to admin menu" and IsUserAdmin(message.chat.id))
def BackToAdminMenuHandler(message):  # Always returns to admin menu
    bot.send_message(message.chat.id, "Back to admin menu",
                     reply_markup=admin_keyboard)
    SetUserStatus(message.chat.id, user_idle)


@bot.message_handler(func=lambda message: message.text == "Back to basic randoms")
def BackToBasicRandomsHandler(message):  # Always returns to basic randoms
    bot.send_message(message.chat.id, "Back to basic randoms",
                     reply_markup=basicRandomsMenu)
    SetUserStatus(message.chat.id, user_idle)
