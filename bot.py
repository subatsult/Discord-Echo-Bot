import discord
from discord.ext import commands
import aiohttp
import io
from cfg import *

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # Check if the message contains mentions
        if message.mentions:
            user = message.mentions[0]

            # Debug: Print user details
            print(f'Mentioned user: {user.name}, Avatar URL: {user.avatar}')
            
            if user.avatar:
                avatar_url = user.avatar.url
                # Debug: Print the avatar URL
                print(f'Avatar URL: {avatar_url}')
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as response:
                        if response.status == 200:
                            img_data = io.BytesIO(await response.read())
                            await message.channel.send(f'{user.name}\'s avatar:', file=discord.File(img_data, 'avatar.png'))
                        else:
                            await message.channel.send('Could not retrieve the avatar. Response status: {}'.format(response.status))
            else:
                await message.channel.send('User does not have an avatar set. Debug: Avatar URL: {}'.format(user.avatar.url if user.avatar else 'None'))
        else:
            await message.channel.send('No user mentioned.')
    
    await bot.process_commands(message)

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
bot.run(TOKEN)
