import discord
from bot import Bot

TOKEN = open('./token').read().strip()
client = discord.Client()

PREFIX = "!"

bot = Bot(client, PREFIX)

@client.event
async def on_message(message):
    await bot.run(message)

@client.event
async def on_ready():
    bot.ready()

client.run(TOKEN)
