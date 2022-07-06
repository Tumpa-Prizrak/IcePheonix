import discord
from discord.ext import commands

import helper as h


class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.invisible = True

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        setts = h.get_guild_settings(member.guild.id)
        if setts[1] is None:
            return
        emb = discord.Embed(title=f"{member} присоеденился", color=discord.Color.green())
        emb.set_thumbnail(url=member.avatar_url)
        await self.client.get_channel(setts[1]).send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        setts = h.get_guild_settings(member.guild.id)
        if setts[1] is None:
            return
        emb = discord.Embed(title=f"{member} вышел", color=discord.Color.red())
        emb.set_thumbnail(url=member.avatar_url)
        await self.client.get_channel(setts[1]).send(embed=emb)


def setup(client):
    client.add_cog(Events(client))
