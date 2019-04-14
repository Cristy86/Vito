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
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f'{error}.')

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(f'{error}.')

        elif isinstance(error, commands.CommandInvokeError):
            return await ctx.send(f'{error}.')

        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send(f'{error}.')
        
        elif isinstance(error, commands.UserInputError):
            return await ctx.send(f'{error}.')
        
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'{error}.')
        
        elif isinstance(error, commands.NotOwner):
            return await ctx.send(f'{error}.')
        
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(f'{error}.')
        
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f'{error}.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return
            except:
                pass
                
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
