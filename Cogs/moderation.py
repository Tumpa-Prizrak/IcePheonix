import discord
from discord.ext import commands

import helper as h


class ModerationCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.someShit = {
            "man": "<Человек>",
            "reason": "<Причина>"
        }
        self.runame = 'Модерация'
        self.invisible = False

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен",
                                    colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен",
                                    colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            emb = discord.Embed(title="Я не могу это сделать, прав не хватает :sob:")
            await ctx.send(embed=emb)
        else:
            raise error

    @commands.command(usage='ban <Участник> [причина]', brief='Дать Фениксу в лапы Банхаммер и стукнуть им человека',
                      description='Банит человека по указанной причине. Он не сможет вернуться на сервер с этого '
                                  'аккаунта вплоть до его разбана. Требуется право ban_members (банить участников) '
                                  'как у бота, так и у вызвавшего команду')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason="Bad guy"):
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb)
        if ctx.author.top_role.position <= man.top_role.position or ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions()
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"**{man.display_name}** был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @commands.command(usage='kick <Участник> [причина]', brief='Выгнать участника с сервера',
                      description='При помощи данной команды можно выгнать человека с сервера. Он сможет вернуться по '
                                  'ссылке-приглашению. Требуется право kick_members (выгонять участников) как у бота, '
                                  'так и у вызвавшего команду')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, man: discord.Member, *, reason: str = "Bad guy"):
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb)
        if ctx.author.top_role.position <= man.top_role.position or ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions()
        await man.kick(reason=reason)
        emb = discord.Embed(title=f"**{man.display_name}** был кикнут", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @commands.command(usage='warn <Участник> <причина>', brief='Выдать участнику предупреждение',
                      description='Выдаёт предупреждение по указанной причине. Список предупреждений можно посмотреть '
                                  'командой  warns. Требуется право manage_roles(управлять ролями) у вызвавшего '
                                  'команду.')
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx: commands.Context, man: discord.Member, *, reason: str):
        h.do_to_database("INSERT INTO warns (person, server, warn, moderator) VALUES (?, ?, ?, ?)",
                         man.id, ctx.guild.id, reason, ctx.author.id)
        await ctx.send(
            f"{man.mention} было выдано предупреждение по причине \"{reason}\" модератором {ctx.author.mention}")

    @commands.command(usage='warns <Участник>', brief='список предупреждений участника',
                      description='<Квина, заполни, плиз>')
    async def warns(self, ctx: commands.Context, man: discord.Member = None):
        if man is None:
            man = ctx.author
        man_warns = h.do_to_database("SELECT * FROM warns WHERE person=? and server=?", man.id, ctx.guild.id, if_short=False)
        emb = discord.Embed(title=f"\"{man.display_name}\" warns")
        if not man_warns:
            emb.description = "*Пусто*"
        else:
            await ctx.send(str(man_warns))
            emb.description = "\n".join(map(lambda x: f"#{x[0]}: {self.client.get_user(x[4]).mention if self.client.get_user(x[4]) is not None else 'Неизвестно'} - {x[3]}",
                                            man_warns))
            emb.set_footer(text="#Номер нарушения: модератор - Причина")
        await ctx.send(embed=emb)
    
    @commands.command(usage='clear <количество>', brief='Очищает указанное количество сообщений', 
                      description="<Квина, заполни, плиз>")
    async def clear(self, ctx: commands.Context, count: int):
        pass

    # TODO mute


def setup(client):
    client.add_cog(ModerationCommand(client))
