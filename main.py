# TODO CherryFox, Вы сделали что-то великое! В награду, я даю тебе эту клубнику!

import asyncio
import datetime
import json
import os
import random
import sys
import time

import aeval
import aiohttp
import discord
import requests
from discord.ext import commands, tasks

import helper as h

bot = commands.Bot(command_prefix=commands.when_mentioned_or(h.json_data['prefix']), intents=discord.Intents.all(),
                   case_insensitive=True)
bot.remove_command("help")
# slash = InteractionClient(bot)
# Load Cogs
for i in os.listdir("Cogs/"):
    try:
        if i.endswith(".py"):
            bot.load_extension(f"Cogs.{i[:-3]}")
            h.create_log(f"Load cog: Cogs.{i[:-3]}")
    except commands.errors.NoEntryPointError:
        pass


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(
            name="!help",
            platform="Twitch",
            details=f"{h.json_data['prefix']}help",
            game="Create bot",
            url="https://www.twitch.tv/andrew_k9"
        )
    )
    h.create_log("Ready")


minify_text = lambda txt: f'{txt[:-900]}...\n# ...и ещё {len(txt.replace(txt[:-900], ""))} символов' if len(
    txt) >= 1024 else txt


@bot.command(aliases=['eval', 'aeval', 'evaluate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    await ctx.message.delete()
    if ctx.author.id not in h.json_data['owners']:
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
    bot.run(h.json_data['token'])
except aiohttp.ClientConnectionError:
    h.create_log("Возможно вы не в сети, проверте ваше интернет соеденение и попробуйте ещё раз", "error")
