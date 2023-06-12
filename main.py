from Bot.shared import constants as const
from Bot.userFirstEncounter.encountering import *
from Bot.handlersMenu.returning import *
from Bot.handlersMenu.menu import *
from Bot.handlersTicket.tickets import *
from Bot.handlersSwap.swap import *
from Bot.handlersRandom.handlers import *
from Bot.handlersAdminPanel.panel import *

# TODO:
# > Deleting reg key: check if key exists, if not - send message, if yes - show existing keys
# > Swap: add more user-friendly interface
# > add Unban user function
# > make more files for the project
# > get admin using master key
# > make main keyboard dynamic (add admin panel if user is admin)

# all text messages (DEBUG STATE)
@const.bot.message_handler(func=lambda message: message.text == "whoami" and GetUserStatus(message.chat.id) == user_idle)
def DEBUG(message):
    const.bot.send_message(message.chat.id, "Your chat id: " + str(message.chat.id) + "\n")

if __name__ == '__main__':
    if bot.token == None:
        print("Error: token is not set")
        exit(1)
    const.bot.polling(none_stop=True)
