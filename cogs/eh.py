import traceback
import sys
from discord.ext import commands
from utils.settings import GREEN_EMBED, ERROR_EMOJI
import discord
import humanize
import datetime

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> `{ctx.command}` has been disabled."
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> There was a error that is unexpected, please report this to the owner. (c_ristian#0126)\n\n`{error}`"
            return await ctx.send(embed=embed)
            

        elif isinstance(error, commands.CheckFailure):
                embed = discord.Embed(color=GREEN_EMBED)
                embed.description = f"<{ERROR_EMOJI}> Oh! I am sorry, a check failed. `{error}`"
                return await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> There was a error that is unexpected, please report this to the owner. (c_ristian#0126)\n\n`{error}`"
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> There was a error that is unexpected, please report this to the owner. (c_ristian#0126)\n\n`{error}`"
            return await ctx.send(embed=embed)
        
        elif isinstance(error, commands.UserInputError):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> `{error}`"
            return await ctx.send(embed=embed)
        
        elif isinstance(error, commands.CommandOnCooldown):
            test = error.retry_after
            test = round(test, 2)
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> Try again after {humanize.naturaldelta(datetime.timedelta(seconds=test))}."
            return await ctx.send(embed=embed)
        
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> I am sorry but you are not the owner of this bot."
            return await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> I am missing some permissions.\n\n`{error}`"
            return await ctx.send(embed=embed)
        
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(color=GREEN_EMBED)
            embed.description = f"<{ERROR_EMOJI}> The bot is missing some permissions.\n\n`{error}`"
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return
            except:
                pass
                
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
