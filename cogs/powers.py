import discord
from discord import app_commands
from discord.ext import commands

import json

import global_functions
from datas.datas import Datas

class Powers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #modo
    @app_commands.command(name="reset_power",description="permet de réactivé les effets des persos panda et arsmote")
    async def reset_power(self,interaction: discord.Interaction):
        await interaction.response.defer()
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
            await interaction.edit_original_response(content=":white_check_mark: **Le pouvoir a bien été réinitialisé.** :white_check_mark:")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon role")
    
    #players
    @app_commands.command(name="yato",description=r"20% de chances d'obtenir 2 cristaux durant 10 tirages l'reste=items")
    async def yato(self,interaction: discord.Interaction):
        await interaction.response.defer()
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        if {"id":Datas.Yato_id,"active":True} in player.caracter[8] and not player.caracter[10]>0:
            player.caracter[10]=10
            for power in player.caracter[8]:
                    if power['id']==Datas.Yato_id:
                        power['active']=False
            await interaction.edit_original_response(content="activé")
        elif  player.caracter[10]>0:
            await interaction.edit_original_response(content=f"il vous reste {player.caracter[10]} tirages où le pouvoir peut prendre effets")
        elif {"id":Datas.Yato_id,"active":False} in player.caracter[8]:
            await interaction.edit_original_response(content=f"votre pouvoir est désactivé")
        else:
            await interaction.edit_original_response(content=":x: **Vous n'avez pas l'objet requis pour effectuer cette commande.** :x:")
        player.update_stats_player_fichier()
    
    @app_commands.command(name="panda",description=r"utilise la capacité de panda et réduit de 10% la pity a avoir")
    async def panda(self,interaction: discord.Interaction):
        await interaction.response.defer()
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        if {"id":Datas.panda_id,"active":True} in player.caracter[8]:
            #nombre de pandas possédé par le player
            for item in player.caracter[4]:
                if item["id"]==Datas.panda_id:
                    item_numbers = item["nb"]

            if item_numbers==1:
                player.caracter[6][2]=9
                player.caracter[6][3]=45
                player.caracter[6][5]=72
            elif item_numbers==2:
                player.caracter[6][2]=9
                player.caracter[6][3]=43
                player.caracter[6][5]=68
            elif item_numbers>=3:
                player.caracter[6][2]=8
                player.caracter[6][3]=40
                player.caracter[6][5]=64

            for power in player.caracter[8]:
                if power['id']==Datas.panda_id:
                    power['active']=False
            player.update_stats_player_fichier()
            await interaction.edit_original_response(content=f"votre pouvoir a bien été utilisé votre pity est désormais de : \n {player.caracter[6][0]}/{player.caracter[6][2]} pour les 4 étoiles \n {player.caracter[6][1]}/{player.caracter[6][3]} pour les 5 étoiles\n {player.caracter[6][4]}/{player.caracter[6][5]} pour les 6 étoiles")
        elif {"id":Datas.panda_id,"active":False} in player.caracter[8]:
            await interaction.edit_original_response(content="votre pouvoir est désactivé")
        else:
            await interaction.edit_original_response(content=":x: **Vous n'avez pas l'objet requis pour effectuer cette commande.** :x:")


async def setup(bot):
    await bot.add_cog(Powers(bot))