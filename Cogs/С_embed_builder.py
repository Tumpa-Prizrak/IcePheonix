import nextcord
from nextcord.ext import commands
import Cogs.helper as h
from asyncio import run

class embed_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @nextcord.slash_command(name="send_embed")
    async def send_embed(ctx: commands.Context,
                        title: str = nextcord.SlashOption(name="Title", description="Sets the embed's title.", required=True),
                        desc: str = nextcord.SlashOption(name="Description", description="Sets the embed's description", required=True)):
        descriptions = h.fix_long_embed(desc)
        for i in range(0, len(descriptions)):
            emb = nextcord.Embed(
                title=title, description=descriptions[i], colour=0xD8BFD8)
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(embed_cog(bot))