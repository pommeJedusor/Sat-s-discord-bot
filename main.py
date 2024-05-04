import discord, json, datetime
from discord.ext import commands
from datas.datas import Datas

from model import global_functions
from model import ModelPlayer

cogs = ["gems","items_owned","items","powers","tirage","arsmote","question","help"]

intents = discord.Intents.all()
bot=commands.Bot(command_prefix="!", intents=intents)
            
@bot.event
async def on_ready():
    try:
        for cog in cogs:
            await bot.load_extension(f"cogs.{cog}")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) }command(s)")
    except Exception as e:
        print(e)

    bot_channel = bot.get_channel(Datas.channel_message_bot)
    #check si y a des réponse à la question de la semaine et donne les gemmes correspondante si c'est le cas
    channel_question=bot.get_channel(Datas.channel_question)
    with open(Datas.question_file, "r") as f:
        line = f.readline()
        line=json.loads(line)
    async for message in channel_question.history(oldest_first=False):
        if message.id == line["message_id"]:
            last_question=message
            break
    async for message in channel_question.history(after=last_question,oldest_first=True):
        await on_message(message)

    #check si y a des reviews d'events
    channel_review=bot.get_channel(Datas.channel_review_events)
    is_find = True
    try:
        with open(Datas.review_events_file, "r") as f:
            line = f.readline()
            line=json.loads(line)
    except Exception as error:
        print("no review events init")
        with open(Datas.review_events_file, "w") as f:
           is_find=False 
    if is_find:
        async for message in channel_review.history(oldest_first=False):
            if message.id == line["message_id"]:
                last_review=message
                break
        async for message in channel_review.history(after=last_review,oldest_first=True):
            await on_message(message)

    #check si y a des nouveaux votes
    vote_channel = bot.get_channel(Datas.hosts_id)
    async for message in vote_channel.history(limit=1):
        message_vote=message
    for reaction in message_vote.reactions:
        async for user in reaction.users():
            if global_functions.votes(user,message_vote):
                await bot_channel.send(f"{user.name} a voté pour le host et gagné 1 gemme ")
    print("prêt")

@bot.tree.command(name="reload_cogs")
async def reload_cogs(interaction:discord.Interaction):
    await interaction.response.defer()
    for cog in cogs:
        await bot.unload_extension(f"cogs.{cog}")
    for cog in cogs:
        await bot.load_extension(f"cogs.{cog}")
    synced = await bot.tree.sync()
    await interaction.edit_original_response(content=f"{len(synced)} synchronisé")


@bot.event
async def on_raw_reaction_add(payload):
    channel=bot.get_channel(Datas.hosts_id)
    player=ModelPlayer.Player(payload.member.name,payload.user_id)
    player.is_player()
    if payload.message_id ==channel.last_message_id and not payload.message_id in player.votes:
        player.votes.append(payload.message_id)
        player.nb_gemmes+=1
        player.update_stats_player_fichier()
        bot_channel = bot.get_channel(Datas.channel_message_bot)
        await bot_channel.send(f"{payload.member.name} a voté pour le host et gagné 1 gemme ")

@bot.event
async def on_message(message):
    if message.channel.id == Datas.channel_question and not message.author.bot:
        with open(Datas.question_file,"r") as f:
            ligne = f.readline()
            if ligne:
                line=json.loads(ligne)
            else:
                line = {"nb_gemmes": 0, "id_users": [], "starttime": 0, "message_id": 0}

        if datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("@everyone")>=0 and global_functions.bon_role(message.author):
            #si y a le @everyone dans le message et bon_role
            args={"nb_gemmes":2,"id_users":[],"starttime":datetime.datetime.timestamp(message.created_at),"message_id":message.id}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))
            parameter_channel = bot.get_channel(Datas.channel_message_bot)
            await parameter_channel.send(f"la question de la semaine a été posée avec succès")

        elif datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("@everyone")==-1 and not line["id_users"]==False and not message.author.id in line['id_users']: 
            #si un joueur réponds à la question
            player=ModelPlayer.Player(message.author.name,message.author.id)
            player.is_player()
            player.nb_gemmes+=line['nb_gemmes']
            line['id_users'].append(message.author.id)
            with open(Datas.question_file,"w") as f:
                f.write(json.dumps(line))
            player.update_stats_player_fichier()
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"{message.author.name} a répondu à la question de la semaine et a gagné {line['nb_gemmes']} cristaux")

    #review events
    if message.channel.id == Datas.channel_review_events and not message.author.bot:
        with open(Datas.review_events_file,"r") as f:
            ligne = f.readline()
            if ligne:
                line=json.loads(ligne)
            else:
                line = {"nb_gemmes": 0, "id_users": [], "starttime": 0, "message_id": 0}

        if datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("<@&1159869065934934076>")>=0 and global_functions.bon_role(message.author):
            #si y a le @Prochain Host dans le message et bon_role
            args={"nb_gemmes":1,"id_users":[],"starttime":datetime.datetime.timestamp(message.created_at),"message_id":message.id}
            with open(Datas.review_events_file,'w') as f:
                f.write(json.dumps(args))
            parameter_channel = bot.get_channel(Datas.channel_message_bot)
            await parameter_channel.send(f"les reviews events ont été lancé avec succès")

        elif datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("<@&1159869065934934076>")==-1 and not line["id_users"]==False and not message.author.id in line['id_users'] and line['nb_gemmes']: 
            #si un joueur fournit une review de l'event
            player=ModelPlayer.Player(message.author.name,message.author.id)
            player.is_player()
            player.nb_gemmes+=line['nb_gemmes']
            line['id_users'].append(message.author.id)
            with open(Datas.review_events_file,"w") as f:
                f.write(json.dumps(line))
            player.update_stats_player_fichier()
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"{message.author.name} a fournit une reveiw de l'event et a gagné {line['nb_gemmes']} cristaux")


bot.run(Datas.bot_token)
