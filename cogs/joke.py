import discord
from discord.ext import commands

import asyncio, io

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def nothing(self, ctx, yes: str):
        """no."""
        if ctx.author.bot:
            return

        await ctx.send(f"***{yes}***")

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def thanos(self, ctx):
        """yes."""
        if ctx.author.bot:
            return

        await ctx.send(f"**thanos will slap you {ctx.author.mention}**")


def setup(bot):
    bot.add_cog(Joke(bot))
