import discord
from discord import app_commands
from discord.ext import commands

import global_functions
from datas.datas import Datas

import random, asyncio

tirage_en_cours = False

class Tirage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="tirage",description="permet de faire des tirages")
    async def tirages(self,interaction:discord.Interaction,nombre_de_tirage:int):
        global tirage_en_cours
        player = global_functions.Player(interaction.user.id,interaction.user.id)
        player.is_player()
        channel_perso=self.bot.get_channel(player.caracter[5])
        if player.caracter[2]>=nombre_de_tirage and nombre_de_tirage<=10 and interaction.channel_id==Datas.channel_tirage_gacha and not tirage_en_cours:
            tirage_en_cours = True
            await interaction.response.send_message(f"vous avez obtenus...")

            #yato
            """if player.caracter[10]>0:
                if nombre_de_tirage>player.caracter[10]:
                    nombre_de_tentative_gemmes=player.caracter[10]
                else:
                    nombre_de_tentative_gemmes=nombre_de_tirage
                compteur_de_gemmes=0
                for i in range(nombre_de_tentative_gemmes):
                    if random.randint(1,5)==4:
                        compteur_de_gemmes+=1
                        nombre_de_tirage-=1
                        player.caracter[2]+=1
                        player.caracter[3]+=1
                    player.caracter[10]-=1
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
                    await asyncio.sleep(i.caracter[1])
                    if player.caracter[5]!=1040228357981343764:
                        await channel_perso.send(f"{i.caracter[0]} : {i.caracter[1]} étoiles :")
                    if not interaction.channel==channel_perso:
                        await interaction.channel.send(f"{i.caracter[0]} : {i.caracter[1]} étoiles :")
                    if i.caracter[3]:
                        if player.caracter[5]!=1040228357981343764:
                            await channel_perso.send(f"{i.caracter[3]}")
                        if not interaction.channel==channel_perso:
                            await interaction.channel.send(f"{i.caracter[3]}")
                else:
                    await asyncio.sleep(5)
                    await interaction.channel.send("vous avez gagné 2 cristaux d'expedition")
            tirage_en_cours = False
        elif not interaction.channel_id==Datas.channel_tirage_gacha:
            await interaction.response.send_message(f"vous êtes dans le mauvais channel aller dans tirage gacha pour effectuer cette commande",ephemeral=True)
        elif nombre_de_tirage>10:
            await interaction.response.send_message("vous ne pouvez éffectuer qu'un maximum de 10 tirages à la fois",ephemeral=True)
        elif tirage_en_cours:
            await interaction.response.send_message(f"un tirage est déja en cours veuillez patienter et retenter plus tard",ephemeral=True)
        else:
            await interaction.response.send_message(f"il vous manque {nombre_de_tirage-player.caracter[2]} gemmes",ephemeral=True)

    @app_commands.command(name="change_channel",description="permet de changer ou d'initialiser le channel d'un joueur")
    async def change_channel(self,interaction:discord.Interaction,user:discord.Member):
        player = global_functions.Player(user.name,user.id)
        player.is_player()
        if global_functions.bon_role(interaction.user):
            player.caracter[5]=interaction.channel_id
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"{Datas.emogi_cristal}** Le Salon perso de __{user}__ est désormais __{interaction.channel.name}__. ** {Datas.emogi_cristal}")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")

    @app_commands.command(name="see_pity",description="permet de voir sa pity")
    async def voir_sa_pity(self,interaction:discord.Interaction):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        await interaction.response.send_message(f"**Votre pity :star::star::star::star: : {player.caracter[6][0]}/{player.caracter[6][2]} **\n**Votre pity :star::star::star::star::star: : {player.caracter[6][1]}/{player.caracter[6][3]} **\n**Votre pity :star::star::star::star::star::star: : {player.caracter[6][4]}/{player.caracter[6][5]} **",ephemeral=True)

    @app_commands.command(name="see_pity_of_a_player",description="permet de voir la pity d'un joueur")
    async def see_pity_of_a_player(self,interaction:discord.Interaction,user:discord.Member):
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            await interaction.response.send_message(f"pour l'obtention d'une 4 étoiles: {player.caracter[6][0]}/{player.caracter[6][2]} \n pour l'obtention d'une 5 étoiles: {player.caracter[6][1]}/{player.caracter[6][3]}\n pour l'obtention d'une 6 étoiles: {player.caracter[6][4]}/{player.caracter[6][5]}")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")

    @app_commands.command(name="edit_pity_of_a_player",description="permet de modifier la pity d'un joueur")
    async def see_pity_of_a_player(self,interaction:discord.Interaction,user:discord.Member,dénominateur_4:int=False,dénominateur_5:int=False,numérateur_4:int=False,numérateur_5:int=False,dénominateur_6:int=False,numérateur_6:int=False):
        if global_functions.bon_role(interaction.user):
            player = global_functions.Player(user.name,user.id)
            player.is_player()
            if not numérateur_5:
                numérateur_5=player.caracter[6][1]
            if not numérateur_4:
                numérateur_4=player.caracter[6][0]
            if not dénominateur_4:
                dénominateur_4=player.caracter[6][2]
            if not dénominateur_5:
                dénominateur_5=player.caracter[6][3]
            if not numérateur_6:
                numérateur_6=player.caracter[6][4]
            if not dénominateur_6:
                dénominateur_6=player.caracter[6][5]
            player.caracter[6] = [numérateur_4,numérateur_5,dénominateur_4,dénominateur_5,numérateur_6,dénominateur_6]
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"le joueur {user.name} a désormais comme pity: \npour 4 étoiles: {player.caracter[6][0]}/{player .caracter[6][2]} \npour 5 étoiles {player.caracter[6][1]}/{player .caracter[6][3]} \net pour 6 étoiles: {player.caracter[6][4]}/{player .caracter[6][5]} ")
        else:
             await interaction.response.send_message("vous n'avez pas le bon role")   

async def setup(bot):
    await bot.add_cog(Tirage(bot))