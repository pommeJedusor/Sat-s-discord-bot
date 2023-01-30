from discord.ext import commands
import discord
from discord import app_commands

import global_functions
from datas.datas import Datas

class ItemsOwned(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="add_item_to_a_player",description="permet à un modo d'ajouter un item à un joueur")
    async def add_item_to_a_player(self,interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            item=global_functions.Items(name)
            if item.is_item() and nombre>0:
                player.add_item([{"id":item.caracter[6],"nb":nombre}])
                await interaction.response.send_message(f":gift: **L'objet __{name}__ (x{nombre}) a bien été ajouté à {user.name}** :gift:")
            elif not item.is_item():
                await interaction.response.send_message(f"{name} n'as pas été trouvé")
            else:
                await interaction.response.send_message(f"vous ne pouvez ajouter qu'un nombre positif d'objets à un joueur")
        else:
            await interaction.response.send_message(f"vous n'avez pas le bon role")

    @app_commands.command(name="remove_item_from_a_player",description="permet à un modo de retirer un item à un joueur")
    async def remove_item_from_a_player(self,interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            item=global_functions.Items(name)
            if item.is_item():
                item_filter = lambda items: items["id"]==item.caracter[6]
                item_player = list(filter(item_filter,player.caracter[4]))
                if len(item_player)>1:
                    print(f"l'item{item} avec l'id {item.caracter[6]} apparait plusieur fois chez {player}")

                if item_player and item_player[0]["nb"]>=nombre>0:
                    item_player = item_player[0]
                    player.lose_item(item.caracter[6],nombre)
                    await interaction.response.send_message(f"l'item {name} a bien été retiré {nombre} fois à {user.name}")
                
                elif not item_player:
                    await interaction.response.send_message(f"{user.name} ne possède pas l'item {name} ")
                elif not item_player[0]["nb"]>=nombre:
                    await interaction.response.send_message(f"vous essayer de retirer {nombre} fois l'item {name} à {user.name} qui ne le possède que {item_player[0]['nb']} fois")
                else:
                    await interaction.response.send_message(f"vous ne pouvez retirer qu'un nombre positif d'objets à un joueur")
            else:
                await interaction.response.send_message(f"{name} n'as pas été trouvé")
        else:
            await interaction.response.send_message(f"vous n'avez pas le bon role")

    @app_commands.command(name="see_items",description="permet de voir ses items")
    async def see_items(self,interaction:discord.Interaction):
        player = global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        if player.caracter[4]:
            text+=f"**   {Datas.emogi_cristal} Ton inventaire : {Datas.emogi_cristal}**\n\n"
            text+=f"__**Objets :**__\n"
        items_tried = []
        for i in range(1,6):
            for item in player.caracter[4]:
                iteme=global_functions.Items("pomme",id=item['id'])
                iteme.is_item(x=6)
                if iteme.caracter[1]==i:
                    items_tried.append(item)
        for item in items_tried:
            iteme=global_functions.Items("pomme",id=item['id'])
            iteme.is_item(x=6)
            stars = "".join([":star:" for i in range(iteme.caracter[1])])
            text+=f"{stars} - **{iteme.caracter[0]} (x{item['nb']}) **\n"
        if not text:
            text="malheureusement vous ne possédez aucun item, n'hésitez pas à faire des tirages pour en avoir "
        await interaction.response.send_message(text)

    @app_commands.command(name="see_items_of_a_player",description="permet à un modo de voir les items d'un joueur")
    async def see_items_of_a_player(self,interaction:discord.Interaction, user:discord.Member):
        if global_functions.bon_role(interaction.user):
            player = global_functions.Player(user.name,user.id)
            player.is_player()
            text=""
            items_tried = []
            for i in range(1,6):
                for item in player.caracter[4]:
                    iteme=global_functions.Items("pomme",id=item['id'])
                    iteme.is_item(x=6)
                    if iteme.caracter[1]==i:
                        items_tried.append(item)
            for item in items_tried:
                iteme=global_functions.Items("pomme",id=item['id'])
                iteme.is_item(x=6)
                stars = "".join([":star:" for i in range(iteme.caracter[1])])
                text+=f"{stars} - **{iteme.caracter[0]} (x{item['nb']}) **\n"
            if text:
                await interaction.response.send_message(text)
            else:
                await interaction.response.send_message("ce joueur n'as pas d'items")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")

    @app_commands.command(name="see_effects",description="permet de voir ses effets")
    async def see_effects(self,interaction: discord.Interaction):
        player = global_functions.Player(interaction.user.name,interaction.user.id)
        player.is_player()
        text=""
        for i in player.caracter[4]:
            item=global_functions.Items("pomme",id=i['id'])
            if item.is_item(x=6) and item.caracter[4]:
                effet=""
                if i['nb']>=len(item.caracter[4]):
                    effet=item.caracter[4][-1]
                else:
                    effet=item.caracter[4][i['nb']]
                text+=f"l'item {item.caracter[0]} vous octroy l'effet: {effet} \n"
        if text !="":
            await interaction.response.send_message(text)
        else:
            await interaction.response.send_message(f":x: **Vous n'avez aucun effet.** :x:")

    @app_commands.command(name="see_effects_of_a_player",description="permet de voir les effets d'un joueur")
    async def see_effects_of_a_player(self,interaction: discord.Interaction, user:discord.Member):
        if global_functions.bon_role(interaction.user):
            player=global_functions.Player(user.name,user.id)
            player.is_player()
            text=""
            for i in player.caracter[4]:
                item=global_functions.Items("pomme",id=i['id'])
                if item.is_item(x=6) and item.caracter[4]:
                    effet=""
                    if i['nb']>=len(item.caracter[4]):
                        effet=item.caracter[4][-1]
                    else:
                        effet=item.caracter[4][i['nb']]
                    text+=f"l'item {item.caracter[0]} lui octroy l'effet: {effet} \n"
            if text !="":
                await interaction.response.send_message(text)
            else:
                await interaction.response.send_message(f"il n'aucun effet")
        else:
            await interaction.response.send_message("vous n'avez pas le bon role")


async def setup(bot):
    await bot.add_cog(ItemsOwned(bot))