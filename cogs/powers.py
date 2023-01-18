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
            print("activé")
        elif  not {"id":Datas.Yato_id,"active":True} in player.caracter[8]:
            print("pouvoir désactivé")
        else:
            print("le pouvoir est encore actif")
        player.update_stats_player_fichier()

    @app_commands.command(name="arsmote",description="permet de reroll un 4 étoile obtnu lors du dernier tirage pour en obtenir un autre")
    async def arsmote(self,interaction: discord.Interaction,nom_du_4_étoiles:str):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        item=global_functions.Items(nom_du_4_étoiles)
        channel_perso=self.bot.get_channel(player.caracter[5])
        if {"id":Datas.arsmote_id,"active":True} in player.caracter[8] and item.is_item() and item.caracter[6] in player.caracter[9] and item.caracter[1]==4:
            if player.lose_item(item.caracter[6],1):
                text=""
                for i in player.tirages(1,tirage_4=True):
                    text+=f"{i.caracter[0]}: {i.caracter[1]} étoiles \n"
                for power in player.caracter[8]:
                    if power['id']==Datas.arsmote_id:
                        power['active']=False
                await interaction.response.send_message(text)
                await channel_perso.send(text)
                await interaction.channel.send(i.caracter[3])
                await channel_perso.send(i.caracter[3])
                player.update_stats_player_fichier()
            else:
                await interaction.response.send_message(f"l'item {item.caracter[0]} n'as pas réussis à être supprimé")
        elif {"id":Datas.arsmote_id,"active":False} in player.caracter[8]:
            await interaction.response.send_message("votre pouvoir est désactivé")
        elif not {"id":Datas.arsmote_id,"active":True} in player.caracter[8]:
            await interaction.response.send_message("vous n'avez pas l'item requis pour effectuer cette commande")
        elif not item.is_item():
            await interaction.response.send_message(f"l'item {nom_du_4_étoiles} n'as pas été trouvé")
        elif not item.caracter[6] in player.caracter[9]:
            await interaction.response.send_message(f"vous n'avez pas obtenu l'item {item.caracter[0]} lors de votre dernier tirage")
        else:
            await interaction.response.send_message(f"l'item {item.caracter[0]} n'est pas 4 étoiles mais {item.caracter[1]} étoiles ")

    
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