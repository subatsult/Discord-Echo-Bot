# Discord Echo Bot

## Description

This is a Discord bot that serves two primary functions:
1. **Avatar Sender**: Every 10 seconds, the bot sends the avatar of the most recently mentioned user to the channel.
2. **Random Reactions**: Every 5 seconds, the bot sends a random emoji to the last channel it interacted with and reacts to messages where it was mentioned with a random emoji.

The bot also includes a translation feature that translates messages between English and Russian, depending on the detected language.

## Features

- **Avatar Sender**: Sends the avatar image of the most recently mentioned user to the channel every 10 seconds.
- **Random Emoji Sender**: Sends a random emoji to the last channel interacted with every 5 seconds.
- **Random Reaction**: Reacts to messages with a random emoji if the bot is mentioned.
- **Language Translation**: Translates messages between English and Russian.

## Requirements

- Python 3.7 or higher
- `discord.py` library
- `aiohttp` library
- `googletrans` library

## Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/subatsult/discord-echo-bot.git
   cd discord-echo-bot
