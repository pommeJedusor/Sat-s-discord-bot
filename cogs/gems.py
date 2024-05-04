import discord
from discord import app_commands
from discord.ext import commands

import json

from model import global_functions
from model import ModelPlayer

from datas.datas import Datas

class Gems(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #modo
    @app_commands.command(name="add_gems",description="permet à un modo d'ajouter à un joueur un nombre de gemmes choisis par l'éxécutant de la commande")
    async def add_gems(self,interaction: discord.Interaction, nombre_de_gemmes: int, user: discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user) and nombre_de_gemmes>0:
            player = ModelPlayer.Player(user.name,user.id)
            player.is_player()
            player.nb_gemmes+=nombre_de_gemmes
            player.update_stats_player_fichier()
            await interaction.edit_original_response(content=f"les {nombre_de_gemmes} gemme(s) ont bien été ajoués à {user.name} ")
        elif nombre_de_gemmes==0:
            await interaction.edit_original_response(content="euh.... ???? vous êtes sûr??? bon ... bah ... c'est fait.. je suppose???")
        elif nombre_de_gemmes<0:
            await interaction.edit_original_response(content="les nombres nuls ou négatifs ne sont pas accepter veuillez utiliser la commande '/destroy_gems' ou son homologue '\spend_gems'")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon rôle")

    @app_commands.command(name="see_gems_of_a_player",description="permet à un modo de voir les gemmes d'un joueur")
    async def see_gems_of_a_player(self,interaction : discord.Interaction, user : discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player = ModelPlayer.Player(user.name,user.id)
            player.is_player()
            await interaction.edit_original_response(content=f"{Datas.emogi_cristal} **{user.name}** possède **{player.nb_gemmes} Cristaux d'Expédition ** ! {Datas.emogi_cristal}\n{Datas.emogi_cristal} a dépensé au total **{player.gemmes_spend} Cristaux d'Expédition **! {Datas.emogi_cristal}")
        else:
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle")

    @app_commands.command(name="spend_gems",description="permet de dépenser les gemmes d'un joueur")
    @app_commands.describe(depenser="True pour enlever les gemmes et augmenter 'les gemmes dépenser', False pour juste les enlever")
    async def spend_gems(self,interaction:discord.Interaction,user:discord.Member,nombres_de_gemmes:int,depenser:bool=False):
        await interaction.response.defer()
        player=ModelPlayer.Player(user.name,user.id)
        player.is_player()
        if global_functions.bon_role(interaction.user) and player.nb_gemmes>=nombres_de_gemmes>0:
            player.nb_gemmes-=nombres_de_gemmes
            if depenser:
                player.gemmes_spend+=nombres_de_gemmes
            player.update_stats_player_fichier()
            await interaction.edit_original_response(content=f"les {nombres_de_gemmes} gemmes de {user.name} ont bien été dépensé qui a maintenant {player.nb_gemmes} gemmes ")
        elif not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content="vous n'avez pas le bon role")
        elif not nombres_de_gemmes>0:
            await interaction.edit_original_response(content="ous ne pouvez pas retirer un nombre nul ou négatif de gemmes user de la commande '/add_gems' pour cette effet")
        else:
            await interaction.edit_original_response(content=f"vous ne pouvez pas retirer {nombres_de_gemmes} gemmes à un joueur qui en a moins ({player.nb_gemmes}) ")

    @app_commands.choices(tri=[
    app_commands.Choice(name="gems", value="gems"),
    app_commands.Choice(name="name", value="name"),
    ])
    @app_commands.command(name="see_all_gems",description="permet de voir les gemmes possédés et dépensé de tout les joueurs")
    async def see_all_gems(self,interaction : discord.Interaction, tri :app_commands.Choice[str]=None):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content="voici la liste des joueurs et leurs nombres de gemmes")
            texts=[]
            with open (Datas.player_file,"r") as f:
                for line in f:
                    line = json.loads(line)
                    texts.append([line[0],line[2],f"{line[0]}: {line[2]} possédées {line[3]} dépensé"])

            tri_lambda_gems = lambda x: x[1]
            tri_lambda_name = lambda x: x[0].lower()
            texts.sort(key=tri_lambda_name)
            if not tri==None and tri.value=="gems":
                texts.sort(key=tri_lambda_gems)
                
            print(texts)

            for i in range(len(texts)//10+1):
                text = ""
                first=True
                for line in texts[i*10:(i+1)*10]:
                    if first:
                        text+=line[2]
                        first=False
                    else:
                        text+="\n"+line[2]
                await interaction.channel.send(text)
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon rôle\nutiliser plutôt see_gems pour voir vos gemmes")

    #players
    @app_commands.command(name="see_gems",description="permet de voir son nombre de gemmes possédés et dépensé ")
    async def see_gems(self,interaction : discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        player = ModelPlayer.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        await interaction.edit_original_response(content=f"{Datas.emogi_cristal} Vous possédez **{player.nb_gemmes} Cristaux d'Expédition** ! {Datas.emogi_cristal}\n{Datas.emogi_cristal} Vous avez dépensez au total **{player.gemmes_spend} Cristaux d'Expédition** ! {Datas.emogi_cristal}")
                


async def setup(bot):
    await bot.add_cog(Gems(bot))