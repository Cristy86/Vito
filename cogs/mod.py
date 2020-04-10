import discord
from discord.ext import commands


import asyncio
import traceback
from discord.ext.commands.cooldowns import BucketType

import aiohttp
import platform

import os
import unicodedata

import time
import random

from datetime import datetime
import psutil
from utils.settings import ERROR_EMOJI, SUCCESS_EMOJI, GREEN_EMBED

class Moderation(commands.Cog):
    """Mod-only commands for the bot."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def clear(self, ctx, num: int, target:discord.Member = None):
        """Clears X messages."""  
        if ctx.author.bot:
            return
        if num>500 or num<0:
            await ctx.send (f"<{ERROR_EMOJI}> Invalid amount. Maximum is `500`.")
            return
        def msgcheck(amsg):
            if target:
                return amsg.author.id==target.id
            return True
        await ctx.channel.purge(limit=num, check=msgcheck)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Done!"
        embed.description = f"I deleted the most possible messages I could! Maybe the ammount of messages (`{num}`) may be a bit incorrect but sorry! This embed will be deleted after 10 seconds."
        embed.set_footer(text=self.bot.user.name)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed, delete_after=10)

    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason: str = None):
        """Kicks a member with an reason."""      
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't kick the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't kick guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't kick `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't kick `{user}`.")
        if reason is None:
            reason = 'No reason.'
        
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'<{SUCCESS_EMOJI}> Done. The boot kicked him!')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got kicked. :boot:"
            embed.add_field(name="`Moderator`", value=ctx.author)
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass
    
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def softban(self, ctx, user: discord.Member = None, *, reason: str = None):
        """Bans a user and then unbans the user.."""
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't softban the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't softban guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't softban `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't softban `{user}`.")
        if reason is None:
            reason = 'No reason.'
        
        await ctx.guild.ban(user, reason=reason)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f'<{SUCCESS_EMOJI}> Done. Softbanned him!')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got softbanned. <a:BlobBan:466662201835388949>"
            embed.add_field(name="`Moderator`", value=ctx.author)
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            embed.add_field(name="What does softban means?", value="If you don't know, softban means that bans an user and then unbans the user.", inline=True)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass

    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason: str = None):
        """Bans an user.."""      
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't ban the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't ban guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't ban `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't ban `{user}`.")
        if reason is None:
            reason = 'No reason.'
        
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'<{SUCCESS_EMOJI}> Done. Banned him!')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got banned. <a:BlobBan:466662201835388949>"
            embed.add_field(name="`Moderator`", value=ctx.author)
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass

    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def poll(self, ctx, *, text: str):
        """Starts a poll with text."""
        
        if ctx.author.bot:
            return
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.description = f"{text}"
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('\N{THUMBS UP SIGN}')
        await msg.add_reaction('\N{SHRUG}')
        await msg.add_reaction('\N{THUMBS DOWN SIGN}')

    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command(pass_context=True)
    async def warn(self, ctx, logChannel: discord.TextChannel = None, user: discord.Member = None, *, reason: str = None):
        """Warns an user."""
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't warn the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't warn guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't warn `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't warn `{user}`.")
        if reason is None:
            reason = 'No reason.'
        if logChannel is None:
            return await ctx.send(f"<{ERROR_EMOJI}> I need a channel. [example: #general]")
        
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Alert System"
        embed.description = f"{ctx.author} warned {user}."
        embed.add_field(name="`Moderator`", value=ctx.author)
        embed.add_field(name="`Reason`", value=reason)
        await logChannel.send(embed=embed)

        await ctx.send(f'<{SUCCESS_EMOJI}> Done. Warned him!')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got warned. \N{DOUBLE EXCLAMATION MARK}"
            embed.add_field(name="`Moderator`", value=ctx.author)
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx):
        """Displays you some mute commands."""
        if ctx.invoked_subcommand is None:
                await ctx.send(f'<{ERROR_EMOJI}> Incorrect random subcommand passed. Try {ctx.prefix} help mute')
    
    @mute.command()
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx, user: discord.Member, *, reason: str = None):
        """Mutes an user."""
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't mute the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't mute guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't mute `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't mute `{user}`.")
        if reason is None:
            reason = 'No reason.'
        await ctx.channel.set_permissions(user,         read_messages=True,
                                                        send_messages=False, reason=reason)
        await ctx.send(f'<{SUCCESS_EMOJI}> Done. {user} has been muted.')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got muted.. \N{FACE WITHOUT MOUTH}"
            embed.add_field(name="`Moderator`", value=ctx.author)
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass
    
    
    @mute.command()
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx, user: discord.Member, *, reason: str = None):
        """Unmutes an user."""
        if user is None:
            return await ctx.send(f"<{ERROR_EMOJI}> That's not a user. [example: @User#1111]")
        if ctx.author.bot:
            return
        if self.bot.owner_id == user.id:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't unmute the owner of this bot.")
        if user == ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Can't unmute guild owner.")
        if ctx.me.top_role <= user.top_role:
            return await ctx.send(f"<{ERROR_EMOJI}> My role is lower or equal to member's role, can't unmute `{user}`.")
        if ctx.author.top_role <= user.top_role and ctx.author != ctx.guild.owner:
            return await ctx.send(f"<{ERROR_EMOJI}> Your role is lower or equal to member's role. Can't unmute `{user}`.")
        if reason is None:
            reason = 'No reason.'
        await ctx.channel.set_permissions(user,         read_messages=True,
                                                        send_messages=True, reason=reason)
        await ctx.send(f'<{SUCCESS_EMOJI}> Done. Unmuted {user}, aye!')
        try:
            embed = discord.Embed(color=GREEN_EMBED)
            embed.title = "Alert System"
            embed.description = f"Looks like you got unmuted.. \N{FACE WITHOUT MOUTH}"
            embed.add_field(name="`Moderator`", value=ctx.author")
            embed.add_field(name="`Reason`", value=reason)
            embed.add_field(name="`Guild`", value=ctx.guild)
            await user.send(embed=embed)
        except discord.Forbidden as e:
            error = await ctx.send(f"<{ERROR_EMOJI}> Looks like the user blocked me. DM message failed. Deleting this message in 5 seconds.\n```py\n{type(e).__name__}: {e}\n```")
            await asyncio.sleep(5)
            await error.delete()
            pass
        
def setup(bot):
    bot.add_cog(Moderation(bot))
