import discord
from discord.ext import commands

import helper as help


class Settings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.runame = 'Настройка'
        self.invisible = False

    @commands.command(usage="greetings [канал]")
    async def greetings(self, ctx: commands.Context, channel: discord.TextChannel = None):
        help.get_guild_settings(ctx.guild.id)
        if channel is None:
            help.database("UPDATE server_settings SET hello_channel_id=? WHERE guild_id=?", None, ctx.guild.id)
            await ctx.send(f"Канал для приветсвий сброшен", delete_after=help.json_data['delete_after']['command'])
        else:
            help.database("UPDATE server_settings SET hello_channel_id=? WHERE guild_id=?", channel.id, ctx.guild.id)
            await ctx.send(f"Канал для приветсвий установлен на {channel.mention}",
                        delete_after=help.json_data['delete_after']['command'])

    @commands.command()
    async def events(self, ctx: commands.Context):
        # TODO
        pass

    @commands.command()
    async def settings(self, ctx: commands.Context):
        # TODO
        pass


def setup(client):
    client.add_cog(Settings(client))
