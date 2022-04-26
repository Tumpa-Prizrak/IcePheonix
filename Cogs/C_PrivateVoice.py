from discord import VoiceChannel
import nextcord
from nextcord.ext import commands
import Cogs.helper as h

class NewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @nextcord.slash_command(name="add_Voice")
    async def add_voice(self, interaction: nextcord.Interaction, channel_id: int = nextcord.SlashOption(name="Channel_id", description="Enter the channel name wich will be used to create a new voice сhannel")):
        g = self.bot.get_channel(channel_id)
        if g == None or type(g) != VoiceChannel:
            return await interaction.send("Incorrect channel id")
        h.do_to_database("INSERT INTO voiceCreators VALUES (?, ?)", channel_id, interaction.id)
        await interaction.send(":thumbsup:")
    
    @nextcord.slash_command(name="remove_Voice")
    async def remove_voice(self, interaction: nextcord.Interaction, channel_id: int = nextcord.SlashOption(name="Channel_id", description="Enter the channel name wich will be used to create a new voice сhannel")):
        g = self.bot.get_channel(channel_id)
        if g == None or type(g) != VoiceChannel:
            return await interaction.send("Incorrect channel id")
        h.do_to_database("DELETE FROM VoiceChannel WHERE voice=? and server=?", channel_id, interaction.id)
        await interaction.send(":thumbsup:")

def setup(bot):
    bot.add_cog(NewCog(bot))