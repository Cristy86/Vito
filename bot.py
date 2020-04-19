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
startup_extensions = ['cogs.owner','cogs.webhook','cogs.random','cogs.eh', 'cogs.mod', 'jishaku']


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
    await ctx.trigger_typing()
    t_1 = time.perf_counter()
    t_2 = time.perf_counter()
    time_delta = round((t_2-t_1)*1000)                                                    
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=GREEN_EMBED)
    embed.title = "Stats"
    embed.add_field(name="Owner", value=f"The bot of this owner is `{bot.get_user(339752841612623872)}`, and this bot sees `{len(bot.users)}` users!", inline=True)
    embed.add_field(name="Usage & Misc", value=f"I am in `{len(bot.guilds)}` servers! And my memory usage is `{psutil.virtual_memory().percent} MB` and my CPU usage is `{psutil.cpu_percent()}%`!", inline=True)
    embed.add_field(name="Uptime & Ping latency", value=f"I have been up to `{days}d, {hours}h, {minutes}m, {seconds}s` and my websocket latency is `{round(bot.latency * 1000)}ms` and time is `{time_delta}ms.`!", inline=False)
    embed.add_field(name="A little bit of info", value="Hi! My name is Vito and I am a personal bot made by Cristian. And I am at least featured in some servers but I am a personal server bot too! This bot cannot be invited to other servers without the owner's permission! I do not have many commands, I am a bot used for suggestions, polls and a bit of moderation. That's all!", inline=True)
    embed.set_footer(text=bot.user.name)
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
