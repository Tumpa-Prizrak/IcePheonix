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
                h.create_log(f"Cog {i[2:-3]} loaded", "cogs")
            except Exception as e:
                h.create_log(f"Cog {i[2:-3]} failed to load due to error {e}", "error")
    
    await bot.register_application_commands(c_ping, test)
    h.create_log("Bot is ready!", "ready")

@bot.command()
async def reload_extension(ctx: nextcord.Interaction, extension: str):
    try:
        bot.reload_extension("Cogs.C_" + extension)
        await ctx.send(f"Cog {extension} was reloaded succesfully.")
        h.create_log(f"Cog {extension} was reloaded by {bot.get_user()}", "cogs")
    except Exception as e:
        await ctx.send(f"Unable to reload {extension} due to error: {e}")
        h.create_log(f"Unable to reload {extension} due to error: {e}", "error")

@bot.slash_command(name="ping", description="Показывает пинг бота")
async def c_ping(ctx: nextcord.Interaction):
	await ctx.send(f"Pong! Latency is {round(bot.latency * 1000)} ms")

@bot.command(aliases=['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    minify_text = lambda txt: f'{txt[:-900]}...\n# ...и ещё {len(txt[900:], "")} символов' if len(txt) >= 1024 else txt
    
    if ctx.author.id not in json_data["owners"]:
        try:
            return await ctx.send(f"Кыш!, {bot.get_user(ctx.author.id).mention}")
        except Exception:
            return await ctx.send("Кыш!")
    code = "\n".join(content.split("\n")[1:])[:-3] if content.startswith("```") and content.endswith("```") else content
    standard_args = {
        "nextcord": nextcord,
        "discord": nextcord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx
    }
    
    start = time.perf_counter()  # import time, для расчёта времени выполнения
    try:
        r = await aeval.aeval(f"""{code}""", standard_args, {})  # выполняем код
        end = time.perf_counter() - start  # рассчитываем конец выполнения
        if not code.startswith('#nooutput'):
            # Если код начинается с #nooutput, то вывода не будет
            embed = nextcord.Embed(title="Успешно!", description=f"Выполнено за: {round(end * 1000, 5)} мс", color=0x99ff99)
            """
            Есть нюанс: если входные/выходные данные будут длиннее 1024 символов, то эмбед не отправится, а функция выдаст ошибку.
            Именно поэтому сверху стоит print(r), а так же есть функция minify_text, которая
            минифицирует текст для эмбеда во избежание БэдРеквеста (слишком много символов).
            """
            embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`')
            embed.add_field(name=f'Выходные данные:', value=f'`{minify_text(str(r))}`', inline=False)
            await ctx.send(embed=embed)
            
            h.create_log(f"{ctx.author} used eval command with input: {code}.")
    except Exception as e:
        end = time.perf_counter() - start
        code = minify_text(str(code))
        embed = nextcord.Embed(title=f"При выполнении возникла ошибка.\nВремя: {round(end * 1000, 5)} мс", description=f'Ошибка:\n```py\n{e}```', color=0xff0000)
        embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`', inline=False)
        await ctx.send(embed=embed)
        raise e

@bot.slash_command()
async def test(ctx: commands.Context, desc: str = nextcord.SlashOption(name="description", description="Enter embed description"), *, field: str = nextcord.SlashOption(name="field", description="Enter embed field")):
    descriptions = h.fix_long_embed(desc)
    for i in range(0, len(descriptions)):
        emb = nextcord.Embed(title="Test", description=descriptions[i])
        
        if field != "":
            for _ in field.split(" "):
                egg = _.split(':')
                emb.add_field(name=egg[0], value=egg[1], inline=False)
        
        await ctx.send(embed=emb)

if __name__ == "__main__":
    bot.run(json_data["token"])