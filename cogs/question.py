from discord import app_commands
from discord.ext import commands
import discord
import datetime

import global_functions
import json

from datas.datas import Datas

import random

PROPOSITON_QUESTION_FILE = "datas/datas_propositions_questions"

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    #modos
    @app_commands.command(name="recompense_question_semaine", description="choisir le nombre de gemmes de récompense par défaut 2")
    async def reward_question_semaine(self,interaction:discord.Interaction,gemmes:int):
        await interaction.response.defer()
        #check si modo
        if not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle")
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
            player.nb_gemmes+=dif_gems
            player.update_stats_player_fichier()

        await interaction.edit_original_response(content=f"la récompense est désormais de {gemmes}")

    @app_commands.command(name="oubli_question", description="si mention ajouté à la queston de la semaine par edit")
    async def oubli_question(self,interaction:discord.Interaction,gemmes:int,énième_message:int=None,message_id:str=None):
        await interaction.response.defer()
        try:
            if message_id:
                message_id = int(message_id)
        except:
            await interaction.edit_original_response(content=f"entrez un nombre valide",ephemeral=True)
            return 0
        right_message = None
        channel_question=self.bot.get_channel(Datas.channel_question)
        if not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle",ephemeral=True)
            return 0
        elif (énième_message and message_id):
            await interaction.edit_original_response(content=f"vous ne pouvez pas choisir 'énèime message' et 'message id' en même temps",ephemeral=True)
            return 0
        elif not (énième_message or message_id):
            await interaction.edit_original_response(content=f"vous devez choisir 'énième message' 'ou message_id'",ephemeral=True)
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
            await interaction.edit_original_response(content=f"la question de {right_message.author} a été posée avec succès\nl'id: {right_message.id}\n<@718805832652816486> faut redémarrer le bot")
        else:
            await interaction.edit_original_response(content=f"le message n'as pas été trouvé")

    @app_commands.command(name="voir_les_questions", description="permet de voir les question proposé par les joueurs")
    async def voir_les_questions(self,interaction:discord.Interaction):
        data = [

        ]

        for i in range(1,15):
            data.append({
                "number": f"{i})",
                "question": f"une question potentiellement intéressante mais potentiellement pas",
                "votes": random.randint(1,5)
            })

        pagination_view = PaginationView(timeout=None)
        pagination_view.data = data
        await pagination_view.send(interaction)

    #players
    @app_commands.command(name="proposition_question", description="permet de proposer une question pour la question de la semaine")
    async def proposition_question(self,interaction:discord.Interaction):
        await interaction.response.send_modal(QuestionModal())
            
class QuestionModal(discord.ui.Modal, title="proposition_question"):
    proposition_question = discord.ui.TextInput(label="proposition_question",style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        proposition_question2 = [interaction.user.id,self.proposition_question.value,0]
        for p in proposition_question2:
            print(p)
        with open(PROPOSITON_QUESTION_FILE,"a") as f:
            f.write(json.dumps(proposition_question2)+"\n")
        await interaction.response.send_message(f"proposition_question envoyé",ephemeral=True)


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 5

    async def send(self, interaction):
        self.message = await interaction.response.send_message(view=self)
        await self.update_message(interaction, self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"liste des questions {self.current_page} / {int(len(self.data) / self.sep) + 1}:")
        for item in data:
            embed.add_field(name=item['number'], value=f"{item['question']}\nvotes: {item['votes']}", inline=False)
        return embed

    async def update_message(self,interaction: discord.Interaction,data):
        self.update_buttons()
        await interaction.edit_original_response(embed=self.create_embed(data),view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<",
                       style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(interaction, self.get_current_page_data())

    @discord.ui.button(label="<",
                       style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(interaction, self.get_current_page_data())

    @discord.ui.button(label=">",
                       style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(interaction, self.get_current_page_data())

    @discord.ui.button(label=">|",
                       style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        await self.update_message(interaction, self.get_current_page_data())

async def setup(bot):
    await bot.add_cog(Question(bot))