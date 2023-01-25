import discord
from discord import app_commands
from discord.ext import commands
import global_functions
from datas.datas import Datas

class Gems(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="add_gems",description="permet à un modo d'ajouter à un joueur un nombre de gemmes choisis par l'éxécutant de la commande")
    async def add_gems(self,interaction: discord.Interaction, nombre_de_gemmes: int, user: discord.Member):
        if global_functions.bon_role(interaction.user) and nombre_de_gemmes>0:
            player = global_functions.Player(user.name,user.id)
            player.is_player()
            player.caracter[2]+=nombre_de_gemmes
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"les {nombre_de_gemmes} gemme(s) ont bien été ajoués à {user.name} ")
        elif nombre_de_gemmes==0:
            await interaction.response.send_message("euh.... ???? vous êtes sûr??? bon ... bah ... c'est fait.. je suppose???")
        elif nombre_de_gemmes<0:
            await interaction.response.send_message("les nombres nuls ou négatifs ne sont pas accepter veuillez utiliser la commande '/destroy_gems' ou son homologue '\spend_gems'")
        else:
            await interaction.response.send_message("vous n'avez pas le bon rôle")

    @app_commands.command(name="see_gems_of_a_player",description="permet à un modo de voir les gemmes d'un joueur")
    async def see_gems_of_a_player(self,interaction : discord.Interaction, user : discord.Member):
        if global_functions.bon_role(interaction.user):
            player = global_functions.Player(user.name,user.id)
            player.is_player()
            await interaction.response.send_message(f"{Datas.emogi_cristal} **{user.name}** possède **{player.caracter[2]} Cristaux d'Expédition ** ! {Datas.emogi_cristal}\n{Datas.emogi_cristal} a dépensé au total **{player.caracter[3]} Cristaux d'Expédition **! {Datas.emogi_cristal}")
        else:
            await interaction.response.send_message(f"vous n'avez pas le bon rôle")

    @app_commands.command(name="spend_gems",description="permet de dépenser les gemmes d'un joueur")
    @app_commands.describe(depenser="True pour enlever les gemmes et augmenter 'les gemmes dépenser', False pour juste les enlever")
    async def spend_gems(self,interaction:discord.Interaction,user:discord.Member,nombres_de_gemmes:int,depenser:bool=False):
        player=global_functions.Player(user.name,user.id)
        player.is_player()
        if global_functions.bon_role(interaction.user) and player.caracter[2]>=nombres_de_gemmes>0:
            player.caracter[2]-=nombres_de_gemmes
            if depenser:
                player.caracter[3]+=nombres_de_gemmes
            player.update_stats_player_fichier()
            await interaction.response.send_message(f"les {nombres_de_gemmes} gemmes de {user.name} ont bien été dépensé qui a maintenant {player.caracter[2]} gemmes ")
        elif not global_functions.bon_role(interaction.user):
            await interaction.response.send_message("vous n'avez pas le bon role")
        elif not nombres_de_gemmes>0:
            await interaction.response.send_message("ous ne pouvez pas retirer un nombre nul ou négatif de gemmes user de la commande '/add_gems' pour cette effet")
        else:
            await interaction.response.send_message(f"vous ne pouvez pas retirer {nombres_de_gemmes} gemmes à un joueur qui en a moins ({player.caracter[2]}) ")

    @app_commands.command(name="see_gems",description="permet de voir son nombre de gemmes possédés et dépensé ")
    async def see_gems(self,interaction : discord.Interaction):
        player = global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        await interaction.response.send_message(f"{Datas.emogi_cristal} Vous possédez **{player.caracter[2]} Cristaux d'Expédition** ! {Datas.emogi_cristal}\n{Datas.emogi_cristal} Vous avez dépensez au total **{player.caracter[3]} Cristaux d'Expédition** ! {Datas.emogi_cristal}")


async def setup(bot):
    await bot.add_cog(Gems(bot))