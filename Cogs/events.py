import discord
from discord.abc import GuildChannel
from discord.ext import commands

import helper as help


class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.invisible = True

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = help.get_guild_settings(member.guild.id)
        if settings[1] is None:
            return

        emb = discord.Embed(title=f"{member} присоединился", color=discord.Color.green())
        emb.set_thumbnail(url=member.avatar_url)
        time = member.joined_at.strftime("%d/%m/%Y, в %H:%M:%S")
        emb.set_footer(f"ID юзера: {member.id}; дата присоединения: {time}")

        await self.client.get_channel(settings[1]).send(embed=emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        settings = help.get_guild_settings(member.guild.id)
        if settings[1] is None:
            return

        emb = discord.Embed(title=f"{member} вышел/был удалён", color=discord.Color.red())
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(f"ID юзера: {member.id}")

        await self.client.get_channel(settings[1]).send(embed=emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        settings = help.get_guild_settings(message.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Сообщение удалено", color=discord.Color.red())
        emb.add_field(name="Удалённое сообщение:", value=f"```{message.content}```", inline=False)
        emb.add_field(name="Автор", value=f"{message.author.display_name} ({message.author.mention})", inline=False)
        emb.add_field(name="Канал", value=f"{message.channel.name} ({message.channel.mention})", inline=False)
        time = message.created_at.strftime("%d/%m/%Y, в %H:%M:%S")
        emb.set_footer(text=f"ID сообщения: {message.id}; дата создания: {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        settings = help.get_guild_settings(before.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Сообщение изменено", color=discord.Color.blue())
        emb.add_field(name="Старое содержимое:", value=f"```{before.content}```", inline=False)
        emb.add_field(name="Новое содержимое:", value=f"```{after.content}```", inline=False)
        emb.add_field(name="Автор", value=f"{before.author.display_name} ({before.author.mention})", inline=False)
        emb.add_field(name="Канал", value=f"{before.channel.name} ({before.channel.mention})", inline=False)
        time = after.edited_at.strftime("%d/%m/%Y, в %H:%M:%S")
        emb.set_footer(text=f"ID сообщения: {before.id}; дата изменения: {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel):
        settings = help.get_guild_settings(channel.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Канал создан", color=discord.Color.blurple())
        emb.add_field(name="Канал", value=f"{channel.mention}", inline=False)
        time = channel.created_at.strftime("%d/%m/%Y, в %H:%M:%S")
        emb.set_footer(text=f"ID канала: {channel.id}; дата создания: {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_guild_channel_create")
        await self.client.get_channel(settings[2]).send(str(channel))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        settings = help.get_guild_settings(channel.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Канал удалён", color=discord.Color.red())
        emb.add_field(name="Канал", value=f"={channel.mention}", inline=False)
        emb.set_footer(text=f"ID канала: {channel.id}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_guild_channel_delete")
        await self.client.get_channel(settings[2]).send(str(channel))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        settings = help.get_guild_settings(before.guild.id)
        if settings[2] is None:
            return

        if before.name != after.name:
            emb = discord.Embed(description="Изменено название канала", color=discord.Color.blue())
            emb.add_field(name="Старое название:", value=f"```{before.name}```", inline=False)
            emb.add_field(name="Новое название:", value=f"```{after.name}```", inline=False)
            emb.set_footer(text=f"ID канала: {after.id}")
            await self.client.get_channel(settings[2]).send(embed=emb)

        if before.position != after.position:
            emb = discord.Embed(description="Измненена позиция канала", color=discord.Color.blue())
            emb.add_field(name="Старая позиция:", value=f"```{before.name}```", inline=False)
            emb.add_field(name="Новая позиция:", value=f"```{after.name}```", inline=False)
            emb.set_footer(text=f"ID канала: {after.id}")
            await self.client.get_channel(settings[2]).send(embed=emb)

        if before.category != after.category:
            emb = discord.Embed(description="Изменена категория канала", color=discord.Color.blue())
            emb.add_field(name="Старая категория:", value=f"```{before.category}```", inline=False)
            emb.add_field(name="Новая категория:", value=f"```{after.category}```", inline=False)
            emb.set_footer(text=f"ID канала: {after.id}")
            await self.client.get_channel(settings[2]).send(embed=emb)

        if before.is_nsfw() != after.is_nsfw():
            emb = discord.Embed(description="Изменён NSFW-тег канала", color=discord.Color.blue())
            emb.add_field(name="Старый тег:", value=f"```{before.is_nsfw()}```", inline=False)
            emb.add_field(name="Новый тег:", value=f"```{after.is_nsfw()}```", inline=False)
            emb.set_footer(text=f"ID канала: {after.id}")
            await self.client.get_channel(settings[2]).send(embed=emb)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        settings = help.get_guild_settings(before.guild.id)
        if settings[2] is None:
            return

        await self.client.get_channel(settings[2]).send("on_member_update")
        await self.client.get_channel(settings[2]).send(str(before))
        await self.client.get_channel(settings[2]).send(str(after))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        settings = help.get_guild_settings(role.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Роль создана", color=discord.Color.green())
        emb.add_field(name="Название роли:", value=role.mention)
        time = role.created_at.strftime("%d/%m/%Y, в %H:%M:%S")
        emb.set_footer(text=f"ID роли: {role.id}; дата создания: {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_guild_role_create")
        await self.client.get_channel(settings[2]).send(str(role))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        settings = help.get_guild_settings(role.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Роль удалена", color=discord.Color.red())
        emb.add_field(name="Название роли:", value=role.mention)
        emb.set_footer(text=f"ID роли: {role.id}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_guild_role_delete")
        await self.client.get_channel(settings[2]).send(str(role))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        settings = help.get_guild_settings(before.guild.id)
        if settings[2] is None:
            return

        await self.client.get_channel(settings[2]).send("on_guild_role_update")
        await self.client.get_channel(settings[2]).send(str(before))
        await self.client.get_channel(settings[2]).send(str(after))

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: discord.Emoji, after: discord.Emoji):
        settings = help.get_guild_settings(guild.id)
        if settings[2] is None:
            return

        if before.name != after.name:
            emb = discord.Embed(title=f"Изменено название emoji {after}")
            emb.add_field(name=f"Старое название emoji:", value=before.name)
            emb.add_field(name="Новое название emoji:", value=after.name)
            emb.set_footer(text=f"ID emoji: {after.id}")

        # TODO: other cases

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_guild_emojis_update")
        await self.client.get_channel(settings[2]).send(str(before))
        await self.client.get_channel(settings[2]).send(str(after))

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.Member | discord.User):
        settings = help.get_guild_settings(guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Юзер забанен", color=discord.Color.red())
        emb.add_field(name="Имя юзера:", value=user.mention)
        time = user.joined_at.strftime("%d/%m/%Y, %H:%M:%S")
        emb.set_footer(text=f"ID юзера: {user.id}; дата присоединения: {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_member_ban")
        await self.client.get_channel(settings[2]).send(str(user))

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.Member | discord.User):
        settings = help.get_guild_settings(guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Юзер разбанен", color=discord.Color.green())
        emb.add_field(name="Имя юзера:", value=user.mention)
        time = user.joined_at.strftime("%d/%m/%Y, %H:%M:%S")
        emb.set_footer(text=f"ID юзера: {user.id}; дата присоединения: в {time}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_member_unban")
        await self.client.get_channel(settings[2]).send(str(user))

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        settings = help.get_guild_settings(invite.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Приглашение создано", color=discord.Color.green())
        emb.add_field(name="Приглашение:", value=invite.code)
        created_at = invite.created_at.strftime("%d/%m/%Y, в %H:%M:%S")
        expires_at = invite.expires_at.strftime("%d/%m/%Y, в %H:%M:%S")
        if expires_at is not None:
            emb.set_footer(
                text=f"ID прилашения: {invite.id}; дата создания приглащения: {created_at}, \
                дата истечения приглашения: {expires_at}")
        else:
            emb.set_footer(
                text=f"ID прилашения: {invite.id}; дата создания приглащения: {created_at}, \
                приглашение действует вечно")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_invite_create")
        await self.client.get_channel(settings[2]).send(str(invite))

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        settings = help.get_guild_settings(invite.guild.id)
        if settings[2] is None:
            return

        emb = discord.Embed(description="Приглашение удалено", color=discord.Color.red())
        emb.add_field(name="Приглашение:", value=invite.code)
        created_at = invite.created_at.strftime("%d/%m/%Y, %H:%M:%S")
        emb.set_footer(text=f"ID прилашения: {invite.id}; дата создания приглащения: {created_at}")

        await self.client.get_channel(settings[2]).send(embed=emb)
        await self.client.get_channel(settings[2]).send("on_invite_delete")
        await self.client.get_channel(settings[2]).send(str(invite))


def setup(client):
    client.add_cog(Events(client))
