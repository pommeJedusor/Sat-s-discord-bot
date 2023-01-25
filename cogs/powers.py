import discord
from discord import app_commands
from discord.ext import commands

import json

import global_functions
from datas.datas import Datas

class Powers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reset_power",description="permet de réactivé les effets des persos panda et arsmote")
    async def reset_power(self,interaction: discord.Interaction):
        if global_functions.bon_role(interaction.user):
            text=""
            with open(Datas.player_file,"r") as f:
                for ligne in f:
                    ligne=json.loads(ligne)
                    for power in ligne[8]:
                        power['active']=True
                    text+=json.dumps(ligne)+"\n"
            with open(Datas.player_file,"w") as f:
                f.write(text)
            await interaction.response.send_message("l'opération a réussis ")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")
    
    @app_commands.command(name="yato",description=r"20% de chances d'obtenir 2 cristaux durant 10 tirages l'reste=items")
    async def yato(self,interaction: discord.Interaction):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        if {"id":Datas.Yato_id,"active":True} in player.caracter[8] and not player.caracter[10]>0:
            player.caracter[10]=10
            for power in player.caracter[8]:
                    if power['id']==Datas.Yato_id:
                        power['active']=False
            await interaction.response.send_message("activé")
        elif  player.caracter[10]>0:
            await interaction.response.send_message(f"il vous reste {player.caracter[10]} tirages où le pouvoir peut prendre effets")
        else:
            await interaction.response.send_message("pouvoir désactivé")
        player.update_stats_player_fichier()
    
    @app_commands.command(name="panda",description=r"utilise la capacité de panda et réduit de 10% la pity a avoir")
    async def panda(self,interaction: discord.Interaction):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        if {"id":Datas.panda_id,"active":True} in player.caracter[8]:
            player.caracter[6][2]=9
            player.caracter[6][3]=45
            for power in player.caracter[8]:
                if power['id']==Datas.panda_id:
                    power['active']=False
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"votre pouvoir a bien été utilisé votre pity est désormais de : \n {player.caracter[6][0]}/{player.caracter[6][2]} pour les 4 étoiles \n {player.caracter[6][1]}/{player.caracter[6][3]} pour les 5 étoiles")
        elif {"id":Datas.panda_id,"active":False} in player.caracter[8]:
            await interaction.response.send_message("votre pouvoir est désactivé")
        else:
            await interaction.response.send_message("vous n'avez pas l'item requis pour effectuer cette commande")


async def setup(bot):
    await bot.add_cog(Powers(bot))