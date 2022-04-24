import Cogs.helper as h
import nextcord, json, aeval, time, os
from nextcord.ext import commands

json_data = json.load(open("settings.json", "r"))
bot = commands.Bot(command_prefix="__", case_insensitive=True, owner_ids=json_data["owners"], strip_after_prefix=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    for i in os.listdir("Cogs"):
        if i.startswith("C_") and i.endswith(".py"):
            try:
                bot.load_extension("Cogs." + i[:-3])
                h.create_log(f"Cog Cogs.{i[:3]} loaded")
            except Exception as e:
                h.create_log(f"Cog Cogs.{i[:3]} failed to load by error {e}")
    await bot.register_new_application_commands()
    h.create_log("Ready!")

@bot.slash_command(name="ping", description="Показывает пинг бота")
async def c_ping(ctx: nextcord.Interaction):
	await ctx.send(f"Pong! Latency is {round(bot.latency * 1000)} ms")

@bot.command(aliases=['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    minify_text = lambda txt: f'{txt[:-900]}...\n# ...и ещё {len(txt.replace(txt[:-900], ""))} символов' if len(txt) >= 1024 else txt
    if ctx.author.id not in json_data["owners"]:
        return await ctx.send("Кыш!")
    code = "\n".join(content.split("\n")[1:])[:-3] if content.startswith("```") and content.endswith("```") else content
    standard_args = {
        "nextcord": nextcord,
        "discord": nextcord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx
    }
    start = time.time()  # import time, для расчёта времени выполнения
    try:
        r = await aeval.aeval(f"""{code}""", standard_args, {})  # выполняем код
        ended = time.time() - start  # рассчитываем конец выполнения
        if not code.startswith('#nooutput'):
            # Если код начинается с #nooutput, то вывода не будет
            embed = nextcord.Embed(title="Успешно!", description=f"Выполнено за: {ended}", color=0x99ff99)
            """
            Есть нюанс: если входные/выходные данные будут длиннее 1024 символов, то эмбед не отправится, а функция выдаст ошибку.
            Именно поэтому сверху стоит print(r), а так же есть функция minify_text, которая
            минифицирует текст для эмбеда во избежание БэдРеквеста (слишком много символов).
            """
            embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`')
            embed.add_field(name=f'Выходные данные:', value=f'`{minify_text(str(r))}`', inline=False)
            await ctx.send(embed=embed)
    except Exception as e:
        ended = time.time() - start
        code = minify_text(str(code))
        embed = nextcord.Embed(title=f"При выполнении возникла ошибка.\nВремя: {ended}", description=f'Ошибка:\n```py\n{e}```', color=0xff0000)
        embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`', inline=False)
        await ctx.send(embed=embed)
        raise e

@bot.command()
async def test(ctx: commands.Context, desc: str, *, fiel: str = ""):
    emb = nextcord.Embed(title='Test', description=desc)
    print(fiel)
    if fiel != "":
        for i in fiel.split(" "):
            egg = i.split(':')
            emb.add_field(name=egg[0], value=egg[1], inline=False)
    await ctx.send(embeds=h.EmbedFixer(emb))

if __name__ == "__main__":
    bot.run(json_data["token"])