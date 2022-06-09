import discord
from discord.ext import commands
import sqlite3
conn = sqlite3.connect("Cogs/mysqldb.db")
curor = conn.cursor()


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.invisible = True
    
    #TODO delete this or add some usefull staff

    # @commands.Cog.listener()
    # async def on_message(self, mess):
    #     Is_on_mute = list(curor.execute("SELECT * FROM mutes"))
    #     for i in Is_on_mute:
    #         if i[0] == mess.author.id and i[1] == mess.guild.id:
    #             await mess.delete()
    #             break


def setup(client):
    client.add_cog(Events(client))
