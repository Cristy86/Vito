import discord
from discord.ext import commands

import asyncio
import os
import random
from datetime import datetime
from utils.settings import GREEN_EMBED
from discord.ext.commands.cooldowns import BucketType

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def random(self, ctx):
        """Chooses a random user."""
        if ctx.author.bot:
            return
        
        user = random.choice(ctx.guild.members)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.title = "Random Member"
        embed.description = f"\U0001f464 User: {self.bot.get_user(user.id)}\n\n\U0001f194 User ID: {user.id}\n\n\U0001f916 Bot: {user.bot}\n\n\U00002139 Joined At: {user.joined_at}"
        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
