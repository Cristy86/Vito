import discord
from discord.ext import commands

import asyncio
import os
import platform, psutil
from utils.settings import GREEN_EMBED
from datetime import datetime

bot = commands.Bot(command_prefix=commands.when_mentioned_or(os.getenv('BOT_PREFIX')))
bot.launch_time = datetime.utcnow()
bot.process = psutil.Process()
startup_extensions = ['cogs.owner','cogs.random','cogs.eh','jishaku']


@bot.event
async def on_ready():
    print('Logged in as:')
    print('------')
    print(f'Username: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'Active on: {len(bot.guilds)} Servers.')
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{os.getenv('BOT_PREFIX')}help | {len(bot.users)} users."))

@bot.check
async def _bot_check(ctx):
    if user.bot:
      return
    else:
      pass

@bot.command(name='info')
async def _info(ctx):
    """Shows info about the bot."""
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=GREEN_EMBED)
    embed.title = "Info"
    embed.description = f"Python Version: {platform.python_version()}\n\ndiscord.py version: {discord.__version__}\n\nMemory usage: {psutil.virtual_memory().percent} MB\n\nCPU usage: {psutil.cpu_percent()}%\n\nPing latency: {round(bot.latency * 1000)}ms\n\nOwner: {bot.get_user(339752841612623872)}\n\nUptime: {days}d, {hours}h, {minutes}m, {seconds}s\n\nServers: {len(bot.guilds)}\n\nUsers: {len(bot.users)}"
    embed.set_footer(text=f"{bot.user.name}")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)                                                         
                                                        
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(os.getenv('BOT_TOKEN'))
