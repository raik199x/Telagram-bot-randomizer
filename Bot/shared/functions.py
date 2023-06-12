from Bot.shared.constants import *


def SetUserStatus(chatId, status):
    """
    sets users status into given one (if such user doesn't exist, creates new one)

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
        return user_not_found
    status = file.readline()
    file.close()
    return int(status)


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
