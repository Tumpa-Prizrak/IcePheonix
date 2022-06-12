import discord
from discord.ext import commands
import helper as h


class OtherCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.runame = 'Остальное'
        self.invisible = False

    @commands.command()
    async def help(self, ctx, *, cmd_input=None):
        if cmd_input is None:
            emb = discord.Embed(title="Команды:", colour=discord.colour.Colour.green())
            emb.set_footer(
                text=f"Можешь прописать {ctx.prefix}help <команда>, чтобы узнать больше про нужную команду :)",
                icon_url="https://cdn.discordapp.com/attachments/880063679570259969/897478783215476826/0c5aa927105c867558d290d6a1f3f72f.webp")
            for cog in self.client.cogs.values():
                if not getattr(cog, 'invisible'):
                    emb.add_field(name=f'**{cog.runame}:**', value=" ".join(f'`{i.name}`' for i in cog.get_commands()),
                                  inline=False)
        else:
            for cmd in self.client.commands:
                if cmd.name == cmd_input:
                    emb = discord.Embed(title=f"Команда {cmd.name}",
                                        description=f'Синтаксис: {ctx.prefix}{cmd.usage if cmd.usage else cmd.name}',
                                        colour=discord.colour.Colour.green())
                    emb.add_field(name=cmd.brief if cmd.brief else '<нет краткого описания>',
                                  value=cmd.description if cmd.description else '** **')
                    break
        await ctx.send(embed=emb)

    @commands.command(usage='ping', brief='Показывает пинг бота')
    async def ping(self, ctx):
        await ctx.send(f"Понг! Задержка {round(self.client.latency * 1000)} мс")

    @commands.command(usage='profile', brief='Показывает ваш профиль')
    async def profile(self, ctx: commands.Context, person: discord.Member = None):
        if person == None:
            person = ctx.author
        info = h.get_profile_info(person)
        print(info)
        emb = discord.Embed(title="Ваш профиль" if person == None else f"Профиль {person.display_name}",
                            color=person.top_role.colour)
        emb.set_author(name=str(person))
        emb.set_thumbnail(url=person.avatar_url)
        emb.add_field(name=f"Статус", value=str(person.status), inline=False)
        emb.add_field(name=f"Активность", value=str(person.activity), inline=False)
        emb.add_field(name="Обо мне", value=info[1] if info[1] is not None else "*Ничего не сказано*")
        emb.add_field(name=f"ID", value=str(person.id), inline=False)
        emb.add_field(name="Дата регистрации",
                      value=f"<t:{round(person.created_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Дата вступления",
                      value=f"<t:{round(person.joined_at.timestamp())}:R>",
                      inline=False)
        emb.add_field(name="Высшая роль", value=person.top_role, inline=False)
        all_roles = ", ".join(list(map(lambda x: x.mention, person.roles)))
        emb.add_field(name="Роли", value=all_roles if len(emb) + len(
            all_roles) < 1000 else "*Недоступно*")  # FIXME spliting instade "*Недоступно*"
        if info[2] is not None:
            emb.set_image(url=info[2])
        await ctx.send(embed=emb)

    @commands.command(usage='set <about | picture> <значение>')
    async def set(self, ctx: commands.Context, colum: str, *, val: str = None):
        if colum in ('about', 'a'):
            h.do_to_database("UPDATE profile SET about=? WHERE name=?", val, ctx.author.id)
            await ctx.send(f"Значение \"Обо мне\" изменено на {val}" if val is not None else "Значение")
        elif colum in ('picture', 'pic', 'p'):
            h.do_to_database("UPDATE profile SET pic=? WHERE name=?", val, ctx.author.id)
            await ctx.send("Картинка изменена")
        else:
            await ctx.send('Неправильный аттрибут. Возможные значения: info | picture')

    # TODO vote


def setup(client):
    client.add_cog(OtherCommand(client))
