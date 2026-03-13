import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN: str = os.getenv('DISCORD_TOKEN', 'no_token_found')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    

async def main():
    async with bot:
        await bot.load_extension("commands.card")
        await bot.load_extension("commands.pack")
        await bot.start(TOKEN)

asyncio.run(main())
