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

    @commands.Cog.listener()
    async def on_message_delete(self, guild: discord.Guild):
        h.get_guild_settings(guild.id)

    @commands.Cog.listener()
    async def on_message_edit(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_private_channel_delete(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_private_channel_create(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_private_channel_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_webhooks_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_member_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_invite_create(self, guild: discord.Guild):
        pass

    @commands.Cog.listener()
    async def on_invite_delete(self, guild: discord.Guild):
        pass


def setup(client):
    client.add_cog(Events(client))
