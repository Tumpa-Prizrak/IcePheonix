# TODO CherryFox, Вы сделали что-то великое! В награду, я даю тебе эту клубнику!
import time

import aeval
import aiohttp
import discord

import helper as h


bot = h.MyBot(debug=True, help_cog_file="other.py")


def minify_text(text):
    if len(text) > 1024:
        return f"{text[:950]}...\n# ...и ещё {len(text.replace(text[:950]))} символов"
    return text


'''
@bot.command()
async def t(ctx, guild: int):
    help = await bot.get_guild(guild).invites()
    await ctx.send(help)
'''


@bot.command(aliases=['eval', 'aeval', 'evaluate', 'выполнить', 'exec', 'execute', 'code'])
async def __eval(ctx, *, content):
    await ctx.message.delete()
    if ctx.author.id not in h.json_data['owners']:
        return await ctx.send("Кыш!")
    code = "\n".join(content.split("\n")[1:])[:-3] if content.startswith("```") and content.endswith("```") else content
    standard_args = {
        "discord": discord,
        "bot": bot,
        "ctx": ctx
    }
    start = time.time()  # import time, для расчёта времени выполнения
    try:
        r = await aeval.aeval(f"""{code}""", standard_args, {})  # выполняем код
        ended = time.time() - start  # рассчитываем конец выполнения
        if not code.startswith('#nooutput'):
            # Если код начинается с #nooutput, то вывода не будет
            embed = discord.Embed(title="Успешно!", description=f"Выполнено за: {ended}", color=0x99ff99)
            embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`')
            embed.add_field(name=f'Выходные данные:', value=f'`{minify_text(str(r))}`', inline=False)
            await ctx.send(embed=embed)
    except Exception as e:
        ended = time.time() - start
        code = minify_text(str(code))
        embed = discord.Embed(title=f"При выполнении возникла ошибка.\nВремя: {ended}",
                              description=f'Ошибка:\n```py\n{e}```', color=0xff0000)
        embed.add_field(name=f'Входные данные:', value=f'`{minify_text(str(code))}`', inline=False)
        await ctx.send(embed=embed)
        raise e


try:
    bot.run(h.json_data['token'])
except aiohttp.ClientConnectionError:
    h.Log.error("Возможно вы не в сети, проверьте ваше интернет соеденение и попробуйте ещё раз")
