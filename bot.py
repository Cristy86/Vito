import discord
from discord.ext import commands

import asyncio
import os


bot = commands.Bot(command_prefix=commands.when_mentioned_or(os.getenv('BOT_PREFIX')))
startup_extensions = ['cogs.owner','jishaku']


@bot.event
async def on_ready():
    print('Logged in as:')
    print('------')
    print(f'Username: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'Active on: {len(bot.guilds)} Servers.')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{os.getenv('BOT_PREFIX')}help | {len(bot.users)} users."))

@bot.command(name='info')
async def _info(ctx):
    """Shows info about the bot and the owner."""
    if ctx.author.bot:
        return

    embed = discord.Embed(color=0x00ea17)
    embed.title = "Info"
    embed.description = "Who is Vito?\nVito is a personal bot that is made by Cristy#0126.\nIt will be used to test things and make commands.\nCristy used to code discord.py bots now 8 months ago.\nHe started to get annoyed by being accused of coping source and many things. So he decided to code discord.js bots and leave discord.py behind. After that when starting to code discord.js bots, he did not like the coding in discord.js and many people said that discord.js sucked and he needed to code discord bots with other languages. He gave up and never started to code discord bots until he created Vito."
    embed.set_footer(text=f"{bot.user.name}")
    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)                                                        
                                                        
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(os.getenv('BOT_TOKEN'))
