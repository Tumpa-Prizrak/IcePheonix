import discord
from discord.ext import commands
import aiohttp
from random import randint
import typing
import helper as h


class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
        self.runame = 'Реакции'
        self.invisible = False

    async def cog_command_error(self, ctx, error):
        chel = '<Человек>'
        if isinstance(error, commands.MissingRequiredArgument):
            qu = '<{}>'
            emb = discord.Embed(
                title=f"Параметр {qu.format(chel if error.param.name == 'person' else error.param.name)} пропущен",
                description=f'Правильное использование команды: {ctx.command.usage}',
                colour=discord.colour.Colour.red())
            await ctx.send(embed=emb, delete_after=h.json_data['delete_after']['error'])
        else:
            raise error

    async def get_gif(self, param):
        async with self.session.get(  # TODO change api? and replace apikey to new
            f"https://g.tenor.com/v1/search?q={param.replace(' ', '%20')}&key={h.json_data['apikey']}&limit={str(h.json_data['limit'])}"
        ) as r:
            if r.status == 200:
                while 1:
                    try:
                        return (await r.json())["results"][randint(0, h.json_data["limit"])]["media"][0]['gif']['url']
                    except IndexError:
                        continue
            else:
                return r.status

    @staticmethod
    async def build_embed(reaction, author, action, words, target=None, err="Вы не можете сделать это с собой :sob:"):
        if target is not None:
            if author == target:
                return discord.Embed(
                    title=err,
                    colour=discord.colour.Colour.red()
                )
        if not isinstance(reaction, int):
            if type(target) == str:
                return discord.Embed(
                    title=f"{author.name} {action} {target}" + f" со словами {words}" if words is not None else "",
                    colour=discord.colour.Colour.green()).set_image(url=reaction)
            else:
                return discord.Embed(
                    title=f"{author.name} {action} {target.name if target is not None else ''}" \
                          + f"{'со словами' + words if words is not None else ''}",
                    colour=discord.colour.Colour.green()).set_image(url=reaction)
        else:
            return discord.Embed(title=f"Произошла неожиданная ошибка. Код ошибки: {reaction}",
                                 colour=discord.colour.Colour.red())

    @commands.command(usage='baka <Человек>', brief='Отругать кого-то')
    async def baka(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime baka')
        emb = await self.build_embed(reaction, ctx.author, 'ругает', words, person, "Вы отругали себя. Вы садитесь в угол и начинаете плакать")
        await ctx.send(embed=emb)

    @commands.command(usage='bang head', brief='Долбиться головой об стену')
    async def bang(self, ctx, second: str, *, words: str = None):
        if second != "head": return
        await ctx.message.delete()
        reaction = await self.get_gif('anime bang head')
        emb = await self.build_embed(reaction, ctx.author, 'бьётся головой о стену', words)
        await ctx.send(embed=emb)

    @commands.command(usage='bite <Человек>', brief='Укусить кого-то')
    async def bite(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime bite')
        emb = await self.build_embed(reaction, ctx.author, 'укусил(а)', words, person, "Вы кусаете себя, вам больно")
        await ctx.send(embed=emb)

    @commands.command(usage='blush', brief='Покраснеть')
    async def blush(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime blush')
        emb = await self.build_embed(reaction, ctx.author, 'краснеет', words)
        await ctx.send(embed=emb)

    @commands.command(usage='cry', brief='Поплакать. Не надо плакать :(')
    async def cry(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime cry')
        emb = await self.build_embed(reaction, ctx.author, 'плачет', words)
        await ctx.send(embed=emb)

    @commands.command(usage='cuddle <Человек>', brief='Прижаться к кому-то')
    async def cuddle(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime cuddle')
        emb = await self.build_embed(reaction, ctx.author, 'прижался(ась) к', words, person, "Вы пытаетесь прижаться к самому/самой себею. Вы ломаете себе плечи")
        await ctx.send(embed=emb)

    @commands.command(usage='dance [Человек]', brief='Потанцевать с кем-то или в одиночку')
    async def dance(self, ctx, person: typing.Union[discord.Member, str] = None, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime dance')
        emb = await self.build_embed(reaction, ctx.author, 'танцует' if person is None else 'танцует с', words, person)
        await ctx.send(embed=emb)

    @commands.command(usage='drink [Человек]', brief='БУХАЕМ!!! Выпить напиток. С другом или без')
    async def drink(self, ctx, person: typing.Union[discord.Member, str] = None, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime drink tea')
        emb = await self.build_embed(reaction, ctx.author, 'пьёт' if person is None else 'пьёт с', words, person)
        await ctx.send(embed=emb)

    @commands.command(usage='feed <Человек>', brief='Покормить кого-то')
    async def feed(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime feed')
        emb = await self.build_embed(reaction, ctx.author, 'покормил(а)', words, person, "Что вы делаете в моём холодильнике? Вы что хотите кушать?")
        await ctx.send(embed=emb)

    @commands.command(usage='high five <Человек>', brief='Пятюню? Дать "пять" кому-то')
    async def high(self, ctx, second: str, person: typing.Union[discord.Member, str], *, words: str = None):
        if second != "five": return
        await ctx.message.delete()
        reaction = await self.get_gif('anime high five')
        emb = await self.build_embed(reaction, ctx.author, 'дал(а) пять', words, person, "Вы хлопаете в ладоши")
        await ctx.send(embed=emb)

    @commands.command(usage='flip', brief='Перевернуть стол... Стоп, а ПК?!')
    async def flip(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime table flip')
        emb = await self.build_embed(reaction, ctx.author, 'опрокинул(а) стол', words)
        await ctx.send(embed=emb)

    @commands.command(usage='hit <Человек>', brief='Дать по щам кому-нибудь')
    async def hit(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime hit')
        emb = await self.build_embed(reaction, ctx.author, 'ударил(а)', words, person)
        await ctx.send(embed=emb)

    @commands.command(usage='hug <Человек>', brief='Обнимашкиииии!!! Обнимем кого-то?')
    async def hug(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime hug')
        emb = await self.build_embed(reaction, ctx.author, 'обнял(а)', words, person, "Вы обнялись со своей шизой")
        await ctx.send(embed=emb)

    @commands.command(usage='innocent', brief='Я точно не импостер, не, ну серьёзно :D')  # Брон молодец
    async def innocent(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime innocent')
        emb = await self.build_embed(reaction, ctx.author, 'оправдывается', words)
        await ctx.send(embed=emb)

    @commands.command(usage='kill <Человек>', brief='РЕЗНЯ! Убить кого-то')
    async def kill(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime kill')
        emb = await self.build_embed(reaction, ctx.author, 'убил(а)', words, person, "Суицид - не выход! Осуждаю!")
        await ctx.send(embed=emb)

    @commands.command(usage='kiss <Человек>', brief='Поцелуемся с кем-то? \*чмок*')  # \* чтобы не выделялось курсивом
    async def kiss(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime kiss')
        emb = await self.build_embed(reaction, ctx.author, 'поцеловал(а)', words, person, "Вы целуетесь с зеркалом, но вас палит ваша мама")
        await ctx.send(embed=emb)

    @commands.command(usage='lick <Человек>', brief='Лизни кого-то)')
    async def lick(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime lick')
        emb = await self.build_embed(reaction, ctx.author, 'лизнул(а)', words, person, "Вы попытались дотянутся языком до кончика носа. У вас ожидаемо не получается")
        await ctx.send(embed=emb)

    @commands.command(usage='pat <Человек>', brief='Кто тут у нас хороший? А ну иди сюда, поглажу :)')
    async def pat(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime pat')
        emb = await self.build_embed(reaction, ctx.author, 'погладил(а)', words, person, "Вы гладите себя по голове но вам от этого стало грустно")
        await ctx.send(embed=emb)

    @commands.command(usage='poke <Человек>', brief='Тыкнуть в кого-то')
    async def poke(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime poke')
        emb = await self.build_embed(reaction, ctx.author, 'тыкнул(а) в', words, person, "Вы тыкаете себя в щёку. Вам не больно")
        await ctx.send(embed=emb)

    @commands.command(usage='scare <Человек>', brief='Бу! Напугать кого-то')
    async def scare(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime scare')
        emb = await self.build_embed(reaction, ctx.author, 'испугал(а)', words, person, "Вы испугали сами себя и получили инфаркт")
        await ctx.send(embed=emb)

    @commands.command(usage='slap <Человек>', brief='Дать подщёчину кому-то')
    async def slap(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime slap')
        emb = await self.build_embed(reaction, ctx.author, 'дал(а) подщёчину', words, person, "Вы ударили себя и у вас появился фингал под глазом")
        await ctx.send(embed=emb)

    @commands.command(usage='sleep', brief='Поспать. Спокойной ночи 💤')
    async def sleep(self, ctx, *, words: str = None):
        reaction = await self.get_gif('anime sleep')
        emb = await self.build_embed(reaction, ctx.author, 'спит', words)
        await ctx.send(embed=emb)

    @commands.command(usage='tickle <Человек>', brief='Пощекотать кого-то')
    async def tickle(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime tickle')
        emb = await self.build_embed(reaction, ctx.author, 'пощекотал(а)', words, person, "Вы щекотите самого себя но вас посчитали за шизика")
        await ctx.send(embed=emb)

    @commands.command(usage='walk [Человек]', brief='Ходить, гулять, бродить')
    async def walk(self, ctx, person: typing.Union[discord.Member, str] = None, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime walk')
        emb = await self.build_embed(reaction, ctx.author, 'гуляет' if person is None else 'гуляет с', words, person)
        await ctx.send(embed=emb)
    
    @commands.command(usage="two stripes <Человек>", brief="<Квина, сделай пж>")
    async def two(self, ctx, second: str, person: typing.Union[discord.Member, str], *, words: str = None):
        if second != "stripes": return
        await ctx.message.delete()
        reaction = await self.get_gif('anime two stripes')
        emb = await self.build_embed(reaction, ctx.author, 'Показал(а) две полоски', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='catch <Человек>', brief='<Квина, сделай пж>')
    async def catch(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime catch')
        emb = await self.build_embed(reaction, ctx.author, 'поймал(а)', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='squish <Человек>', brief='<Квина, сделай пж>')
    async def squish(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime squish')
        emb = await self.build_embed(reaction, ctx.author, 'тискает', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='marry <Человек>', brief='<Квина, сделай пж>')
    async def marry(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime marry')
        emb = await self.build_embed(reaction, ctx.author, 'Сделал(а) предложение руки и сердца', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='love <Человек>', brief='<Квина, сделай пж>')
    async def love(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime love')
        emb = await self.build_embed(reaction, ctx.author, 'Признался(ась) в любви', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='massage <Человек>', brief='<Квина, сделай пж>')
    async def massage(self, ctx, person: typing.Union[discord.Member, str], *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime massage')
        emb = await self.build_embed(reaction, ctx.author, 'сделал(а) массаж', words, person, "<Квина, сделай пж>")
        await ctx.send(embed=emb)
    
    @commands.command(usage='shrug', brief='<Квина, сделай пж>')
    async def shrug(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime shrug')
        emb = await self.build_embed(reaction, ctx.author, 'пожимает плечами', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='confused', brief='<Квина, сделай пж>')
    async def confused(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime confused')
        emb = await self.build_embed(reaction, ctx.author, 'смущается', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='stockings', brief='<Квина, сделай пж>')
    async def stockings(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime stockings')
        emb = await self.build_embed(reaction, ctx.author, 'одел(а) чулки', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='striptease', brief='<Квина, сделай пж>')
    async def striptease(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime striptease')
        emb = await self.build_embed(reaction, ctx.author, 'танцует стриптиз', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='anger', brief='<Квина, сделай пж>')
    async def anger(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime anger')
        emb = await self.build_embed(reaction, ctx.author, 'злится', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='rain', brief='<Квина, сделай пж>')
    async def rain(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime rain')
        emb = await self.build_embed(reaction, ctx.author, 'стоит под дождём', words)
        await ctx.send(embed=emb)
    
    @commands.command(usage='cook', brief='<Квина, сделай пж>')
    async def cook(self, ctx, *, words: str = None):
        await ctx.message.delete()
        reaction = await self.get_gif('anime cook')
        emb = await self.build_embed(reaction, ctx.author, 'готовит', words)
        await ctx.send(embed=emb)


async def setup(client):
    await client.add_cog(ReactionsCommand(client))
