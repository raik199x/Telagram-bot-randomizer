# Bot-randomizer

Telegram bot that allow you to create tickets for randomizing events

Bot is in beta version and bugs may be found, if you found something write me somewhere.

---

## Motivation

In moments when you need to make a queue to somewhere with your team, the most honest and less time consuming method is randomizing.

For that purpose you can use this bot for half-automated randomization.

Since bot runs through telegram, you don't need to have static ip and your bot will be available as long as it is enabled.

---

## How it works?

When you set up your bot, you can create reg token for your team so everyone can join bot.

Then you can create ticket like "Queue to clean room" and everyone (who need or want) can join that ticket, when
everyone joined random, admins can start random and everyone get notification from bot which place did he\she get.

If someone don't like his position, he\she can try to create swap request with someone.

---

## Installation

First of all, you need to create your bot in chat with [bot father](https://telegram.me/BotFather) and obtain his token.

Then you need to create environment variable named *TOKEN* that will be equal to your token (ex. ```export TOKEN=your_token_value```) or modify *main.py* and insert your token.

To run this bot you need to install requirements:

 pip3 install -r requirements.txt
  
then clone this repository and simply run bot

 python3 main.py
  
To make it available for a long time i installed [Termux](https://f-droid.org/packages/com.termux/) on my android phone and run bot on it.

---

## Contacts

Mail: <raik199x@mail.ru>

Telegram: @raik199x
