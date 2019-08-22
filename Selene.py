import discord
import random
import asyncio
import aiohttp
import json
import requests
from discord import Game
from discord.ext.commands import Bot
from bs4 import BeautifulSoup as BS
import urllib.request
from Settings import *

TOKEN = "NjAyNjA3OTU4MTE4ODkxNTQz.XV3bAQ.1a1LJLROk2PmmoEJgwcgUgk4huU"
BOT_PREFIX = ("?", "!")

client = discord.Client()

client = Bot(command_prefix=BOT_PREFIX)

@client.command()
async def Hello(ctx):
    await ctx.send("Embrace!")


@client.command()
async def guide(ctx, job: str):
    if job == 'blm':
        await ctx.send("https://docs.google.com/document/d/1L4gF-1x70jzWfUf3gCCJCni9Hnjy5EMZZbUbIsweXj8/preview")
    elif job == 'smn':
        await ctx.send('https://docs.google.com/document/d/14yHTfZX5ZdrLM6wZ5DbwO6riCncS7AWaLeIi_5q7Wig/preview')
    elif job in ['whm', 'rdm']:
        await ctx.send("Kupo, you don't need it.")
    elif job == 'drk':
        await ctx.send('https://docs.google.com/document/d/1c3RZ55-Ylae0AwLAp9-6kJY33peRayi3fhJg2n6sxRg/preview')
    elif job == 'dnc':
        await ctx.send('https://docs.google.com/document/d/1iktjQ-kW7Vp-iWy_xEWh6t62FaXqjfGELGmcWOtPQfM/preview')
    elif job == 'brd':
        await ctx.send('https://docs.google.com/document/d/1oAy_ZGB9XdWENlnMmAnURfBEyGUKqeOqARdYGnhV-CE/preview')
    else:
        await ctx.send('Oops, guide is not ready :(')


def fflogparse(ffdata):
    #to find how many bosses and how many jobs used per boss
    savage = []
    for item in ffdata:
        if item['difficulty'] == 101:
            savage.append(item)
    ffdata = savage
    bnum = len(ffdata) #number of bosses

    #to find corresponding boss, job, dps, and percentile
    fflogdictionary = {}
    for x in range(0, bnum):
        if ffdata[x]['encounterName'] in fflogdictionary:
            fflogdictionary[ffdata[x]['encounterName']].update({ffdata[x]['spec'] : [ffdata[x]['total'], ffdata[x]['percentile']]})
        else:
            fflogdictionary[ffdata[x]['encounterName']] = {ffdata[x]['spec'] : [ffdata[x]['total'], ffdata[x]['percentile']]}
    return(fflogdictionary)

def clear_count (ffdata):
    num = len(ffdata) #number of bosses
    bosses = {} #number of jobs per boss
    clears = {} #number of clears per boss
    for x in range(0, num):
        bosses[x] = len(ffdata[x]['specs'])
    for x in range(0, num):
        boss_clear = 0
        for y in range(0, bosses[x]):
            boss_clear = boss_clear + len(ffdata[x]['specs'][y]['data'])
        clears[x] = boss_clear
    return clears


def output(ff_data):
    num = len(ff_data) #number of bosses
    di = {}

    fflist = list(ff_data.keys()) #list of boss names
    for x in range(0, num): #finds number of jobs per boss
        di[x] = len(ff_data[fflist[x]])

    em = discord.Embed(colour=Data_output_color) #start of discord embed output for boss and parses

    for x in range(0, num): #created sentences
        bossname = fflist[x]
        say = ""
        for y in range(0, di[x]):
            percentile = int(ff_data[fflist[x]][list(ff_data[fflist[x]])[y]][1])
            if percentile % 10 == 1 and percentile != 11:
                percent = str(percentile) + "st"
            elif percentile % 10 == 2 and percentile != 12:
                percent = str(percentile) + "nd"
            elif percentile % 10 == 3 and percentile != 13:
                percent = str(percentile) + "rd"
            else:
                percent = str(percentile) + "th"
            deeps = ff_data[fflist[x]][list(ff_data[fflist[x]])[y]][0]
            classjob = list(ff_data[fflist[x]])[y]
            if percentile < 20:
                say = say + classjob + " with " + str(deeps) + " DPS and " + percent + ' percentile. ' + Low_percentile_warning + '\n'
            else:
                say = say + classjob + " with " + str(deeps) + " DPS and " + percent + ' percentile. \n'
        em.add_field(name = bossname, value = say, inline = False) #Addition of fields to the started embed
    return(em)

def bot_talks(name, server, region):
    #API location

    url = "https://www.fflogs.com/v1/rankings/character/" + name + "/" + server + "/" + region + "?api_key=" + fflogkey

    data = requests.get(url) #to obtain the data
    jdata = json.loads(data.text) #transform data to dictionary/list format
    code = data.status_code

    if code == 400:
        return(discord.Embed(title = Not_exist_text, colour=Not_exist_color))
    elif len(jdata) == 0:
        return(discord.Embed(title = Not_available_text, colour=Not_available_color))
    elif "hidden" in jdata:
        return(discord.Embed(title = Hidden_parse_error_text, colour=Hidden_parse_error_color))
    else:
        ff = fflogparse(jdata) #boss, job, dps, percent data

        realname = jdata[0]['characterName']
        charID = str(jdata[0]['characterID'])

        #start of icon image search
        html = urllib.request.urlopen('https://www.fflogs.com/character/id/' + charID)
        soup = BS(html, "html.parser")
        resultsimg = (soup.find("img", {"id" : "character-portrait-image"}))
        imgurl = resultsimg.get('src')

        botsays = output(ff)
        botsays.set_author(name=realname, url = 'https://www.fflogs.com/character/id/' + charID, icon_url=imgurl)

        return(botsays)

@client.command()
async def fflog(ctx, first: str, second:str, third:str):
    name = first + " " + second
    server = 'Jenova'
    region = 'NA'

    botwords = bot_talks(name, server, region)

    await ctx.send(embed = botwords)

@client.command()
async def fflogs(ctx, first: str, second:str):
    name = first + " " + second
    server = 'Jenova'
    region = 'NA'

    botwords = bot_talks(name, server, region)

    await ctx.send(embed = botwords)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="Embrace Freja"))


client.run(TOKEN)

