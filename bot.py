import discord
from cfg import TOKEN
from discord.ext import commands, tasks
import aiohttp
import io
import random
from googletrans import Translator

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Ensure members intent is enabled
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the translator
translator = Translator()

# Global variables to keep track of the last user and channel interacted with
last_user = None
last_channel = None

# List of emojis to use for reactions
reaction_emojis = ['👍', '👎', '😂', '😮', '😢', '😡', '❤️', '🎉']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    send_avatar.start()
    send_random_emoji.start()

@bot.event
async def on_message(message):
    global last_user, last_channel

    if message.author == bot.user:
        return

    if message.mentions:
        # Update to the first mentioned user
        last_user = message.mentions[0]
        last_channel = message.channel

        # React to the message with a random emoji once
        if not any(reaction.emoji in reaction_emojis for reaction in message.reactions):
            emoji = random.choice(reaction_emojis)
            await message.add_reaction(emoji)
    
    # Detect message language
    detected_lang = translator.detect(message.content).lang

    # Translate message if necessary
    if detected_lang == 'ru':
        translated = translator.translate(message.content, src='ru', dest='en')
        response = f'Translated message: {translated.text}'
    elif detected_lang == 'en':
        translated = translator.translate(message.content, src='en', dest='ru')
        response = f'Переведенное сообщение: {translated.text}'
    else:
        response = 'Sorry, I can only translate between English and Russian.'

    await message.channel.send(response)
    await bot.process_commands(message)

@tasks.loop(seconds=10)
async def send_avatar():
    global last_user, last_channel

    if last_user and last_channel:
        avatar_url = last_user.avatar.url
        
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    img_data = io.BytesIO(await response.read())
                    # Send the avatar image to the last channel interacted with
                    await last_channel.send(f'{last_user.name}\'s avatar:', file=discord.File(img_data, 'avatar.png'))
                else:
                    print(f'Failed to retrieve avatar. Status code: {response.status}')
    else:
        print('No user or channel available to send avatar.')

@tasks.loop(seconds=5)
async def send_random_emoji():
    global last_channel

    if last_channel:
        emoji = random.choice(reaction_emojis)
        await last_channel.send(f'Random emoji: {emoji}')

bot.run(TOKEN)
