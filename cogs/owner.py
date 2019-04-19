from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import aiohttp

import datetime
from collections import Counter

from platform import python_version
import copy
import os
from utils.settings import OWNERS, GREEN_EMBED, ERROR_EMOJI, SUCCESS_EMOJI, LOADING_EMOJI
import time
from typing import Union

class Owner(commands.Cog):
    """Owner-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self.blocked = []

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'




    @commands.command(name='load', hidden=False)
    @commands.guild_only()
    async def _load(self, ctx, *, extension_name):
        """Loads a module."""
        try:
            wait = await ctx.send(f"<{LOADING_EMOJI}> **`Wait for result.`**")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.load_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")

    @commands.command(name='unload', hidden=False)
    @commands.guild_only()
    async def _unload(self, ctx, *, extension_name):
        """Unloads a module."""
        try:
            wait = await ctx.send(f"**`Wait for result.`**")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.unload_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")

    @commands.command(name='reload', hidden=False)
    @commands.guild_only()
    async def _reload(self, ctx, *, extension_name):
        """Reloads a module."""
        try:
            wait = await ctx.send(f"<{LOADING_EMOJI}> **`Wait for result.`**")
            await asyncio.sleep(1)
            await wait.delete()
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
            await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")
        except Exception as e:
            await ctx.message.add_reaction(f"{ERROR_EMOJI}")
            await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")

    @commands.command()
    @commands.guild_only()
    async def runas(self, ctx, member: Union[discord.Member, discord.User], *, commandName: str):
        """Runs as someone.
        Credits: Adrian#1337
        """
        wait = await ctx.send(f"<{LOADING_EMOJI}> **`Wait for result.`**")
        await asyncio.sleep(1)
        await wait.delete()
        fake_msg = copy.copy(ctx.message)
        fake_msg._update(ctx.message.channel, dict(content=ctx.prefix + commandName))
        fake_msg.author = member
        new_ctx = await ctx.bot.get_context(fake_msg)
        await ctx.bot.invoke(new_ctx)
        await ctx.message.add_reaction(f"{SUCCESS_EMOJI}")

    @commands.command(hidden=True, name='eval', aliases=['exec'])
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code.
        Credits: R. Danny made by Danny#0007
        https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L72-L117
        """

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        await ctx.message.add_reaction(LOADING_EMOJI)
        start = time.perf_counter()

        try:
            exec(to_compile, env)
        except Exception as e:
            end = time.perf_counter()
            await ctx.message.remove_reaction(LOADING_EMOJI, member=ctx.me)
            await ctx.message.add_reaction(ERROR_EMOJI)
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = f"Error. <{ERROR_EMOJI}>"
            embed.description = f'```py\n{e.__class__.__name__}: {e}\n```'
            embed.timestamp = datetime.datetime.utcnow()
            return await ctx.author.send(embed=embed)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            end = time.perf_counter()
            await ctx.message.remove_reaction(LOADING_EMOJI, member=ctx.me)
            await ctx.message.add_reaction(ERROR_EMOJI)
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = f"Error. <{ERROR_EMOJI}>"
            embed.description = f'```py\n{value}{traceback.format_exc()}\n```'
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.author.send(embed=embed)
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.remove_reaction(LOADING_EMOJI, member=ctx.me)
                await ctx.message.add_reaction(SUCCESS_EMOJI)
            except:
                pass

            if ret is None:
                if value:
                    end = time.perf_counter()
                    embed = discord.Embed(color=GREEN_EMBED)
                    embed.title = f"Success. <{SUCCESS_EMOJI}>"
                    embed.description = f'```py\n{value}\n```'
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.author.send(embed=embed)
            else:
                end = time.perf_counter()
                self._last_result = ret
                embed = discord.Embed(color=GREEN_EMBED)
                embed.title = f"Success. <{SUCCESS_EMOJI}>"
                embed.description = f'```py\n{value}{ret}\n```'
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.author.send(embed=embed)

    @commands.command(pass_context=True)
    async def cleanup(self, ctx, count: int):
        """Cleans up the bot's messages."""
        async for m in ctx.channel.history(limit=count + 1):
            if m.author.id == self.bot.user.id:
                await m.delete()

        wait = await ctx.send(f"<{LOADING_EMOJI}> **`Wait for result.`**")
        await asyncio.sleep(1)
        await wait.delete()
        await ctx.send(f"<{SUCCESS_EMOJI}> **Cleared ​`{count}​` messages.**", delete_after=5)

    @commands.command(pass_context=True, hidden=True)
    async def emojis(self, ctx, *, guildID: int):
        """Takes information about the emojis from a server."""
        try:
            wait = await ctx.send(f"<{LOADING_EMOJI}> **`Wait for result.`**")
            g = self.bot.get_guild(guildID)
            g2 = self.bot.get_guild(465180787667369996)

            ch = await g2.create_text_channel(f'{g.name}-emojis')

            for e in g.emojis:
                await ch.send(f"`{e}` - {e.url}")

            await wait.delete()
            await ctx.send(f"<{SUCCESS_EMOJI}> **Done, `{len(g.emojis)}` emojis.**")
        except Exception as e:
            await wait.delete()
            await ctx.send(f"<{ERROR_EMOJI}> **The guildID might be invalid, make sure the bot is there.**\n\n```py\n{type(e).__name__}: {str(e)}\n```")


    @commands.guild_only()
    @commands.group(hidden=True, name="activity")
    async def _activity(self, ctx):
        """A command that changes status playing and more."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Incorrect block subcommand passed.')

    @commands.guild_only()
    @_activity.command()
    async def playing(self, ctx, *, activity: str):
        """Sets playing status in silent."""
        await self.bot.change_presence(activity=discord.Game(name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @commands.guild_only()
    @_activity.command()
    async def watching(self, ctx, *, activity: str):
        """Sets watching status in silent."""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @commands.guild_only()
    @_activity.command()
    async def listening(self, ctx, *, activity: str):
        """Sets listening status in silent."""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

    @commands.guild_only()
    @_activity.command()
    async def streaming(self, ctx, url: str, *, activity: str):
        """Sets streaming status in silent."""
        await self.bot.change_presence(activity=discord.Streaming(name=activity, url=url))
        await ctx.message.add_reaction(SUCCESS_EMOJI)

def setup(bot):
    bot.add_cog(Owner(bot))
