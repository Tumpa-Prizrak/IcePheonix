import discord
from discord.ext import commands

import helper as h


class ModerationCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.someShit = {
            "user": "<Человек>",
            "reason": "<Причина>"
        }
        self.runame = 'Модерация'
        self.invisible = False

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен",
                                    colour=discord.colour.Colour.red())
                await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен",
                                    colour=discord.colour.Colour.red())
                await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        elif isinstance(error, discord.Forbidden):
            emb = discord.Embed(title="Я не могу это сделать, прав не хватает :sob:")
            await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        else:
            raise error

    @commands.command(
        usage='ban <Участник> [причина]',
        brief='Дать Фениксу в лапы Банхаммер и стукнуть им человека',
        description='Банит человека по указанной причине. Он не сможет вернуться на сервер с этого '
                    'аккаунта вплоть до его разбана. Требуется право ban_members (банить участников) '
                    'как у бота, так и у вызвавшего команду'
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason="Bad guy"):
        await ctx.message.delete()
        if user == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        if ctx.author.top_role.position <= user.top_role.position or ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions()

        await user.ban(reason=reason)
        emb = discord.Embed(title=f"**{user.display_name}** был забанен", colour=discord.colour.Color.green())

        await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['command'])

    @commands.command(
        usage='kick <Участник> [причина]',
        brief='Выгнать участника с сервера',
        description='При помощи данной команды можно выгнать человека с сервера. Он сможет вернуться по '
                    'ссылке-приглашению. Требуется право kick_members (выгонять участников) как у бота,'
                    'так и у вызвавшего команду'
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str = "Bad guy"):
        await ctx.message.delete()
        if user == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        if ctx.author.top_role.position <= user.top_role.position or ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions()
        await user.kick(reason=reason)
        emb = discord.Embed(title=f"**{user.display_name}** был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['command'])

    @commands.command(
        usage='warn <Участник> <причина>',
        brief='Выдать участнику предупреждение',
        description='Выдаёт предупреждение по указанной причине. Список предупреждений можно посмотреть '
                    'командой  warns. Требуется право manage_roles(управлять ролями) у вызвавшего команду.'
    )
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx: commands.Context, user: discord.Member, *, reason: str = "без причины"):
        await ctx.message.delete()
        h.database("INSERT INTO warns (person, server, warn, moderator) VALUES (?, ?, ?, ?)",
                   user.id, ctx.guild.id,
                   reason, ctx.author.id)
        await ctx.send(
            f"{user.mention} было выдано предупреждение по причине \"{reason}\" модератором {ctx.author.mention}",
            delete_after=h.json_data['delete_after']['command'])

    @commands.command(
        usage='warns <Участник>',
        brief='список предупреждений участника',
        description='<Квина, заполни, плиз>'
    )
    async def warns(self, ctx: commands.Context, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        user_warns = h.database("SELECT * FROM warns WHERE person=? and server=?", user.id, ctx.guild.id, short=False)
        emb = discord.Embed(title=f"\"{user.display_name}\" warns")
        if not user_warns:
            emb.description = "*Пусто*"
        else:
            emb.description = "\n".join(map(
                lambda x:
                f"#{x[0]}: {self.client.get_user(x[4]).mention if self.client.get_user(x[4]) is not None else 'Неизвестно'} - {x[3]}",
                user_warns)
            )
            emb.set_footer(text="#Номер нарушения: модератор - Причина")
        await ctx.send(embed=emb)

    @commands.command(
        usage='clear <количество>',
        brief='Очищает указанное количество сообщений',
        description="<Квина, заполни, плиз>"
    )
    async def clear(self, ctx: commands.Context, amount: int):
        await ctx.message.delete()
        if amount <= 0:
            return await ctx.send(
                "Параметр `amount` должен быть больше нуля",
                delete_after=h.json_data['delete_after']['error']
            )
        await ctx.channel.purge(limit=amount)

    # TODO mute/unmute/tempmute


async def setup(client):
    await client.add_cog(ModerationCommand(client))
