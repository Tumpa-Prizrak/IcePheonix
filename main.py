# TODO CherryFox, Вы сделали что-то великое! В награду, я даю тебе эту клубнику!

import asyncio
import datetime
import json
import os
import random
import sys
import time
from colorama import Fore, Style

import aeval
import aiohttp
import discord
import requests
from discord.ext import commands, tasks

import helper as help

bot = commands.Bot(command_prefix=commands.when_mentioned_or(help.json_data['prefix']), intents=discord.Intents.all(),
                case_insensitive=True)
bot.remove_command("help")
# slash = InteractionClient(bot)
# Load Cogs
for i in os.listdir("Cogs/"):
    try:
        if i.endswith(".py"):
            bot.load_extension(f"Cogs.{i[:-3]}")
            help.Log.info(f"Load cog: Cogs.{i[:-3]}")
    except commands.errors.NoEntryPointError:
        pass


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(
            name="!help",
            platform="Twitch",
            details=f"{help.json_data['prefix']}help",
            game="Create bot",
            url="https://www.twitch.tv/andrew_k9"
        )
    )
    help.Log.log(f"Logged in as {bot.user}(ID: {bot.user.id})", code="ready", color=Fore.MAGENTA, style=Style.BRIGHT)


minify_text = lambda txt: f'{txt[:-900]}...\n# ...и ещё {len(txt.replace(txt[:-900], ""))} символов' if len(
    txt) >= 1024 else txt


@bot.command()
async def t(ctx, a: int):
    help = await bot.get_guild(a).invites()
    await ctx.send(help)


@bot.command(aliases=['eval', 'aeval', 'evaluate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    await ctx.message.delete()
    if ctx.author.id not in help.json_data['owners']:
        return await ctx.send("Кыш!")
    code = "\n".join(content.split("\n")[1:])[:-3] if content.startswith("```") and content.endswith("```") else content
    standard_args = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "tasks": tasks,
        "ctx": ctx,
        "asyncio": asyncio,
        "aiohttp": aiohttp,
        "os": os,
        'sys': sys,
        "time": time,
        "datetime": datetime,
        "random": random,
        "requests": requests
    }
    start = time.time()  # import time, для расчёта времени выполнения
    try:
        r = await aeval.aeval(f"""{code}""", standard_args, {})  # выполняем код
        ended = time.time() - start  # рассчитываем конец выполнения
        if not code.startswith('#nooutput'):
            # Если код начинается с #nooutput, то вывода не будет
            embed = discord.Embed(title="Успешно!", description=f"Выполнено за: {ended}", color=0x99ff99)
            embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`')
            embed.add_field(name=f'Выходные данные:', value=f'`{minify_text(str(r))}`', inline=False)
            await ctx.send(embed=embed)
    except Exception as e:
        ended = time.time() - start
        code = minify_text(str(code))
        embed = discord.Embed(title=f"При выполнении возникла ошибка.\nВремя: {ended}",
                            description=f'Ошибка:\n```py\n{e}```', color=0xff0000)
        embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`', inline=False)
        await ctx.send(embed=embed)
        raise e


try:
    bot.run(help.json_data['token'])
except aiohttp.ClientConnectionError:
    help.Log.error("Возможно вы не в сети, проверьте ваше интернет соеденение и попробуйте ещё раз")
