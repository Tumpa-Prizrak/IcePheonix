import discord
from discord.ext import commands

import helper as help


class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.runame = 'Экономика'
        self.invisible = False

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            emb = discord.Embed(title="Бро, у тебя нет прав", colour=discord.colour.Colour.red())
            await ctx.send(embed=emb, delete_after=help.json_data['delete_after']['error'])
        else:
            raise error

    @commands.command(usage='balance [пользователь]', aliases=['bal', 'money', 'mon'])
    async def balance(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author
        data = help.get_profile_info(user.id)
        await ctx.send(embed=discord.Embed(title=f"Баланс пользователя {user.display_name}", description=f"Баланс составляет {data[3]}$"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx: commands.Context, user: discord.Member, value: int):
        if value <= 0:
            return await ctx.send("Количество должно быть положительным")
        help.database("UPDATE profile SET money=? WHERE name=?",
                      help.database("SELECT money FROM profile WHERE name=?", user.id)[0] + value, user.id)
        await ctx.send("Выполнено :thumbsup:", delete_after=help.json_data['delete_after']['command'])

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx: commands.Context, user: discord.Member, value: int):
        if value <= 0:
            return await ctx.send("Количество должно быть положительным")
        help.database("UPDATE profile SET money=? WHERE name=?",
                      help.database("SELECT money FROM profile WHERE name=?", user.id)[0] - value, user.id)
        await ctx.send("Выполнено :thumbsup:", delete_after=help.json_data['delete_after']['command'])


def setup(client):
    client.add_cog(Economy(client))
