from discord import app_commands
from discord.ext import commands
import discord
import datetime

import global_functions
import json, time

from datas.datas import Datas

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @app_commands.command(name="question", description="à faire juste avant de poser la question de la semaine")
    async def question(self,interaction:discord.Interaction,gemmes:int):
        if global_functions.bon_role(interaction.user):
            with open(Datas.question_file,"w") as f:
                f.write(json.dumps({"nb_gemmes": gemmes, "id_users": False, "starttime": time.time(), "message_id": interaction.user.id}))
            await interaction.response.send_message(f"c'est fait",ephemeral=True)
        else:
            await interaction.response.send_message(f"c'vous n'avez pas le bon rôle",ephemeral=True)

    @app_commands.command(name="oubli_question", description="si oublié d'utiliser la commande pour la question de la semaine")
    async def oubli_question(self,interaction:discord.Interaction,gemmes:int,questionneur:discord.Member):
        if global_functions.bon_role(interaction.user):
            pomme=False
            channel_question=self.bot.get_channel(Datas.channel_question)
            async for message in channel_question.history(oldest_first=False):
                if message.author.id==questionneur.id:
                    with open(Datas.question_file,"w") as f:
                        f.write(json.dumps({"nb_gemmes": gemmes, "id_users": [], "starttime": datetime.datetime.timestamp(message.created_at), "message_id": message.id}))
                        pomme=True
                        good_message=message
                    break
            if pomme:
                await interaction.response.send_message(f"c'est fait",ephemeral=True)
                async for message in channel_question.history(after=message,oldest_first=True):
                    await self.bot.on_message(message)
            else:
                await interaction.response.send_message(f"message non trouvé",ephemeral=True)
        else:
            await interaction.response.send_message(f"vous n'avez pas le bon rôle",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Question(bot))