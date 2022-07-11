import datetime
import json
import sqlite3
import string
from discord.ext import commands
from time import sleep
from functools import partial
from colorama import init, Fore, Style

import discord
import random

json_data = json.load(open("config.json"))


def embed_builder(title: str, *, desc: str = None,
                  color: discord.Colour = discord.Colour.green()): return discord.Embed(title=title, description=desc,
                                                                                        color=color)


def database(command: str, *options, short: bool = True) -> list:
    dbFilename = json_data["db"]
    while True:
        try:
            conn = sqlite3.connect(dbFilename, timeout=1)
            cursor = conn.cursor()
            if not options:
                returnStr = list(cursor.execute(command))
            else:
                returnStr = list(cursor.execute(command, options))
            conn.commit()
            cursor.close()
            conn.close()
            return returnStr[0] if short and len(returnStr) == 1 else returnStr
        except sqlite3.OperationalError as e:
            create_log(e, code="error")
            sleep(1)
            continue


def get_profile_info(person: int):
    if not database("SELECT * FROM profile WHERE name = ?", person):
        database("INSERT INTO profile values (?, ?, ?, ?)", person, None, None, 0)
    return database("SELECT * FROM profile WHERE name = ?", person)


def get_guild_settings(guild: int):
    if not database("SELECT * FROM server_settings WHERE guild_id = ?", guild):
        database("INSERT INTO server_settings values (?, ?, ?)", guild, None, None)
    return database("SELECT * FROM server_settings WHERE guild_id = ?", guild)


def create_log(message: str, code: str = "ok", logged: bool = True):
    out = f"[{code.upper()}][{str(datetime.datetime.now())[:19]}]: {message}"
    print(out)

    if logged:
        with open(f"logs/log_{datetime.date.today()}.txt", "a", encoding="UTF-8") as file:
            file.write("\n" + out)


def get_max_from_value(variant: dict):
    out = []
    while len(variant) != 0:
        max_value = list(variant.keys())[0]
        for i in variant.keys():
            if variant[i] > variant[max_value]:
                max_value = i
        out.append(max_value)
        variant.pop(max_value)
    return out


class Log:
    @staticmethod
    def log(content: str = None, *, code: str = "ok", logged: bool = True, color=Fore.WHITE, style=Style.NORMAL):
        output = Log.__generate_output(content, code)
        print(f"{color}{style}{output}")
        if logged:
            Log.__to_txt(output)

    info = partial(log, code="info", color=Fore.BLUE, style=Style.BRIGHT)
    error = partial(log, code="error", logged=False, color=Fore.RED, style=Style.BRIGHT)
    debug = partial(log, code="debug", logged=False, color=Fore.YELLOW)
    command = partial(log, code="command", color=Fore.LIGHTGREEN_EX)

    @staticmethod
    async def discord(log_channel_id: int, interaction: commands.Context, **kwargs):
        try:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await log_channel.send(**kwargs)
        except Exception as e:
            Log.error(e, logged=False)

    @staticmethod
    def __to_txt(output):  # sourcery skip: instance-method-first-arg-name
        with open(f"logs/log_{datetime.date.today()}.txt", "a", encoding="UTF-8") as file:
            file.write("\n" + output)

    @staticmethod
    def __generate_output(message: str = None, code: str = "ok"):
        return f"[{str(datetime.datetime.now())[:19]}][{code.upper()}]: {message}"  # TODO remove [:19]


def log_deleted_message(
        message: discord.Message,
        filename: str
):
    with open(f"logs/log_{filename}.txt", "a", encoding="UTF-8") as file:
        file.write(f"\n [{str(message.created_at)[:19]}] {message.author}: {message.content or message.attachments}")


def random_word(length):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))
