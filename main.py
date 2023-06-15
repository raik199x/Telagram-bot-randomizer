from Bot.shared import constants as const
from Bot.userFirstEncounter.encountering import *
from Bot.handlersMenu.returning import *
from Bot.handlersMenu.menu import *
from Bot.handlersTicket.tickets import *
from Bot.handlersSwap.swap import *
from Bot.handlersRandom.handlers import *
from Bot.handlersAdminPanel.panel import *

# TODO:
# > Swap: add more user-friendly interface
# > get admin using master key
# > console logging?

# all text messages (DEBUG STATE)
@const.bot.message_handler(func=lambda message: message.text == "whoami" and GetUserStatus(message.chat.id) == user_idle)
def DEBUG(message):
    const.bot.send_message(message.chat.id, "Your chat id: " + str(message.chat.id) + "\n")

if __name__ == '__main__':
    if bot.token == None:
        print("Error: token is not set")
        exit(1)
    print("Bot is running")
    const.bot.polling(none_stop=True)
