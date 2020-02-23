import discord
from discord.ext import commands

import asyncio
import os
import random, praw
import aiohttp
from datetime import datetime
from utils.settings import GREEN_EMBED, ERROR_EMOJI
from discord.ext.commands.cooldowns import BucketType

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),                        
                        user_agent=os.getenv('REDDIT_USER_AGENT'))
    
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

        
    def meme(self):
         memes_submissions = self.reddit.subreddit('memes').hot()
         post_to_pick = random.randint(1, 100)
         for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
         return submission.url
    
    def do_softwaregore(self):
        softwaregore_submissions = self.reddit.subreddit('softwaregore').hot()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in softwaregore_submissions if not x.stickied)
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
        """Shows a meme from r/memes."""
        if ctx.author.bot:
            return
        
        try:
            async with ctx.typing():
                b = await self.bot.loop.run_in_executor(None, self.meme)
                await ctx.send(b)
        except Exception as e:
            await ctx.message.add_reaction(ERROR_EMOJI)
            await ctx.send(f'{e}')
                                   
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 20.0, commands.BucketType.user)
    async def hastebin(self, ctx, *, text:str):
        """Uploads text to Hastebin."""
  
        text = self.cleanup_code(text)
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hastebin.com/documents",data=text.encode('utf-8')) as post:
                post = await post.json()
                await ctx.send(f"<https://hastebin.com/{post['key']}>")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 20.0, commands.BucketType.user)
    async def mystbin(self, ctx, *, text:str):
        """Uploads text to mystb.in."""

        text = self.cleanup_code(text)
        async with aiohttp.ClientSession() as session:
            async with session.post("http://mystb.in/documents",data=text.encode('utf-8')) as post:
                post = await post.json()
                await ctx.send(f"<http://mystb.in/{post['key']}>")

                               
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def softwaregore(self, ctx):
        """Generates a random r/softwaregore from reddit."""
        try:
            async with ctx.typing():
                b = await self.bot.loop.run_in_executor(None, self.do_softwaregore)
                embed = discord.Embed(color=GREEN_EMBED)
                embed.set_image(url=b)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.message.add_reaction(ERROR_EMOJI)
            await ctx.send(f'```py\n{type(e).__name__}: {str(e)}\n```')
                               
def setup(bot):
    bot.add_cog(Random(bot))
