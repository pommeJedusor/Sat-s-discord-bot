import discord
from discord import app_commands
from discord.ext import commands

import global_functions
from datas.datas import Datas

class Dropdown(discord.ui.Select):
    def __init__(self,bot,*args):
        self.bot = bot
        # Set the options that will be presented inside the dropdown
        options=[]
        print(args[0])
        for arg in args[0][0]:
                options.append(discord.SelectOption(label=arg["name"],value=arg["id"]))

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder="choisissez l'item que vous souhaitez reroll", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        player = global_functions.Player(name=interaction.user.name,id=interaction.user.id)
        player.is_player()
        item = global_functions.Items(name="pomme",id=self.values[0])
        item.is_item(x=6)
        channel_perso=self.bot.get_channel(player.caracter[5])

        player.lose_item(item.caracter[6],1)
        text=""
        for i in player.tirages(1,tirage_4=True):
            text+=f"{i.caracter[0]}: {i.caracter[1]} étoiles \n"
        player.caracter[8].append({"id": Datas.arsmote_id, "active": False})
        player.caracter[8].remove({"id": Datas.arsmote_id, "active": True})
        await interaction.response.send_message(text)
        await interaction.channel.send(i.caracter[3])
        if not interaction.channel_id == player.caracter[5]:
            await channel_perso.send(text)
            await channel_perso.send(i.caracter[3])
        player.update_stats_player_fichier()


class DropdownView(discord.ui.View):
    def __init__(self,bot,*args):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(bot,args))


class Arsmote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @app_commands.command(name="arsmote",description="commande que je teste")
    async def arsmote(self, interaction: discord.Interaction):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        items = []
        if {"id":Datas.arsmote_id,"active":True} in player.caracter[8]:
            for item in player.caracter[9]:
                if not item in items:
                    items.append(item)
            true_items = []
            for item in items:
                item = global_functions.Items("nimp",id=item)
                item.is_item(x=6)
                if item.caracter[1] == 4:
                    true_items.append({"name":item.caracter[0],"id":item.caracter[6]})
            if true_items:
                view = DropdownView(self.bot,true_items)
                await interaction.response.send_message("arsmote",view=view,ephemeral=True)
            else:
                await interaction.response.send_message(f"vous n'avez pas eu de 4 étoiles lors de votre dernier tirage",ephemeral=True)
        else:
            await interaction.response.send_message(f"vous n'avez pas le pouvoir d'actif",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Arsmote(bot))