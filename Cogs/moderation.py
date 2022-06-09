import discord
from discord.ext import commands

doc = """Дать Фениксу в лапы Банхаммер и указать на человека"""
syntax = "ban <Человек> [Причина]"


class ModerationCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.someShit = {
            "man": "<Человек>"
        }
        self.runame = 'Модерация'
        self.invisible = False

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb)
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                emb = discord.Embed(title=f"Параметр \"{self.someShit[error.param.name]}\" пропущен", colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
            except KeyError:
                emb = discord.Embed(title=f"Параметр \"{error.param.name}\" пропущен", colour=discord.colour.Colour.red())
                await ctx.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            emb = discord.Embed(title="Я не могу это сделать, прав не хватает :sob:")
            await ctx.send(embed=emb)
        else:
            raise error

    @commands.command(usage = 'ban <Участник> [причина]', brief='Дать Фениксу в лапы Банхаммер и стукнуть им человека', description = 'Банит человека по указанной причине. Он не сможет вернуться на сервер с основного аккаунта вплоть до его разбана. Требуется право ban_members (банить участников) как у бота, так и у вызвавшего команду')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, man: discord.Member, *, reason = "Bad guy"):
        if man == ctx.author:
            emb = discord.Embed(title="Вы не можете сделать это с собой  :sob:", colour=discord.colour.Colour.red())
            return await ctx.send(embed=emb)
        if ctx.author.top_role.position <= man.top_role.position or ctx.guild.owner != ctx.author:
            raise commands.MissingPermissions()
        await man.ban(reason=reason)
        emb = discord.Embed(title=f"**{man.display_name}** был забанен", colour=discord.colour.Color.green())
        await ctx.send(embed=emb)

    @commands.command(usage = 'kick <Участник> [причина]', brief = 'Выгнать участника с сервера', description='При помощи данной команды можно выгнать человека с сервера. Он сможет вернуться по ссылке-приглашению, если найдёт её. Требуется право kick_members (выгонять участников) как у бота, так и у вызвавшего команду')
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

    #TODO mute
    #TODO warn 
    #TODO warns


def setup(client):
    client.add_cog(ModerationCommand(client))
