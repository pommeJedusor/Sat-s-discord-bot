from discord import app_commands
from discord.ext import commands
import discord

import json, time

from datas.datas import Datas

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @app_commands.command(name="question", description="à faire juste avant de poser la question de la semaine")
    async def question(self,interaction:discord.Interaction,gemmes:int):
        with open(Datas.question_file,"w") as f:
            f.write(json.dumps({"nb_gemmes": gemmes, "id_users": False, "starttime": time.time(), "message_id": interaction.user.id}))
        await interaction.response.send_message(f"c'est fait",ephemeral=True)

async def setup(bot):
    await bot.add_cog(Question(bot))