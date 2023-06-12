from Bot.shared.constants import *
from Bot.shared.functions import GetUserStatus, SetUserStatus
from Bot.randomFunctions.randoms import CoinFlip, DiceRoll, RandomNumber
from Bot.Keyboards.static import waitingInput


@bot.message_handler(func=lambda message: message.text == "Coin flip" and GetUserStatus(message.chat.id) == user_idle)
def CoinFlipHandler(message):
    bot.send_photo(message.chat.id, open(
        filesDirectory + CoinFlip(), "rb"))


@bot.message_handler(func=lambda message: message.text == "Dice roll" and GetUserStatus(message.chat.id) == user_idle)
def DiceRollHandler(message):
    SetUserStatus(message.chat.id, user_dice_roll)
    diceKeyboard = telebot.types.ReplyKeyboardMarkup()
    for i in range(1, 10, 3):
        diceKeyboard.add(str(i), str(i+1), str(i+2))
    diceKeyboard.add("Back")
    bot.send_message(
        message.chat.id, "Enter number of dices to roll", reply_markup=diceKeyboard)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_dice_roll and message.text.isdigit())
def DiceRollResultHandler(message):
    if int(message.text) < 0:
        bot.send_message(message.chat.id, "Number of dices cannot be negative")
    elif int(message.text) > 10:
        bot.send_message(
            message.chat.id, "Number of dices cannot be more than 10")

    dices = DiceRoll(int(message.text))
    media = []

    for photoPath in dices:
        with open(filesDirectory + photoPath, 'rb') as photo:
            file_data = photo.read()
            media.append(telebot.types.InputMediaPhoto(file_data))

    bot.send_media_group(message.chat.id, media)


@bot.message_handler(func=lambda message: message.text == "Random number" and GetUserStatus(message.chat.id) == user_idle)
def RandomNumberHandler(message):
    SetUserStatus(message.chat.id, user_random_number)
    bot.send_message(
        message.chat.id, "Enter range (from:to)", reply_markup=waitingInput)


@bot.message_handler(func=lambda message: GetUserStatus(message.chat.id) == user_random_number)
def RandomNumberResultHandler(message):
    # first if double point here
    if message.text.count(":") != 1:
        bot.send_message(message.chat.id, "Wrong input, format: 'from:to'")
        return
    # then that both numbers are digits
    if not message.text.split(":")[0].isdigit() or not message.text.split(":")[1].isdigit():
        bot.send_message(
            message.chat.id, "Wrong input, both numbers must be digits")
        return
    # then that first number is less than second
    if int(message.text.split(":")[0]) > int(message.text.split(":")[1]):
        bot.send_message(
            message.chat.id, "Wrong input, first number must be less than second")
        return
    # then that both numbers are in range
    if int(message.text.split(":")[0]) < 0 or int(message.text.split(":")[1]) > 1000000:
        bot.send_message(
            message.chat.id, "Wrong input, both numbers must be in range 0-1000000")
        return
    result = RandomNumber(message.text.split(
        ":")[0], message.text.split(":")[1])
    bot.send_message(message.chat.id, result, reply_markup=waitingInput)
