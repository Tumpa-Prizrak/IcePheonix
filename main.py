import Cogs.helper as h
import nextcord, json, aeval, time, os
from nextcord.ext import commands

json_data = json.load(open("settings.json", "r"))
bot = commands.Bot(command_prefix="__", case_insensitive=True, owner_ids=json_data["owners"], strip_after_prefix=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    """for i in os.listdir("Cogs"):
        if i.startswith("C_") and i.endswith(".py"):
            try:
                bot.load_extension("Cogs." + i[:-3])
                h.create_log(f"Cog {i[2:-3]} loaded", "cogs")
            except Exception as e:
                h.create_log(f"Cog {i[2:-3]} failed to load due to error {e}", "error")"""
    
    await bot.register_new_application_commands()
    await bot.register_application_commands(c_ping, c_add_voice, c_remove_voice)

    for i in bot.guilds:
        await i.rollout_application_commands()
    h.create_log("Bot is ready!", "ready")

@bot.slash_command(name="ping", description="Показывает пинг бота")
async def c_ping(ctx: nextcord.Interaction):
	await ctx.send(f"Pong! Latency is {round(bot.latency * 1000)} ms")

### Temp voices ###################################################################################################################################

@nextcord.slash_command(name="set_voice")
async def c_add_voice(interaction: nextcord.Interaction, channel_id: str = nextcord.SlashOption(name="id", description="Enter the channel name wich will be used to create a new voice сhannel")):
    channel_id = int(channel_id)
    g = bot.get_channel(channel_id)
    if g == None or type(g) != nextcord.VoiceChannel:
        return await interaction.send("Incorrect channel id")
    h.do_to_database("INSERT INTO voiceCreators VALUES (?, ?)", channel_id, interaction.guild.id)
    await interaction.send(":thumbsup:")
    
@nextcord.slash_command(name="unset_voice")
async def c_remove_voice(interaction: nextcord.Interaction, channel_id: str = nextcord.SlashOption(name="id", description="Enter the channel name wich will be used to create a new voice сhannel")):
    channel_id = int(channel_id)
    g = bot.get_channel(channel_id)
    if g == None or type(g) != nextcord.VoiceChannel:
        return await interaction.send("Incorrect channel id")
    h.do_to_database("DELETE FROM VoiceChannel WHERE voice=? and server=?", channel_id, interaction.guild.id)
    await interaction.send(":thumbsup:")

@bot.event
async def on_voice_state_update(member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
    try:
        if before.channel.id == after.channel.id:
            return
    except AttributeError:
        pass

    try:
        after.channel.id
        h.create_log([after.channel.id, after.channel.guild.id], "DEBUG")
        h.create_log(h.do_to_database("SELECT * FROM voiceCreators"), "DEBUG")

        if [after.channel.id, after.channel.guild.id] in h.do_to_database("SELECT * FROM voiceCreators"):
            egg = await after.channel.category.create_voice_channel(f"{member.display_name} voice")
            await member.move_to(egg)
            h.do_to_database("INSERT INTO createdVoices VALUES (?, ?, ?)", egg.id, egg.guild.id, member.id)
    except AttributeError:
        if [before.channel.id, member.guild.id] in h.do_to_database("SELECT id, guild FROM createdVoices") and len(before.channel.members) == 0:
            await before.channel.delete()
        h.create_log(before.channel.members, "DEBUG")
        h.create_log(h.do_to_database("SELECT id, guild FROM createdVoices"), "DEBUG")

@bot.slash_command(name="limit")
async def c_limit(interaction: nextcord.Interaction):
    pass

########################################################################################################################################

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

@bot.command()
async def test(ctx: commands.Context, desc: str):
    for i in range(0, len(desc)):
        emb = nextcord.Embed(title="Test", description=desc[i])
        
        await ctx.send(embed=h.fix_long_embed(emb))

if __name__ == "__main__":
    bot.run(json_data["token"])