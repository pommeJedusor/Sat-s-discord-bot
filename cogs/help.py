import discord
from discord import app_commands
from discord.ext import commands

from datas.datas import Datas

import asyncio


class SuggestModal(discord.ui.Modal, title="suggestion"):
    global channel_bot
    suggestion = discord.ui.TextInput(label="suggestion",style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"suggestion envoyé",ephemeral=True)
        await channel_bot.send(f"{interaction.user.name}: {self.suggestion}")

class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="suggestion")
    async def suggest_button(self,interaction:discord.Interaction, Button:discord.ui.Button):
        await interaction.response.send_modal(SuggestModal())



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="si besoin d'aide")
    async def help(self, interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        view=Buttons()
        view.add_item(discord.ui.Button(label="voir les commandes",style=discord.ButtonStyle.link, url="https://github.com/pommeJedusor/Sat-s-discord-bot/blob/main/README.md"))
        await interaction.edit_original_response(view=view)

async def setup(bot):
    global channel_bot
    channel_bot = bot.get_channel(1065764381310328872)
    await bot.add_cog(Help(bot))