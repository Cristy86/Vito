import traceback
import sys
from discord.ext import commands
from utils.settings import ERROR_EMOJI
import discord



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
        
        ignored = (commands.MissingRequiredArgument, commands.BadArgument, commands.NoPrivateMessage, commands.CheckFailure, commands.CommandNotFound, commands.DisabledCommand, commands.CommandInvokeError, commands.TooManyArguments, commands.UserInputError, commands.CommandOnCooldown, commands.NotOwner, commands.MissingPermissions, commands.BotMissingPermissions)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ERROR_EMOJI} {ctx.command} has been disabled.')

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'{ERROR_EMOJI} {error}.')

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'{ERROR_EMOJI} {error}.')

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f'{ERROR_EMOJI} {error}.')

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(f'{ERROR_EMOJI} {error}.')
        
        elif isinstance(error, commands.UserInputError):
            await ctx.send(f'{ERROR_EMOJI} {error}.')
        
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'{ERROR_EMOJI} {error}.')
        
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f'{ERROR_EMOJI} {error}.')
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ERROR_EMOJI} {error}.')
        
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'{ERROR_EMOJI} {error}.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return
            except:
                pass
                
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
