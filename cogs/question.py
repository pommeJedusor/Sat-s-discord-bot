from discord import app_commands
from discord.ext import commands
import discord
import datetime

from model import global_functions
from model import ModelPlayer

import json

from datas.datas import Datas

PROPOSITON_QUESTION_FILE = "datas/datas_propositions_questions.txt"
PAST_PROPOSITON_QUESTION_FILE = "datas/datas_past_propositions_questions.txt"

BOT = None

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    #modos
    @app_commands.choices(questions=[
    app_commands.Choice(name="questions", value=1),
    app_commands.Choice(name="review-events", value=0),
    ])
    @app_commands.command(name="recompense_question_semaine", description="choisir le nombre de gemmes de récompense par défaut 2")
    async def reward_question_semaine(self,interaction:discord.Interaction,gemmes:int, questions:app_commands.Choice[int]=None):
        await interaction.response.defer()
        #check si modo
        if not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle")
            return 0
        
        print(questions)
        if not questions or questions.value:
            file = Datas.question_file
        else:
            file = Datas.review_events_file
        with open(file,"r") as f:
            ligne = f.readline()
            if ligne:
                line=json.loads(ligne)
            else:
                line = {"nb_gemmes": 0, "id_users": [], "starttime": 0, "message_id": 0}
        dif_gems = gemmes - line["nb_gemmes"]
        line["nb_gemmes"] = gemmes
        with open(file, "w") as f:
            f.write(json.dumps(line))

        #fonctionnemnt rétroactif
        for id_user in line["id_users"]:
            user = self.bot.get_user(id_user)
            player = ModelPlayer.Player(user.name,user.id)
            player.is_player()
            player.nb_gemmes+=dif_gems
            player.update_stats_player_fichier()

        await interaction.edit_original_response(content=f"la récompense est désormais de {gemmes}")

    @app_commands.choices(questions=[
    app_commands.Choice(name="questions", value=1),
    app_commands.Choice(name="review-events", value=0),
    ])
    @app_commands.command(name="oubli_question", description="si mention ajouté à la queston de la semaine par edit")
    async def oubli_question(self,interaction:discord.Interaction,gemmes:int,énième_message:int=None,message_id:str=None, questions:app_commands.Choice[int]=None):
        if not questions or questions.value:
            channel=self.bot.get_channel(Datas.channel_question)
            file = Datas.question_file
        else:
            channel=self.bot.get_channel(Datas.channel_review_events)
            file = Datas.review_events_file
        await interaction.response.defer(ephemeral=True)
        try:
            if message_id:
                message_id = int(message_id)
        except:
            await interaction.edit_original_response(content=f"entrez un nombre valide")
            return 0
        right_message = None
        if not global_functions.bon_role(interaction.user):
            await interaction.edit_original_response(content=f"vous n'avez pas le bon rôle")
            return 0
        elif (énième_message and message_id):
            await interaction.edit_original_response(content=f"vous ne pouvez pas choisir 'énèime message' et 'message id' en même temps")
            return 0
        elif not (énième_message or message_id):
            await interaction.edit_original_response(content=f"vous devez choisir 'énième message' 'ou message_id'")
            return 0
        elif message_id:
            async for message in channel.history(oldest_first=False):
                if message.id==message_id:
                    right_message = message
                    break
        elif énième_message:
            async for message in channel.history(oldest_first=False,limit=énième_message):
                right_message = message
        if right_message:
            args={"nb_gemmes":gemmes,"id_users":[],"starttime":datetime.datetime.timestamp(right_message.created_at),"message_id":right_message.id}
            with open(file,'w') as f:
                f.write(json.dumps(args))
            if questions:
                await interaction.edit_original_response(content=f"la question de {right_message.author} a été posée avec succès\nl'id: {right_message.id}\n<@718805832652816486> faut redémarrer le bot")
            else:
                await interaction.edit_original_response(content=f"les reviews events ont été lancé par {right_message.author} avec succès\nl'id: {right_message.id}\n<@718805832652816486> faut redémarrer le bot")
        else:
            await interaction.edit_original_response(content=f"le message n'as pas été trouvé")

    @app_commands.command(name="question_vote", description="permet de voter pour une proposition de question")
    async def question_vote(self,interaction:discord.Interaction,question_number: int):
        await interaction.response.defer(ephemeral=True)
        if global_functions.bon_role(interaction.user, animateur=True):
            with open(PROPOSITON_QUESTION_FILE,"r") as f:
                compteur = 1
                text=""
                exist=False
                for line in f:
                    line=json.loads(line)
                    if compteur==question_number:
                        if interaction.user.id in line[3]:
                            await interaction.edit_original_response(content="vous avez déjà voté pour cette question")
                            return
                        line[2]+=1
                        line[3].append(interaction.user.id)
                        exist=True
                    text+=json.dumps(line)+"\n"
                    compteur+=1
            with open(PROPOSITON_QUESTION_FILE,"w") as f:
                f.write(text)
            
            if not exist:
                await interaction.edit_original_response(content="question non trouvé, veuillez vérifier le nombre de la question entrée")
            else:
                await interaction.edit_original_response(content="vote ajouté avec succès")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon rôle")

    @app_commands.command(name="recompense_question", description="permet de supprimer la question et de récompenser le joueur")
    async def recompense_question(self,interaction:discord.Interaction,question_number: int,gems_number_reward: int):
        await interaction.response.defer(ephemeral=True)
        if global_functions.bon_role(interaction.user):
            with open(PROPOSITON_QUESTION_FILE,"r") as f:
                compteur = 0
                final_line=False
                text=""
                for line in f:
                    compteur+=1
                    line=json.loads(line)
                    line[2]=0
                    if compteur==question_number:
                        final_line = line
                        continue
                    text+=json.dumps(line)+"\n"
            if final_line:
                with open(PROPOSITON_QUESTION_FILE,"w") as f:
                    f.write(text)
                with open(PAST_PROPOSITON_QUESTION_FILE,"a") as f:
                    f.write(json.dumps(line)+"\n")

                player = ModelPlayer.Player("pomme",final_line[0])
                player.is_player()
                player.nb_gemmes+=gems_number_reward
                player.update_stats_player_fichier()
                await interaction.edit_original_response(content="recompense distribué avec succès")
            else:
                await interaction.edit_original_response(content="question non trouvé veuillez vérifier le nombre de la question")
        else:
            await interaction.edit_original_response(content="vous n'avez pas le bon rôle")

    #players
    @app_commands.command(name="proposition_question", description="permet de proposer une question pour la question de la semaine")
    async def proposition_question(self,interaction:discord.Interaction):
        await interaction.response.send_modal(QuestionModal())

    @app_commands.command(name="voir_les_questions", description="permet de voir les question proposé par les joueurs")
    async def voir_les_questions(self,interaction:discord.Interaction):
        global BOT
        await interaction.response.defer()
        data = []

        with open(PROPOSITON_QUESTION_FILE, 'r') as f:
            compteur = 1
            for line in f:
                line = json.loads(line)
                user = await BOT.fetch_user(line[0])
                username = user.name
                data.append({"number":f"{compteur})","question":line[1],"votes":line[2],"user":username})
                compteur+=1

        pagination_view = PaginationView(timeout=None)
        pagination_view.data = data
        await pagination_view.send(interaction)

    @app_commands.command(name="voir_les_questions_supprimées", description="permet de voir les question proposé supprimées")
    async def voir_les_questions_supprimer(self,interaction:discord.Interaction):
        global BOT
        await interaction.response.defer()
        data = []

        with open(PAST_PROPOSITON_QUESTION_FILE, 'r') as f:
            compteur = 1
            for line in f:
                line = json.loads(line)
                user = await BOT.fetch_user(line[0])
                username = user.name
                data.append({"number":f"{compteur})","question":line[1],"votes":line[2],"user":username})
                compteur+=1

        pagination_view = PaginationViewDelete(timeout=None)
        pagination_view.data = data
        await pagination_view.send(interaction)
            
class QuestionModal(discord.ui.Modal, title="proposition_question"):
    proposition_question = discord.ui.TextInput(label="proposition_question",style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        proposition_question2 = [interaction.user.id,self.proposition_question.value,0,[]]
        for p in proposition_question2:
            print(p)
        with open(PROPOSITON_QUESTION_FILE,"a") as f:
            f.write(json.dumps(proposition_question2)+"\n")
        await interaction.response.send_message(f"proposition_question envoyé",ephemeral=True)


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 5

    async def send(self, interaction):
        self.message = await interaction.edit_original_response(view=self)
        await self.update_message(interaction, self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title=f"liste des questions {self.current_page} / {int(len(self.data) / self.sep) + 1}:")
        for item in data:
            embed.add_field(name=item['number'], value=f"{item['question']}\nvotes: {item['votes']}\nuser: {item['user']}", inline=False)
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

class PaginationViewDelete(PaginationView):
    def create_embed(self, data):
        embed = discord.Embed(title=f"liste des questions supprimées {self.current_page} / {int(len(self.data) / self.sep) + 1}:")
        for item in data:
            embed.add_field(name=item['number'], value=f"{item['question']}\nuser: {item['user']}", inline=False)
        return embed

async def setup(bot):
    global BOT
    BOT = bot
    await bot.add_cog(Question(bot))