import discord
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot

TOKEN = "NjAyNjA3OTU4MTE4ODkxNTQz.XTTrDw.TJsENZKkrHWnhY59FlqsLNOgyoY"
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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="Embrace Freja"))


client.run(TOKEN)

print('finished')
