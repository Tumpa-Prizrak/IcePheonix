import discord
from discord.ext import commands

import helper as h


class Settings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.runame = 'Настройка'
        self.invisible = False

    @commands.command(usage="greetings [канал]", brief="<Квина, заполни плиз>")
    async def greetings(self, ctx: commands.Context, channel: discord.TextChannel = None):
        h.get_guild_settings(ctx.guild.id)
        if channel is None:
            h.do_to_database("UPDATE server_settings SET hello_channel_id=? WHERE guild_id=?", None, ctx.guild.id)
            await ctx.send(f"Канал для приветсвий сброшен", delete_after=h.json_data['delete_after']['command'])
        else:
            h.do_to_database("UPDATE server_settings SET hello_channel_id=? WHERE guild_id=?", channel.id, ctx.guild.id)
            await ctx.send(f"Канал для приветсвий установлен на {channel.mention}",
                           delete_after=h.json_data['delete_after']['command'])


def setup(client):
    client.add_cog(Settings(client))
