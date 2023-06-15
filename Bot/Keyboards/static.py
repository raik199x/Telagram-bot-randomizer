from telebot import types


admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add("Change master key")
admin_keyboard.add("Create registration key",
                   "Show registration keys", "Delete registration key")
admin_keyboard.add("Ban user", "Unban user")
admin_keyboard.add("Modify contacts info")
admin_keyboard.add("Back")


answerIncomingSwap = types.ReplyKeyboardMarkup(resize_keyboard=True)
answerIncomingSwap.add("Show tickets")
answerIncomingSwap.add("Accept swap", "Deny swap")
answerIncomingSwap.add("Back to ticket menu")


answerUserSwapRequest = types.ReplyKeyboardMarkup(resize_keyboard=True)
answerUserSwapRequest.add("Show tickets")
answerUserSwapRequest.add("Cancel request", "Back to ticket menu")


requestingSwap = types.ReplyKeyboardMarkup(resize_keyboard=True)
requestingSwap.add("Waiting Input")
requestingSwap.add("Show tickets")
requestingSwap.add("Back to ticket menu")


basicRandomsMenu = types.ReplyKeyboardMarkup(resize_keyboard=True)
basicRandomsMenu.add("Coin flip", "Dice roll")
basicRandomsMenu.add("Random number")
basicRandomsMenu.add("Back")
