from discord import app_commands
from discord.ext import commands
import discord
import datetime

import global_functions
import json

from datas.datas import Datas

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @app_commands.command(name="recompense_question_semaine", description="choisir le nombre de gemmes de récompense par défaut 2")
    async def reward_question_semaine(self,interaction:discord.Interaction,gemmes:int):
        #check si modo
        if not global_functions.bon_role(interaction.user):
            await interaction.response.send_message(f"vous n'avez pas le bon rôle")
            return 0
        
        with open(Datas.question_file,"r") as f:
            ligne = f.readline()
            if ligne:
                line=json.loads(ligne)
            else:
                line = {"nb_gemmes": 0, "id_users": [], "starttime": 0, "message_id": 0}
        dif_gems = gemmes - line["nb_gemmes"]
        line["nb_gemmes"] = gemmes
        with open(Datas.question_file, "w") as f:
            f.write(json.dumps(line))

        #fonctionnemnt rétroactif
        for id_user in line["id_users"]:
            user = self.bot.get_user(id_user)
            player = global_functions.Player(user.name,user.id)
            player.is_player()
            player.caracter[2]+=dif_gems
            player.update_stats_player_fichier()

        await interaction.response.send_message(f"la récompense est désormais de {gemmes}")

    @app_commands.command(name="oubli_question", description="si mention ajouté à la queston de la semaine par edit")
    async def oubli_question(self,interaction:discord.Interaction,gemmes:int,énième_message:int=None,message_id:str=None):
        try:
            if message_id:
                message_id = int(message_id)
        except:
            await interaction.response.send_message(f"entrez un nombre valide",ephemeral=True)
            return 0
        right_message = None
        channel_question=self.bot.get_channel(Datas.channel_question)
        if not global_functions.bon_role(interaction.user):
            await interaction.response.send_message(f"vous n'avez pas le bon rôle",ephemeral=True)
            return 0
        elif (énième_message and message_id):
            await interaction.response.send_message(f"vous ne pouvez pas choisir 'énèime message' et 'message id' en même temps",ephemeral=True)
            return 0
        elif not (énième_message or message_id):
            await interaction.response.send_message(f"vous devez choisir 'énième message' 'ou message_id'",ephemeral=True)
            return 0
        elif message_id:
            async for message in channel_question.history(oldest_first=False):
                if message.id==message_id:
                    right_message = message
                    break
        elif énième_message:
            async for message in channel_question.history(oldest_first=False,limit=énième_message):
                right_message = message
        if right_message:
            args={"nb_gemmes":gemmes,"id_users":[],"starttime":datetime.datetime.timestamp(right_message.created_at),"message_id":right_message.id}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))
            await interaction.response.send_message(f"la question de {right_message.author} a été posée avec succès\nl'id: {right_message.id}\n<@718805832652816486> faut redémarrer le bot")
        else:
            await interaction.response.send_message(f"le message n'as pas été trouvé")


            


async def setup(bot):
    await bot.add_cog(Question(bot))