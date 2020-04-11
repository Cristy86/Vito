import discord
from discord.ext import commands
from utils.paginator import Paginator

import asyncio
import os
import random, praw
import aiohttp
import humanize
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
                                   
    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1.0, 20.0, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Shows information about a user."""

        try:
            user = user or ctx.author
            game = user.activity or None

            if game is None:
                game = game
                large_image_game = "https://cdn.discordapp.com/attachments/447662555993866243/464021387481317376/unknown.png"
                small_image_game = "https://cdn.discordapp.com/attachments/447662555993866243/464021387481317376/unknown.png"
                large_image_text_game = "None"
                small_image_text_game = "None"
            else:
                game = game
                largegame = user.activity.large_image_url
                smallgame = user.activity.small_image_url
                largetextgame = user.activity.large_image_text
                smallimagetextgame = user.activity.small_image_text

            perms = '\n'.join(perm for perm, value in user.guild_permissions if value)
            days = datetime.utcnow() - user.created_at

            days2 = datetime.utcnow() - user.joined_at

            embed = discord.Embed(color=user.color.value)
            embed.title = f"`- - {user} - -`"
            embed.description = f":white_small_square: **Joined at:** **{humanize.naturaldate(user.joined_at)} [`{days2.days} Days.`]**\n:white_small_square: **Status:** **`{user.status}`**\n:white_small_square: **Top Role:** **`{user.top_role.name}`**\n:white_small_square: **Roles:** {','.join([role.name for role in user.roles])}\n:white_small_square: **Playing:** **`{game}`**\n:white_small_square: **Is it a bot:** **`{user.bot if user.bot else 'False'}`**\n:white_small_square: **ID:** **`{user.id}`**\n:white_small_square: **Created at:** **{humanize.naturaldate(user.created_at)} [`{days.days} Days.`]**\n:white_small_square: **Is she/he on mobile:** **`{user.is_on_mobile() if user.is_on_mobile() else 'False'}`**\n:white_small_square: **Custom status:** **`{user.activity.state if user.activity.state else None}`**"
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f"{self.bot.user.name} - Page 1/3")
            embed.timestamp = datetime.utcnow()

            embed2 = discord.Embed(color=user.color.value)
            embed2.title = f"`- - {user}'s permissions - -`"
            embed2.description = f"`{perms}`"
            embed2.set_footer(text=f"{self.bot.user.name} - Page 2/3")

            embed3 = discord.Embed(color=user.color.value)
            embed3.title = f"`- - {user}'s game image - -`"
            embed3.description = f"`Using {smallimagetextgame}`\n`{largetextgame}`"
            embed3.set_image(url=largegame)
            embed3.set_footer(text=f"{self.bot.user.name} - Page 3/3")
            embed3.set_thumbnail(url=smallgame)

            await Paginator(extra_pages=[embed, embed2, embed3])._paginate(ctx)
        except:
            user = user or ctx.author
            game = user.activity

            perms = '\n'.join(perm for perm, value in user.guild_permissions if value)
            days = datetime.utcnow() - user.created_at

            days2 = datetime.utcnow() - user.joined_at

            embed = discord.Embed(color=user.color.value)
            embed.title = f"`- - {user} - -`"
            embed.description = f":white_small_square: **Joined at:** **{humanize.naturaldate(user.joined_at)} [`{days2.days} Days.`]**\n:white_small_square: **Status:** **`{user.status}`**\n:white_small_square: **Top Role:** **`{user.top_role.name}`**\n:white_small_square: **Roles:** {','.join([role.name for role in user.roles])}\n:white_small_square: **Playing:** **`{game}`**\n:white_small_square: **Is it a bot:** **`{user.bot if user.bot else 'False'}`**\n:white_small_square: **ID:** **`{user.id}`**\n:white_small_square: **Created at:** **{humanize.naturaldate(user.created_at)} [`{days.days} Days.`]**\n:white_small_square: **Is she/he on mobile:** **`{user.is_on_mobile() if user.is_on_mobile() else 'False'}`**\n:white_small_square: **Custom status:** **`{user.activity.state if user.activity.state else None}`**"
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f"{self.bot.user.name} - Page 1/2")
            embed.timestamp = datetime.utcnow()

            embed2 = discord.Embed(color=user.color.value)
            embed2.title = f"`- - {user}'s permissions - -`"
            embed2.description = f"`{perms}`"
            embed2.set_footer(text=f"{self.bot.user.name} - Page 2/2")

            await Paginator(extra_pages=[embed, embed2])._paginate(ctx)
    
    @commands.has_permissions(ban_members=True)                              
    @commands.command()
    @commands.cooldown(1,7200,BucketType.guild)
    @commands.guild_only()
    async def suggest(self, ctx, *, text: str):
        """A command that sends a suggestion to our server!"""
        embed = discord.Embed(color=0x80ff80)
        embed.title = "Suggestion"
        test = self.bot.user.name
        embed.description = f"`{ctx.author}` sent a suggestion, the description will be below."
        embed.add_field(name="Description", value=f"{text}", inline=False)
        embed.add_field(name="Notice", value="You cannot vote your suggestion, if so doing that will result removing the reaction.", inline=True)         
        embed.set_footer(text=f"{test}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        msg = await self.bot.get_channel(697860969803546635).send(embed=embed)
        await msg.add_reaction('\N{THUMBS UP SIGN}')
        await msg.add_reaction('\N{THUMBS DOWN SIGN}')
        response = discord.Embed(color=0x80ff80)
        response.title = "Thank you!"
        response.description = "We honestly appreciate suggestions for the server to get better, now just wait and for the administration team and the public to vote for your suggestion!"
        response.set_footer(text=test)                           
        await ctx.send(embed=response)
                                   
    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.cooldown(1.0, 3600, commands.BucketType.user)
    async def webhook(self, ctx, user:discord.Member=None, *, text: str):
        """Makes an webhook and sends text as an user."""
        if ctx.author.bot:
            return
        if user is None:
            user = ctx.author
        server = _bot.get_guild(648939872173817887).members
        if ctx.author in server:
             continue
        else:
             return

        channel = self.bot.get_channel(698552503125671996)
        await ctx.message.add_reaction("⏰")
        content = text
        webhook = await channel.create_webhook(name=f"{user.name}#{user.discriminator}")
        
        await ctx.message.remove_reaction("⏰", member=ctx.author)
        await ctx.message.add_reaction("☑️")
        await webhook.send(content, avatar_url=user.avatar_url_as(format='png'))
        await webhook.delete()
                               
def setup(bot):
    bot.add_cog(Random(bot))
