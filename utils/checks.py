import discord
from discord.ext import commands

import asyncio
import os

def is_bot(ctx):
 return ctx.author.bot == False
