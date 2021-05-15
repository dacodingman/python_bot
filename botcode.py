from attr import has
import discord
import logging
from discord import permissions
from discord.ext import commands
import typing

from discord.ext.commands.core import has_permissions

client = discord.Client()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='ehe')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ehehelppls"))


@bot.command()
async def helppls(ctx):
    await ctx.send("""
    I'm a basic bot, but heres some help if you really need it:

    prefix = ehe

    say: says whatever comes in the following words!
    ban: bans the mentioned member! (note: command only works if the sender has ban permissions)
    """)




@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    if has_permissions(ban_members = False):
        ctx.send("insufficient permisions!")
    else:
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been kick:)')

@bot.command()
async def say(ctx, *args):
    await ctx.send('{}'.format(' '.join(args)))

bot.run('ODQyNzU2MDkxNjE2Mjk2OTgw.YJ57xQ.X4tv5WZgTtqLc4A-JncuuIO4HUk')