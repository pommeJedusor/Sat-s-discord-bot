from discord.ext import commands
import discord
from discord import app_commands

import global_functions, dtb_funcs
from datas.datas import Datas

class ItemsOwned(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #modos
    @app_commands.command(name="add_item_to_a_player",description="permet à un modo d'ajouter un item à un joueur")
    async def add_item_to_a_player(self,interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            item=global_functions.Items(name)
            if item.is_item() and nombre>0:
                player.add_items([{"id":item.id,"nb":nombre}],tirage=False)
                await interaction.edit_original_response(content=f":gift: **L'objet __{name}__ (x{nombre}) a bien été ajouté à {user.name}** :gift:")
            elif not item.is_item():
                await interaction.edit_original_response(content=f"{name} n'as pas été trouvé")
            else:
                await interaction.edit_original_response(content=f"vous ne pouvez ajouter qu'un nombre positif d'objets à un joueur")
        else:
            await interaction.edit_original_response(content=f"vous n'avez pas le bon role")

    @app_commands.command(name="remove_item_from_a_player",description="permet à un modo de retirer un item à un joueur")
    async def remove_item_from_a_player(self,interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            item=global_functions.Items(name)
            if item.is_item():
                player_item = dtb_funcs.get_player_item(player.id, item.id)

                if not player_item:
                    await interaction.edit_original_response(content=f"{user.name} ne possède pas l'item {name} ")
                elif player_item[3]<nombre:
                    await interaction.edit_original_response(content=f"vous essayer de retirer {nombre} fois l'item {name} à {user.name} qui ne le possède que {player_item[3]} fois")
                else:
                    if player.lose_item(item.id,nombre):
                        await interaction.edit_original_response(content=f"l'item {name} a bien été retiré {nombre} fois à {user.name}")
                    else:
                        await interaction.edit_original_response(content="échec pour des raisons inconnues")
            else:
                await interaction.edit_original_response(content=f"{name} n'as pas été trouvé")
        else:
            await interaction.edit_original_response(content=f"vous n'avez pas le bon role")

    @app_commands.command(name="see_items_of_a_player",description="permet à un modo de voir les items d'un joueur")
    async def see_items_of_a_player(self,interaction:discord.Interaction, user:discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            text = ""
            player = global_functions.Player(user.name,user.id)
            player.is_player()

            player_items = dtb_funcs.get_player_items(player_id=player.id)
            for i in range(7):
                for player_item in player_items:
                    item = global_functions.Items("pomme",id=player_item[1])
                    item.is_item(by_name=False)
                    if item.stars==i:
                        stars = "".join([":star:" for i in range(item.stars)])
                        text+=f"{stars} - **{item.name} (x{player_item[3]}) **\n"

            if text:
                await interaction.edit_original_response(content=text)
            else:
                await interaction.edit_original_response(content="ce joueur n'as pas d'items")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon role")
    
    @app_commands.command(name="see_effects_of_a_player",description="permet de voir les effets d'un joueur")
    async def see_effects_of_a_player(self,interaction: discord.Interaction, user:discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            text=""
            for player_item in dtb_funcs.get_player_items(player_id=player.id):
                item=global_functions.Items("pomme",id=player_item[1])
                if item.is_item(by_name=False):
                    for effect in dtb_funcs.get_effects(item_id=item.id,nb_items=player_item[3]):
                        text+=f"l'item {item.name} lui octroy l'effect: {effect[1]} \n"

            if text !="":
                await interaction.edit_original_response(content=text)
            else:
                await interaction.edit_original_response(content=f"il n'aucun effet")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon role")

    #players
    @app_commands.command(name="see_effects",description="permet de voir ses effets")
    async def see_effects(self,interaction: discord.Interaction):
        await interaction.response.defer()
        player = global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        for player_item in dtb_funcs.get_player_items(player_id=player.id):
                item=global_functions.Items("pomme",id=player_item[1])
                if item.is_item(by_name=False):
                    for effect in dtb_funcs.get_effects(item_id=item.id,nb_items=player_item[3]):
                        text+=f"l'item {item.name} vous octroy l'effect: {effect[1]} \n"

        if text !="":
            await interaction.edit_original_response(content=text)
        else:
            await interaction.edit_original_response(content=f":x: **Vous n'avez aucun effet.** :x:")
    
    @app_commands.command(name="see_items",description="permet de voir ses items")
    async def see_items(self,interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        player = global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        player_items = dtb_funcs.get_player_items(player_id=player.id)

        if not player_items:
            await interaction.edit_original_response(content="malheureusement vous ne possédez aucun item, n'hésitez pas à faire des tirages pour en avoir ")
            return
        
        text+=f"**   {Datas.emogi_cristal} Ton inventaire : {Datas.emogi_cristal}**\n\n"
        text+=f"__**Objets :**__\n"
        
        for i in range(7):
            for player_item in player_items:
                item=global_functions.Items("pomme",id=player_item[1])
                item.is_item(by_name=False)
                if item.stars==i:
                    stars = "".join([":star:" for i in range(item.stars)])
                    text+=f"{stars} - **{item.name} (x{player_item[3]}) **\n"

        await interaction.edit_original_response(content=text)


async def setup(bot):
    await bot.add_cog(ItemsOwned(bot))