import discord
from discord import app_commands
from discord.ext import commands

import global_functions

import random, asyncio

class Tirage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="tirage",description="permet de faire des tirages")
    async def tirages(self,interaction:discord.Interaction,nombre_de_tirage:int):
        player = global_functions.Player(interaction.user.id,interaction.user.id)
        player.is_player()
        channel_perso=self.bot.get_channel(player.caracter[5])
        if player.caracter[2]>=nombre_de_tirage and nombre_de_tirage<=10:
            await interaction.response.send_message(f"vous avez obtenus...")
            if nombre_de_tirage>player.caracter[10]:
                poire=player.caracter[10]
            else:
                poire=nombre_de_tirage
            patate=0
            for i in range(poire):
                if random.randint(1,5)==4:
                    patate+=1
                    nombre_de_tirage-=1
                    player.caracter[1]+=2
                    player.caracter[2]-=1
                    player.caracter[3]+=1
                player.caracter[10]-=1
            for i in range(patate):
                await channel_perso.send("vous avez gagné 2 gemmes")
                if not interaction.channel==channel_perso:
                    await interaction.channel.send("vous avez gagné 2 gemmes")
                await asyncio.sleep(2)
            player.update_stats_player_fichier()
            for i in player.tirages(nombre_de_tirage):
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
        elif nombre_de_tirage>10:
            await interaction.response.send_message("vous ne pouvez éffectuer qu'un maximum de 10 tirages à la fois")
        else:
            await interaction.response.send_message(f"il vous manque {nombre_de_tirage-player.caracter[2]} gemmes")

    @app_commands.command(name="change_channel",description="permet de changer ou d'initialiser le channel d'un joueur")
    async def change_channel(self,interaction:discord.Interaction,user:discord.Member):
        player = global_functions.Player(user.name,user.id)
        player.is_player()
        if global_functions.bon_role(interaction.user):
            player.caracter[5]=interaction.channel_id
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"le nouveau channel perso de {user} est désormais {interaction.channel.name} ")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")

    @app_commands.command(name="see_pity",description="permet de voir sa pity")
    async def voir_sa_pity(self,interaction:discord.Interaction):
        player=global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        await interaction.response.send_message(f"pour l'obtention d'une 4 étoiles: {player.caracter[6][0]}/{player.caracter[6][2]} \n pour l'obtention d'une 5 étoiles: {player.caracter[6][1]}/{player.caracter[6][3]}")

    @app_commands.command(name="see_pity_of_a_player",description="permet de voir la pity d'un joueur")
    async def see_pity_of_a_player(self,interaction:discord.Interaction,user:discord.Member):
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            await interaction.response.send_message(f"pour l'obtention d'une 4 étoiles: {player.caracter[6][0]}/{player.caracter[6][2]} \n pour l'obtention d'une 5 étoiles: {player.caracter[6][1]}/{player.caracter[6][3]}")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")

async def setup(bot):
    await bot.add_cog(Tirage(bot))