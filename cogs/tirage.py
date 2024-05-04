import discord
from discord import app_commands
from discord.ext import commands

import asyncio

from model import global_functions
from model import ModelPlayer

from datas.datas import Datas

tirage_en_cours = False

class Tirage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #modo
    @app_commands.command(name="change_channel",description="permet de changer ou d'initialiser le channel d'un joueur")
    async def change_channel(self,interaction:discord.Interaction,user:discord.Member):
        await interaction.response.defer()
        player = ModelPlayer.Player(user.name,user.id)
        player.is_player()
        if global_functions.bon_role(interaction.user):
            player.salon=interaction.channel_id
            player.update_stats_player_fichier()
            await interaction.edit_original_response(content=f"{Datas.emogi_cristal}** Le Salon perso de __{user}__ est désormais __{interaction.channel.name}__. ** {Datas.emogi_cristal}")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon role")

    @app_commands.command(name="see_pity_of_a_player",description="permet de voir la pity d'un joueur")
    async def see_pity_of_a_player(self,interaction:discord.Interaction,user:discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player=ModelPlayer.Player(user.name,user.id)
            player.is_player()
            await interaction.edit_original_response(content=f"pour l'obtention d'une 4 étoiles: {player.pity[0]}/{player.pity[2]} \n pour l'obtention d'une 5 étoiles: {player.pity[1]}/{player.pity[3]}\n pour l'obtention d'une 6 étoiles: {player.pity[4]}/{player.pity[5]}")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon role")

    @app_commands.command(name="edit_pity_of_a_player",description="permet de modifier la pity d'un joueur")
    async def edit_pity_of_a_player(self,interaction:discord.Interaction,user:discord.Member,dénominateur_4:int=False,dénominateur_5:int=False,numérateur_4:int=False,numérateur_5:int=False,dénominateur_6:int=False,numérateur_6:int=False):
        if global_functions.bon_role(interaction.user):
            await interaction.response.defer()
            player = ModelPlayer.Player(user.name,user.id)
            player.is_player()
            if not numérateur_5:
                numérateur_5=player.pity[1]
            if not numérateur_4:
                numérateur_4=player.pity[0]
            if not dénominateur_4:
                dénominateur_4=player.pity[2]
            if not dénominateur_5:
                dénominateur_5=player.pity[3]
            if not numérateur_6:
                numérateur_6=player.pity[4]
            if not dénominateur_6:
                dénominateur_6=player.pity[5]
            player.pity = [numérateur_4,numérateur_5,dénominateur_4,dénominateur_5,numérateur_6,dénominateur_6]
            player.update_stats_player_fichier()
            await interaction.edit_original_response(content=f"le joueur {user.name} a désormais comme pity: \npour 4 étoiles: {player.pity[0]}/{player .pity[2]} \npour 5 étoiles {player.pity[1]}/{player .pity[3]} \net pour 6 étoiles: {player.pity[4]}/{player .pity[5]} ")
        else:
             await interaction.edit_original_response(content="vous n'avez pas le bon role")   

    #players
    @app_commands.command(name="tirage",description="permet de faire des tirages")
    async def tirages(self,interaction:discord.Interaction,nombre_de_tirage:int):
        global tirage_en_cours
        await interaction.response.defer()
        player = ModelPlayer.Player(interaction.user.id,interaction.user.id)
        player.is_player()
        channel_perso=self.bot.get_channel(player.salon)
        if player.nb_gemmes>=nombre_de_tirage and nombre_de_tirage<=10 and interaction.channel_id==Datas.channel_tirage_gacha and not tirage_en_cours:
            tirage_en_cours = True
            await interaction.edit_original_response(content=f"vous avez obtenus...")

            #yato
            """if player.yato_tirages>0:
                if nombre_de_tirage>player.yato_tirages:
                    nombre_de_tentative_gemmes=player.yato_tirages
                else:
                    nombre_de_tentative_gemmes=nombre_de_tirage
                compteur_de_gemmes=0
                for i in range(nombre_de_tentative_gemmes):
                    if random.randint(1,5)==4:
                        compteur_de_gemmes+=1
                        nombre_de_tirage-=1
                        player.nb_gemmes+=1
                        player.gemmes_spend+=1
                    player.yato_tirages-=1
                player.update_stats_player_fichier()
                for i in range(compteur_de_gemmes):
                    await channel_perso.send("vous avez gagné 2 gemmes")
                    if not interaction.channel==channel_perso:
                        await interaction.channel.send("vous avez gagné 2 gemmes")
                    await asyncio.sleep(2)
            player.update_stats_player_fichier()"""

            
            for i in player.tirages(nombre_de_tirage):
                if not type(i)==str:  
                    i.is_item()
                    await asyncio.sleep(i.stars)
                    if player.salon!=1040228357981343764:
                        await channel_perso.send(f"{i.name} : {i.stars} étoiles :")
                    if not interaction.channel==channel_perso:
                        await interaction.channel.send(f"{i.name} : {i.stars} étoiles :")
                    if i.url_img:
                        if player.salon!=1040228357981343764:
                            await channel_perso.send(f"{i.url_img}")
                        if not interaction.channel==channel_perso:
                            await interaction.channel.send(f"{i.url_img}")
                else:
                    await asyncio.sleep(5)
                    await interaction.channel.send("vous avez gagné 2 cristaux d'expedition")
            tirage_en_cours = False
        elif not interaction.channel_id==Datas.channel_tirage_gacha:
            await interaction.edit_original_response(content=f"vous êtes dans le mauvais channel aller dans tirage gacha pour effectuer cette commande")
        elif nombre_de_tirage>10:
            await interaction.edit_original_response(content="vous ne pouvez éffectuer qu'un maximum de 10 tirages à la fois")
        elif tirage_en_cours:
            await interaction.edit_original_response(content=f"un tirage est déja en cours veuillez patienter et retenter plus tard")
        else:
            await interaction.edit_original_response(content=f"il vous manque {nombre_de_tirage-player.nb_gemmes} gemmes")

    @app_commands.command(name="see_pity",description="permet de voir sa pity")
    async def voir_sa_pity(self,interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        player=ModelPlayer.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        await interaction.edit_original_response(content=f"**Votre pity :star::star::star::star: : {player.pity[0]}/{player.pity[2]} **\n**Votre pity :star::star::star::star::star: : {player.pity[1]}/{player.pity[3]} **\n**Votre pity :star::star::star::star::star::star: : {player.pity[4]}/{player.pity[5]} **")

async def setup(bot):
    await bot.add_cog(Tirage(bot))