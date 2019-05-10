import discord
from discord.ext import commands

import asyncio
import time
import random

from utils.settings import CHANNEL1, CHANNEL2, GREEN_EMBED

class Webhook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def test(self, guild):
        count = sum(1 for m in guild.members if m.bot)
        embed = discord.Embed(color=GREEN_EMBED)
        embed.add_field(name="Guild ID", value=f"{guild.id}", inline=False)
        embed.add_field(name="Members", value=f"{guild.member_count - count} members - {count} bots.", inline=False)
        embed.add_field(name="Owner ID", value=f"{guild.owner.id}", inline=False)
        embed.set_thumbnail(url=guild.icon_url or guild.owner.avatar_url)
        embed.set_footer(text=f'{guild.owner}', icon_url=guild.owner.avatar_url)

        return embed
   
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = self.test(guild)
        embed.title = f'{guild}'
        
        webhook = await self.bot.get_channel(CHANNEL1).create_webhook(name=f"Servers: {len(self.bot.guilds)}")
        
        await webhook.send(embed=embed, avatar_url=self.bot.user.avatar_url_as(format='png'))
        await webhook.delete()
    
    @commands.Cog.listener() 
    async def on_guild_remove(self, guild):
        embed = self.test(guild)
        embed.title = f'{guild}'
        
        webhook = await self.bot.get_channel(CHANNEL2).create_webhook(name=f"Servers: {len(self.bot.guilds)}")
        
        await webhook.send(embed=embed, avatar_url=self.bot.user.avatar_url_as(format='png'))
        await webhook.delete()
    

def setup(bot):
    bot.add_cog(Webhook(bot))
