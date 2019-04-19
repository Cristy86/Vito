import discord
from discord.ext import commands

import asyncio
import os
import platform, psutil, pkg_resources
from utils.settings import GREEN_EMBED
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType

bot = commands.Bot(command_prefix=commands.when_mentioned_or(os.getenv('BOT_PREFIX')))
bot.launch_time = datetime.utcnow()
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

@bot.command(name='stats')
@commands.cooldown(1,5,BucketType.user) 
async def _stats(ctx):
    """Shows the stats about the bot."""
    if ctx.author.bot:
        return                                                    
                                                       
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=GREEN_EMBED)
    embed.title = "Stats"
    embed.description = f"<:python:568678201241501696> Python Version: {platform.python_version()}\n\n<:discord:568684907384274964> discord.py version: {pkg_resources.get_distribution('discord.py').version}\n\n\U0001f465 Users: {len(bot.users)}\n\n\U0001f3d3 Ping latency: {round(bot.latency * 1000)}ms\n\n\U0001f464 Owner: {bot.get_user(339752841612623872)}\n\n\U000023f0 Uptime: {days}d, {hours}h, {minutes}m, {seconds}s\n\n\U0001f4c3 Servers: {len(bot.guilds)}\n\nMemory usage: {psutil.virtual_memory().percent} MB\n\nCPU usage: {psutil.cpu_percent()}%"
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
