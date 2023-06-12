import os
import telebot

botDirectory = "BotFiles/"
botTicketsDirectory = "tickets/"
botStatusDirectory = "currentStatus/"

botModeratorsFile = "mods.txt"
botBannedFile = "bans.txt"
botSwapFile = "swap.txt"
botContactsFile = "contacts.txt"
botMasterKeyFile = "master_key.txt"
botRegKeyFile = "reg_keys.txt"

filesDirectory = "data/"

# bot token (export TOKEN=your_token_value) or just hardcode it
bot = telebot.TeleBot(os.getenv("TOKEN"))

user_not_found = 404

user_enter_master_key = 0
user_enter_reg_key = 1
# ----------------------------
# ADMIN MENU
admin_changing_master_key = 10
admin_deleting_reg_key = 11
admin_banning_user = 12
admin_modifying_contacts = 13
admin_unbanning_user = 14
# ----------------------------
# TICKETS
admin_creating_ticket = 21
admin_deleting_ticket = 22
user_joining_ticket = 23
admin_starting_random = 24
# ----------------------------
# SWAPPING
user_writing_swap_rule = 31
user_requested_swap = 32
user_requested_swap_with_you = 33
# ----------------------------
# BASIC RANDOMS
user_dice_roll = 41
user_random_number = 42
user_custom_list_random = 43
# ----------------------------
# IDLE
user_idle = -1
