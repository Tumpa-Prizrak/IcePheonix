# TODO CherryFox, Вы сделали что-то великое! В награду, я даю тебе эту клубнику!

import asyncio
import contextlib
import datetime
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

import helper as h


class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(
            application_id=h.json_data["application_id"],
            intents=intents,
            command_prefix=commands.when_mentioned_or(h.json_data['prefix']),
            case_insensitive=True,
            # strip_after_prefix=True,
            # owner_ids=JSON_DATA["owners"],
        )

    async def setup_hook(self):
        for cog in os.listdir("Cogs"):
            with contextlib.suppress(commands.errors.NoEntryPointError):
                if cog.endswith(".py"):
                    try:
                        await bot.load_extension(f"Cogs.{cog[:-3]}")
                        h.Log.info(f"Load cog: Cogs.{cog[:-3]}")
                    except Exception as e:
                        h.Log.error(f"cog Cogs.{cog[:-3]} failed to load due to error: {e}.")


bot = MyBot(intents=discord.Intents.all())

bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Streaming(
            name="!help",
            platform="Twitch",
            details=f"{h.json_data['prefix']}help",
            game="Creating a bot",
            url="https://www.twitch.tv/andrew_k9"
        )
    )
    h.Log.log(f"Logged in as {bot.user}(ID: {bot.user.id})", code="ready", color=Fore.MAGENTA, style=Style.BRIGHT)


def minify_text(text):
    if len(text) > 1024:
        return f"{text[:950]}...\n# ...и ещё {len(text.replace(text[:950]))} символов"
    return text


'''
@bot.command()
async def t(ctx, guild: int):
    help = await bot.get_guild(guild).invites()
    await ctx.send(help)
'''


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
    h.Log.error("Возможно вы не в сети, проверьте ваше интернет соеденение и попробуйте ещё раз")
