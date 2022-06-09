import asyncio
import datetime
import json
import os
import random
import sqlite3
import sys
import time

import aeval
import aiohttp
import discord
import requests
from discord.ext import commands, tasks

import helper as h

json_data = json.load(open("config.json"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or(json_data['prefix']), intents=discord.Intents.all(),
                   case_insensitive=True)
bot.remove_command("help")
# slash = InteractionClient(bot)
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()
# Load Cogs
for i in os.listdir("Cogs/"):
    try:
        if i.endswith(".py"):
            bot.load_extension(f"Cogs.{i[:-3]}")
            print(f"Load cog: Cogs.{i[:-3]}")
    except commands.errors.NoEntryPointError:
        pass


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(
            name="!help",
            platform="Twitch",
            details=f"{json_data['prefix']}help",
            game="Create bot",
            url="https://www.twitch.tv/andrew_k9"
        )
    )
    print("Ready")


minify_text = lambda txt: f'{txt[:-900]}...\n# ...и ещё {len(txt.replace(txt[:-900], ""))} символов' if len(
    txt) >= 1024 else txt


@bot.command(aliases=['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    if ctx.author.id not in json_data['owners']:
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
            """
             Есть нюанс: если входные/выходные данные будут длиннее 1024 символов, то эмбед не отправится, а функция выдаст ошибку.
             Именно поэтому сверху стоит print(r), а так же есть функция minify_text, которая
             минифицирует текст для эмбеда во избежание БэдРеквеста (слишком много символов).
            """
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
    bot.run(json_data['token'])
except aiohttp.ClientConnectionError:
    print("Возможно вы не в сети, проверте ваше интернет соеденение и попробуйте ещё раз")
