import discord
from discord.ext import commands

import asyncio
import os
import random


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def random(self, ctx):
        """Chooses a random user."""
        user = random.choice(ctx.guild.members)
        await ctx.send(f"User: {bot.get_user(user.id)}\nUser ID: {user.id}\nBot: {user.bot}\nJoined At: {user.joined_at}\nAvatar: {user.avatar_url}")


def setup(bot):
    bot.add_cog(Random(bot))