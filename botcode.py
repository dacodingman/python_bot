from datetime import datetime, timedelta
from inspect import ArgSpec
from operator import truediv
from os import name
from attr import __title__, has
import discord
import logging
from discord import permissions
from discord import message
from discord import channel
from discord import colour
from discord.ext import commands
import typing
import time
from discord.ext.commands.converter import ColorConverter
from pytz import timezone 
from datetime import datetime

import regex
import perms
import re
import bs4
import requests

from discord.ext.commands.core import after_invoke, check, has_permissions

client = discord.Client()

#logger

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord2.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='ehe')

#internal ready up message

guilds = {

787036437727543336 : {'pogchampers' : 'true'}, 
233591609852297216 : {'pogchampers' : 'false'},

}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #channel = bot.get_channel(787036437727543339)
    #await channel.send('hello gamers im online!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ehehelppls"))

#update the help command so it sends as an embed 787036437727543339

@bot.command(name= 'plshelp', aliases=['helppls'])
async def helppls(ctx, self = None, guild = None):
    guild = ctx.message.guild.id
    if guilds[guild]['pogchampers'] == 'true':

        embedVar = discord.Embed(title="help", description=r"""
            I'm a basic bot, but heres some help if you really need it:

            prefix = ehe

            say: says whatever comes in the following words!

            ban: bans the mentioned member! (note: command only works if the sender has ban permissions)

            clear: purges the message (note: will not purge messages older then 14 days)

            joke: find out peepoSmile

            jokeban: @ a user and find out what it does.

            ehe: ehe pp :)

            ftoc: coverts farienheight to celcius

            ctof: converts celcius of farienheight

            subtime: shows the time for GMT +5.5 (aka the time for submolok)

            esttime: shows the time for est

            gmt+2time: shows the time for gmt+2

            coviddata: shows how many covid cases there were in the past 7 days in any state in the U.S.A!

            microchip: shows what % of people in your state have at least one dose of the COVID-19 vaccine!
            (note: any 2 word states must be connected by a -)

            """, color=0x00ff00)
        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title="help", description=r"""
            I'm a basic bot, but heres some help if you really need it:

            prefix = ehe


            say: says whatever comes in the following words!

            ban: bans the mentioned member! (note: command only works if the sender has ban permissions)

            clear: purges the message (note: will not purge messages older then 14 days)

            joke: find out peepoSmile

            jokeban: @ a user and find out what it does.

            ftoc: coverts farienheight to celcius

            ctof: converts celcius of farienheight

            esttime: shows the time for est

            coviddata: shows how many covid cases there were in the past 7 days in any state in the U.S.A!

            vaccinedata: shows what % of people in your state have at least one dose of the COVID-19 vaccine!
            (note: any 2 word states must be connected by a -)

            """, color=0x00ff00)
        await ctx.send(embed=embedVar)


#ban command, it doesnt send insufficient perms message, fix that 

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    if has_permissions(ban_members = False):
        ctx.send("insufficient permisions!")
    else:
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been kick:)')

#purge, types for too long, fix that

@bot.command(name="clear", aliases=['purge', 'annihilate '])
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, limit: typing.Optional[int] = 1):
    if 0 < limit <= 100:
        with ctx.channel.typing():
            await ctx.channel.purge(limit = limit)
            await ctx.message.delete()


#say argument, takes any number of args
            

@bot.command()
async def say(ctx, *, args):
    await ctx.send('{}'.format(''.join(args)))
    await ctx.message.delete()

@bot.command()
async def joke(ctx, args=None):
    if args == None:
        await ctx.send('you :D')
    else:
        await ctx.send('%s is the true joke' % args)

@bot.command()
async def jokeban(ctx, args=None):
    if args == None:
        await ctx.send('you need to ban someone! type a name or @ someone')
    else:
        await ctx.send('i will definitely ban %s now...'%args)

@bot.command()
async def ehe(ctx):
    await ctx.send('ehe pp :)')


#fariengeight to metric

#f-32/1.8

@bot.command()
async def ftoc(ctx, arg, celcius=None):
    arg = int(arg)
    celcius = (arg-32)/1.8
    await ctx.send("%s f is %s in c"%(arg, round(celcius, 2)))

#metric to farienheight

@bot.command()
async def ctof(ctx, arg, far=None):
    arg = int(arg)
    far = (arg*1.8)+32
    await ctx.send("%s c is %s in f"%(arg, round(far, 2)))

#submolok time, 5.5 hours ahead of gmt Asia/Kolkata

@bot.command(name = "subtime", aliases=['gmt+5.5', 'indiatime'])
async def subtime(ctx, ind_time = None):
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    embedVar = discord.Embed(title="time in gmt+2!", description= ind_time, color=0x00ff00)
    await ctx.send(embed=embedVar)

@bot.command(name = "esttime", aliases=['reestime'])
async def esttime(ctx, est_time = None):
    est_time = datetime.now(timezone("US/Eastern")).strftime('%Y-%m-%d %H:%M:%S')
    embedVar = discord.Embed(title="time in est!", description= est_time, color=0x00ff00)
    await ctx.send(embed=embedVar)

@bot.command(name = "gmt+2", aliases=['gmt+2time', 'spaintime'])
async def spaintime(ctx, gmt2_time = None):
    gmt2_time = datetime.now(timezone("Europe/Madrid")).strftime('%Y-%m-%d %H:%M:%S')
    embedVar = discord.Embed(title="time in gmt+2!", description= gmt2_time, color=0x00ff00)
    await ctx.send(embed=embedVar)


@bot.command()
async def goodnight(ctx, args=None):
    await ctx.message.delete()
    await ctx.send('good night, %s'%args)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def pogchampers(ctx, guild = None):
    guild = ctx.message.guild.id
    if guilds[guild]['pogchampers'] == 'True':
        await ctx.send('it worked rees good job jackass')
    else:
        await ctx.send('it worked fumbass')

@bot.command()
async def goodmorning(ctx, args=None):
    await ctx.message.delete()
    await ctx.send('goodmorning, %s'%args)

@bot.command()
@commands.bot_has_permissions(administrator=True)
async def permcheck(ctx):
    await ctx.send('i have admin perms!')

@bot.command()
async def coviddata(ctx, args, soup = None, requests_result = None, elms = None, regex2 = None, regex3 = None):
    yes = 'https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/state/%s'%args
    requests_result = requests.get(yes)
    soup = bs4.BeautifulSoup(requests_result.text, 'html.parser')
    elms = soup.select('div#root div:nth-child(1) > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td:nth-child(4)')
    regex2 = re.findall('[0-9]', str(elms))
    regex3 = ''.join(regex2)
    print(regex3)
    await ctx.send('there were %s covid cases in the last 7 days in %s'%(regex3, args))

@bot.command(name = "microchip", aliases=['vaccinedata'])
async def microchip(ctx, args, soup = None, requests_result = None, elms = None, regex2 = None, regex3 = None, notes = None):
    yes = 'https://usafacts.org/visualizations/covid-vaccine-tracker-states/state/%s'%args
    requests_result = requests.get(yes)
    soup = bs4.BeautifulSoup(requests_result.text, 'html.parser')
    elms = soup.select('div#root p:nth-child(2) > span:nth-child(2)')
    print(elms)
    regex2 = re.findall('[0-9]', str(elms))
    del regex2[0:8]
    regex3 = ''.join(regex2)
    regex3 = regex3 + '%'
    print(regex3)
    await ctx.send('%s of people in %s have at least one dose of the COVID-19 vaccine!'%(regex3, args))
    
    bot.run('token here plz')
