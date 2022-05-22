import discord
from discord.ext import commands
import Cogs.helper as h
from asyncio import run

class embed_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @discord.slash_command(name="send_embed")
    async def send_embed(self, ctx: commands.Context,
                        title: str = discord.SelectOption(name="Title", description="Sets the embed's title.", required=True),
                        desc: str = discord.SelectOption(name="Description", description="Sets the embed's description", required=True)):
        descriptions = h.fix_long_embed(desc)
        for i in range(len(descriptions)):
            emb = discord.Embed(
                title=title, description=descriptions[i], colour=0xD8BFD8)
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(embed_cog(bot))