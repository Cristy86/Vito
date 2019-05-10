import discord
from discord.ext import commands

import asyncio
import os
import random
import aiohttp
import praw
from datetime import datetime
from utils.settings import GREEN_EMBED, ERROR_EMOJI
from discord.ext.commands.cooldowns import BucketType

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                        user_agent=os.getenv('REDDIT_USER_AGENT'))

    def do_dankmeme(self):
        memes_submissions = self.reddit.subreddit('dankmemes').hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        return submission.url

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
        embed.description = f"User: {self.bot.get_user(user.id)}\n\nUser ID: {user.id}\n\nBot: {user.bot}\n\nJoined At: {user.joined_at}"
        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def dadjoke(self, ctx):
        """Says a dad joke."""
        if ctx.author.bot:
            return
        
        try:

            headers = {"Accept": "application/json"}

            async with aiohttp.ClientSession() as session:
                async with session.get('https://icanhazdadjoke.com', headers=headers) as get:
                    resp = await get.json()
                    await ctx.send(f"{resp['joke']}")
        except Exception as e:
            await ctx.send(f"{e}")
    

    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    @commands.guild_only()
    async def dankmeme(self, ctx):
        """Shows a dank meme from r/dankmemes."""
        if ctx.author.bot:
            return
        
        try:
            async with ctx.typing():
                b = await self.bot.loop.run_in_executor(None, self.do_dankmeme)
                await ctx.send(b)
        except Exception as e:
            await ctx.message.add_reaction(ERROR_EMOJI)
            await ctx.send(f'{e}')


def setup(bot):
    bot.add_cog(Random(bot))
