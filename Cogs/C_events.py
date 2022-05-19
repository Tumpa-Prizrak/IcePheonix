### Hello and Goodbye ###

import discord
from discord.ext import commands
import Cogs.helper as h

class embed_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if (member.guild.id,) in h.do_to_database("SELECT guild FROM channels"):
            h.do_to_database("SELECT hello_channel FROM channels WHERE guild=?")[0].send(f"{member.mention} joined!\nNow there're {len(member.guild.members)} members!")
        
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if (member.guild.id,) in h.do_to_database("SELECT guild FROM channels"):
            h.do_to_database("SELECT hello_channel FROM channels WHERE guild=?")[0].send(f"{member.mention} leaved!\nNow there're {len(member.guild.members)} members!")

def setup(bot):
    bot.add_cog(embed_cog(bot))