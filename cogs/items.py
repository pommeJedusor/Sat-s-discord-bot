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

    #modo
    @app_commands.command(name="create_item",description="permet à un modo de creer un item")
    async def create_item(self,interaction:discord.Interaction,name:str,nombre_d_étoiles:int,indice_drop:int,img_link:str):
        await interaction.response.defer()
        item=global_functions.Items(name,nombre_d_étoiles,indice_drop,img_link,id=random.randint(1,1000000000))
        if not item.is_item() and global_functions.bon_role(interaction.user):
            if item.add_item():
                await interaction.edit_original_response(content=f"l'item {name} {nombre_d_étoiles} étoiles avec un indice de drop {indice_drop} a bien été rajouté à la base de donnés")
            else:
                await interaction.edit_original_response(content="l'ajout de l'item a échoué pour des raisons inconnus")
        elif not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content="vous n'avez pas le bon role")
        else:
            await interaction.edit_original_response(content=f"l'item {name} existe déja")

    @app_commands.command(name="edit_item",description="permet à un modo de modifier un item")
    async def edit_item(self,interaction:discord.Interaction,name:str,nombre_d_étoiles:Optional[int],indice_drop:Optional[int],image_link:Optional[str],effets:Optional[str],tirage_active:Optional[bool],new_name:Optional[str]):
        await interaction.response.defer()
        item=global_functions.Items(name)
        if item.is_item() and global_functions.bon_role(interaction.user):
            item.name=name
            message=f"l'item {name} a bien été modifié, et à comme caractéristique:\n"
            if new_name is not None:
                new_item=global_functions.Items(new_name)
                if not new_item.is_item():
                    item.name=new_name
                    message=f"l'item {name} ({new_name} maintenant) a bien été modifié, et à comme caractéristique:\n"
            if nombre_d_étoiles is not None:
                item.stars=nombre_d_étoiles
                message+=f"étoiles: {nombre_d_étoiles}\n"
            if indice_drop is not None:
                item.drop=indice_drop
                message+=f"indice de drop: {indice_drop}\n"
            if image_link is not None:
                item.url_img=image_link
                message+=f"lien pour l'image: {image_link}\n"
            if effets is not None:
                effets=effets.split(",")
                item.effects=effets
                message+=f"effets: {effets}\n"
            if tirage_active is not None:
                item.on_tirage=tirage_active
                if tirage_active:
                    message+=f"est dans les tirages: oui\n"
                else:
                    message+=f"est dans les tirages: non\n"
            item.update_item()
            await interaction.edit_original_response(content=message)
        elif not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle ")
        else:
            await interaction.edit_original_response(content=f"l'item {name} n'as pas été trouvé ")
    
    @app_commands.command(name="delete_item",description="permet de supprimer un item")
    async def delete_item(self,interaction:discord.Interaction,name:str):
        await interaction.response.defer()
        item=global_functions.Items(name)
        if item.is_item() and global_functions.bon_role(interaction.user):
            item.delete_item()
            await interaction.edit_original_response(content=f"l'item {name} a été supprimé ")
        elif not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content="vous n'avez pas le bon role")
        else:
            await interaction.edit_original_response(content=f"l'item {name} n'as pas été trouvé")

    #players
    @app_commands.choices(tri=[
    app_commands.Choice(name="stars", value="stars"),
    app_commands.Choice(name="name", value="name"),
    ])
    @app_commands.command(name="see_all_items",description="permet de voir tous les items")
    async def see_all_items(self,interaction:discord.Interaction,stars:int=None,active:bool=None,drop:int=None, tri :app_commands.Choice[str]=None):
        await interaction.response.defer()

        stars_filter = lambda ligne: stars==None or ligne[1]==stars
        active_filter = lambda ligne: active==None or ligne[5]==active
        drop_filter = lambda ligne: drop==None or ligne[2]==drop

        items=[]
        lignes=[]
        with open(Datas.items_file,'r')as f:
            for ligne in f:
                ligne=json.loads(ligne)
                lignes.append(ligne)

        lignes = list(filter(active_filter,lignes))
        lignes = list(filter(stars_filter,lignes))
        lignes = list(filter(drop_filter,lignes))
        items_tried = lignes
        if (tri and tri.value=="stars") or tri==None:
            items_tried = []
            for i in range(1,7):
                for ligne in lignes:
                    if ligne[1]==i:
                        items_tried.append(ligne)
        if tri and tri.value=="name":
            items_tried = sorted(lignes)
        lignes = items_tried

        for ligne in lignes:
            stars = "".join([":star:" for i in range(ligne[1])])
            if ligne[5]:
                items.append(f"{stars} - **__{ligne[0]}__**  - Taux : {ligne[2]}  - Présent\n")
            else:
                items.append(f"{stars} - **__{ligne[0]}__**  - Taux : {ligne[2]}  - Absent\n")
        await interaction.edit_original_response(content=f"**  {Datas.emogi_cristal}  Liste des objets:{Datas.emogi_cristal}**\n\n__**Objets :**__")
        await interaction.channel.send("".join(items[:10]))
        for i in range(1,(len(items)-1)//10+1):
            await interaction.channel.send("".join(items[10*i:10*i+10]))

    
    @app_commands.command(name="see_image_item",description="permet de voir l'image d'un item")
    async def change_channel(self,interaction:discord.Interaction,name_item:str):
        await interaction.response.defer()
        item=global_functions.Items(name_item)
        if item.is_item() and item.url_img:
            await interaction.edit_original_response(content=item.url_img)
        elif not item.url_img:
            await interaction.edit_original_response(content=f"l'item {item} n'as pas d'image ")
        else:
            await interaction.edit_original_response(content=f"l'item {item} n'as pas été trouvé")

    

async def setup(bot):
    await bot.add_cog(Items(bot))