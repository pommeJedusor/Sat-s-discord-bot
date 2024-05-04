import discord
from discord.ext import commands
from discord import app_commands

import json, random
from typing import Optional

import global_functions
from datas.datas import Datas

class Items(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="create_item",description="permet à un modo de creer un item")
    async def create_item(self,interaction:discord.Interaction,name:str,nombre_d_étoiles:int,indice_drop:int,img_link:str):
        item=global_functions.Items(name,nombre_d_étoiles,indice_drop,img_link,id=random.randint(1,1000000000))
        if not item.is_item() and global_functions.bon_role(interaction.user):
            if item.add_item():
                await interaction.response.send_message(f"l'item {name} {nombre_d_étoiles} étoiles avec un indice de drop {indice_drop} a bien été rajouté à la base de donnés")
            else:
                await interaction.response.send_message("l'ajout de l'item a échoué pour des raisons inconnus")
        elif not global_functions.bon_role(interaction.user):
            await interaction.response.send_message("vous n'avez pas le bon role")
        else:
            await interaction.response.send_message(f"l'item {name} existe déja")

    @app_commands.command(name="edit_item",description="permet à un modo de modifier un item")
    async def edit_item(self,interaction:discord.Interaction,name:str,nombre_d_étoiles:Optional[int],indice_drop:Optional[int],image_link:Optional[str],effets:Optional[str],tirage_active:Optional[bool],new_name:Optional[str]):
        item=global_functions.Items(name)
        if item.is_item() and global_functions.bon_role(interaction.user):
            item.caracter[0]=name
            message=f"l'item {name} a bien été modifié, et à comme caractéristique:\n"
            if new_name is not None:
                new_item=global_functions.Items(new_name)
                if not new_item.is_item():
                    item.caracter[0]=new_name
                    message=f"l'item {name} ({new_name} maintenant) a bien été modifié, et à comme caractéristique:\n"
            if nombre_d_étoiles is not None:
                item.caracter[1]=nombre_d_étoiles
                message+=f"étoiles: {nombre_d_étoiles}\n"
            if indice_drop is not None:
                item.caracter[2]=indice_drop
                message+=f"indice de drop: {indice_drop}\n"
            if image_link is not None:
                item.caracter[3]=image_link
                message+=f"lien pour l'image: {image_link}\n"
            if effets is not None:
                effets=effets.split(",")
                item.caracter[4]=effets
                message+=f"effets: {effets}\n"
            if tirage_active is not None:
                item.caracter[5]=tirage_active
                if tirage_active:
                    message+=f"est dans les tirages: oui\n"
                else:
                    message+=f"est dans les tirages: non\n"
            item.update_item()
            await interaction.response.send_message(message)
        elif not global_functions.bon_role(interaction.user):
            await interaction.response.send_message(f"vous n'avez pas le bon rôle ")
        else:
            await interaction.response.send_message(f"l'item {name} n'as pas été trouvé ")
    
    @app_commands.choices(tri=[
    app_commands.Choice(name="stars", value="stars"),
    app_commands.Choice(name="name", value="name"),
    ])
    @app_commands.command(name="see_all_items",description="permet de voir tous les items")
    async def see_all_items(self,interaction:discord.Interaction,stars:int=None,active:bool=None,drop:int=None, tri :app_commands.Choice[str]=None):

        stars_filter = lambda ligne: stars==None or ligne[1]==stars
        active_filter = lambda ligne: active==None or ligne[5]==active
        drop_filter = lambda ligne: drop==None or ligne[2]==drop

        items=""
        lignes=[]
        with open(Datas.items_file,'r')as f:
            for ligne in f:
                ligne=json.loads(ligne)
                lignes.append(ligne)

        lignes = list(filter(active_filter,lignes))
        lignes = list(filter(stars_filter,lignes))
        lignes = list(filter(drop_filter,lignes))
        items_tried = lignes
        if tri and tri.value=="stars":
            items_tried = []
            for i in range(1,6):
                for ligne in lignes:
                    if ligne[1]==i:
                        items_tried.append(ligne)
        elif tri and tri.value=="name":
            items_tried = sorted(lignes)
        lignes = items_tried

        for ligne in lignes:
            items+=f"nom: {ligne[0]}, {ligne[1]} étoiles, drop:{ligne[2]}, effets:{ligne[4]}"
            if ligne[5]:
                items+=", est présent dans les tirages \n"
            else:
                items+=", est absent des tirages \n"
        await interaction.response.send_message(items)

    @app_commands.command(name="delete_item",description="permet de supprimer un item")
    async def delete_item(self,interaction:discord.Interaction,name:str):
        item=global_functions.Items(name)
        if item.is_item() and global_functions.bon_role(interaction.user):
            item.delete_item()
            await interaction.response.send_message(f"l'item {name} a été supprimé ")
        elif not global_functions.bon_role(interaction.user):
            await interaction.response.send_message("vous n'avez pas le bon role")
        else:
            await interaction.response.send_message(f"l'item {name} n'as pas été trouvé")
    

    @app_commands.command(name="see_image_item",description="permet de voir l'image d'un item")
    async def change_channel(self,interaction:discord.Interaction,name_item:str):
        item=global_functions.Items(name_item)
        if item.is_item() and item.caracter[3]:
            await interaction.response.send_message(item.caracter[3])
        elif not item.caracter[3]:
            await interaction.response.send_message(f"l'item {item} n'as pas d'image ")
        else:
            await interaction.response.send_message(f"l'item {item} n'as pas été trouvé")

    

async def setup(bot):
    await bot.add_cog(Items(bot))