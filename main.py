from Bot.shared import constants as const
from Bot.userFirstEncounter.encountering import *
from Bot.handlersMenu.returning import *
from Bot.handlersMenu.menu import *
from Bot.handlersTicket.tickets import *
from Bot.handlersSwap.swap import *
from Bot.handlersRandom.handlers import *
from Bot.handlersAdminPanel.panel import *
from Bot.logger.setup import logger

# TODO:
# > Swap: add more user-friendly interface
# > get admin using master key


if __name__ == '__main__':
    if bot.token == None:
        logger.error("Bot token is not set")
        exit(1)
    logger.info("Bot started")
    const.bot.polling(none_stop=True)
