import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

import global_functions, dtb_funcs
from datas.datas import Datas

class Items(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #modo
    @app_commands.command(name="create_item",description="permet à un modo de creer un item")
    async def create_item(self,interaction:discord.Interaction,name:str,nombre_d_étoiles:int,indice_drop:int,img_link:str):
        await interaction.response.defer()
        item=global_functions.Items(name,nombre_d_étoiles,indice_drop,img_link)
        if not item.is_item() and global_functions.bon_role(interaction.user):
            if nombre_d_étoiles<1:
                await interaction.edit_original_response(content="il est impossible de créer des items de moin d'une étoile")
            elif indice_drop<0:
                await interaction.edit_original_response(content="il est impossible de créer des items avec un indice de drop de moins de 0")
            elif item.add_item():
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
        if item.is_item() and global_functions.bon_role(interaction.user) and (nombre_d_étoiles==None or nombre_d_étoiles>0) and (indice_drop==None or indice_drop>=0):
            item.name=name
            message=f"l'item {name} a bien été modifié, et à comme caractéristique:\n"
            if new_name:
                new_item=global_functions.Items(new_name)
                if not new_item.is_item():
                    item.name=new_name
                    message=f"l'item {name} ({new_name} maintenant) a bien été modifié, et à comme caractéristique:\n"
                else:
                    await interaction.edit_original_response(content=f"le nouveau nom de l'item {name} est déjà attribué à un item")
                    return
            if nombre_d_étoiles!=None:
                item.stars=nombre_d_étoiles
                message+=f"étoiles: {nombre_d_étoiles}\n"
            if indice_drop!=None:
                item.drop=indice_drop
                message+=f"indice de drop: {indice_drop}\n"
            if image_link:
                item.url_img=image_link
                message+=f"lien pour l'image: {image_link}\n"
            if effets:
                effets=effets.split(",")
                item.effects=effets
                message+=f"effets: {effets}\n"
            if tirage_active!=None:
                item.on_tirage=tirage_active
                if tirage_active:
                    message+=f"est dans les tirages: oui\n"
                else:
                    message+=f"est dans les tirages: non\n"
            item.update_item()
            await interaction.edit_original_response(content=message)
        elif not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle ")
        elif (nombre_d_étoiles!=None and nombre_d_étoiles<1):
            await interaction.edit_original_response(content="il est impossible d'avoir des items de moins d'une étoile")
        elif (indice_drop!=None and indice_drop<0):
            await interaction.edit_original_response(content="il est impossible d'avoir des items à l'indice de drop négatif")
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

        stars_filter = lambda item_dtb: stars==None or item_dtb[2]==stars
        active_filter = lambda item_dtb: active==None or item_dtb[5]==active
        drop_filter = lambda item_dtb: drop==None or item_dtb[3]==drop

        items=[]
        items_dtb = dtb_funcs.get_items()

        items_dtb = list(filter(active_filter,items_dtb))
        items_dtb = list(filter(stars_filter,items_dtb))
        items_dtb = list(filter(drop_filter,items_dtb))

        items_tried = items_dtb
        #if tri==None or tri.value=="stars":
        if (tri and tri.value=="stars") or tri==None:
            items_tried = []
            for nb_stars in range(1,7):
                for ligne in items_dtb:
                    if ligne[2]==nb_stars:
                        items_tried.append(ligne)

        get_name = lambda item_dtb: item_dtb[1]
        if tri and tri.value=="name":
            items_tried = sorted(items_dtb,key=get_name)
        items_dtb = items_tried

        for ligne in items_dtb:
            stars = "".join([":star:" for i in range(ligne[2])])
            if ligne[5]:
                items.append(f"{stars} - **__{ligne[1]}__**  - Taux : {ligne[3]}  - Présent\n")
            else:
                items.append(f"{stars} - **__{ligne[1]}__**  - Taux : {ligne[3]}  - Absent\n")
        await interaction.edit_original_response(content=f"**  {Datas.emogi_cristal}  Liste des objets:{Datas.emogi_cristal}**\n\n__**Objets :**__")
        if items:
            await interaction.channel.send("".join(items[:10]))
        for i in range(1,(len(items)-1)//10+1):
            await interaction.channel.send("".join(items[10*i:10*i+10]))

    
    @app_commands.command(name="see_image_item",description="permet de voir l'image d'un item")
    async def change_channel(self,interaction:discord.Interaction,name_item:str):
        await interaction.response.defer()
        item=global_functions.Items(name_item)
        if item.is_item() and item.url_img:
            await interaction.edit_original_response(content=item.url_img)
        elif not item.is_item():
            await interaction.edit_original_response(content=f"l'item {item.name} n'as pas été trouvé")
        elif not item.url_img:
            await interaction.edit_original_response(content=f"l'item {item.name} n'as pas d'image ")

    

async def setup(bot):
    await bot.add_cog(Items(bot))