from discord.ext import commands
import discord
from discord import app_commands

from model import global_functions
from model import ModelPlayer
from model import ModelItem

from datas.datas import Datas

class ItemsOwned(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    #modos
    @app_commands.command(name="add_item_to_a_player",description="permet à un modo d'ajouter un item à un joueur")
    async def add_item_to_a_player(self,interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player=ModelPlayer.Player(user.name,user.id)
            player.is_player()
            item=ModelItem.Items(name)
            if item.is_item() and nombre>0:
                player.add_item([{"id":item.id,"nb":nombre}])
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
            player=ModelPlayer.Player(user.name,user.id)
            player.is_player()
            item=ModelItem.Items(name)
            if item.is_item():
                item_filter = lambda items: items["id"]==item.id
                item_player = list(filter(item_filter,player.items))
                if len(item_player)>1:
                    print(f"l'item{item} avec l'id {item.id} apparait plusieur fois chez {player}")

                if item_player and item_player[0]["nb"]>=nombre>0:
                    item_player = item_player[0]
                    player.lose_item(item.id,nombre)
                    await interaction.edit_original_response(content=f"l'item {name} a bien été retiré {nombre} fois à {user.name}")
                
                elif not item_player:
                    await interaction.edit_original_response(content=f"{user.name} ne possède pas l'item {name} ")
                elif not item_player[0]["nb"]>=nombre:
                    await interaction.edit_original_response(content=f"vous essayer de retirer {nombre} fois l'item {name} à {user.name} qui ne le possède que {item_player[0]['nb']} fois")
                else:
                    await interaction.edit_original_response(content=f"vous ne pouvez retirer qu'un nombre positif d'objets à un joueur")
            else:
                await interaction.edit_original_response(content=f"{name} n'as pas été trouvé")
        else:
            await interaction.edit_original_response(content=f"vous n'avez pas le bon role")

    @app_commands.command(name="see_items_of_a_player",description="permet à un modo de voir les items d'un joueur")
    async def see_items_of_a_player(self,interaction:discord.Interaction, user:discord.Member):
        await interaction.response.defer()
        if global_functions.bon_role(interaction.user):
            player = ModelPlayer.Player(user.name,user.id)
            player.is_player()
            text=""
            items_tried = []
            for i in range(1,7):
                for item in player.items:
                    iteme=ModelItem.Items("pomme",id=item['id'])
                    iteme.is_item(x=6)
                    if iteme.stars==i:
                        items_tried.append(item)
            for item in items_tried:
                iteme=ModelItem.Items("pomme",id=item['id'])
                iteme.is_item(x=6)
                stars = "".join([":star:" for i in range(iteme.stars)])
                text+=f"{stars} - **{iteme.name} (x{item['nb']}) **\n"
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
            player=ModelPlayer.Player(user.name,user.id)
            player.is_player()
            text=""
            for i in player.items:
                item=ModelItem.Items("pomme",id=i['id'])
                if item.is_item(x=6) and item.effects:
                    effet=""
                    if i['nb']>=len(item.effects):
                        effet=item.effects[-1]
                    else:
                        effet=item.effects[i['nb']]
                    text+=f"l'item {item.name} lui octroy l'effet: {effet} \n"
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
        player = ModelPlayer.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        for i in player.items:
            item=ModelItem.Items("pomme",id=i['id'])
            if item.is_item(x=6) and item.effects:
                effet=""
                if i['nb']>=len(item.effects):
                    effet=item.effects[-1]
                else:
                    effet=item.effects[i['nb']-1]
                text+=f"l'item {item.name} vous octroy l'effet: {effet} \n"
        if text !="":
            await interaction.edit_original_response(content=text)
        else:
            await interaction.edit_original_response(content=f":x: **Vous n'avez aucun effet.** :x:")
    
    @app_commands.command(name="see_items",description="permet de voir ses items")
    async def see_items(self,interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        player = ModelPlayer.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        if player.items:
            text+=f"**   {Datas.emogi_cristal} Ton inventaire : {Datas.emogi_cristal}**\n\n"
            text+=f"__**Objets :**__\n"
        items_tried = []
        for i in range(1,7):
            for item in player.items:
                iteme=ModelItem.Items("pomme",id=item['id'])
                iteme.is_item(x=6)
                if iteme.stars==i:
                    items_tried.append(item)
        for item in items_tried:
            iteme=ModelItem.Items("pomme",id=item['id'])
            iteme.is_item(x=6)
            stars = "".join([":star:" for i in range(iteme.stars)])
            text+=f"{stars} - **{iteme.name} (x{item['nb']}) **\n"
        if not text:
            text="malheureusement vous ne possédez aucun item, n'hésitez pas à faire des tirages pour en avoir "
        await interaction.edit_original_response(content=text)


async def setup(bot):
    await bot.add_cog(ItemsOwned(bot))