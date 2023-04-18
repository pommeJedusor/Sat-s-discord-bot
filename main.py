import discord, json, datetime
from discord.ext import commands
from datas.datas import Datas

import global_functions

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

    #check si y a des nouveaux votes
    vote = bot.get_channel(Datas.hosts_id)
    async for pomme in vote.history(limit=1):
        poire=pomme
    for reaction in poire.reactions:
        async for user in reaction.users():
            if global_functions.votes(user,poire):
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
    player=global_functions.Player(payload.member.name,payload.user_id)
    player.is_player()
    if payload.message_id ==channel.last_message_id and not payload.message_id in player.caracter[7]:
        player.caracter[7].append(payload.message_id)
        player.caracter[2]+=1
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


        if datetime.datetime.timestamp(message.created_at)>line["starttime"] and line["id_users"]==False and line["message_id"]==message.author.id:
            #si question a initié et modo posant la question l'initie
            args={"nb_gemmes":line["nb_gemmes"],"id_users":[],"starttime":datetime.datetime.timestamp(message.created_at),"message_id":message.id}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))
            #envoy le message de validation
            parameter_channel = bot.get_channel(Datas.channel_message_bot)
            await parameter_channel.send(f"<@{message.author.id}>la question de la semaine a été posée avec succès")
        
        elif datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("!question")==0 and global_functions.bon_role(message.author):
            #si y a le !question dans le message et bon_role
            args=message.content.split(" ")
            args[1]=int(args[1])
            args={"nb_gemmes":args[1],"id_users":[],"starttime":datetime.datetime.timestamp(message.created_at),"message_id":message.id}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))

        elif datetime.datetime.timestamp(message.created_at)>line["starttime"] and message.content.find("!question")==-1 and not line["id_users"]==False and not message.author.id in line['id_users']: 
            #si un joueur réponds à la question
            player=global_functions.Player(message.author.name,message.author.id)
            player.is_player()
            player.caracter[2]+=line['nb_gemmes']
            line['id_users'].append(message.author.id)
            with open(Datas.question_file,"w") as f:
                f.write(json.dumps(line))
            player.update_stats_player_fichier()
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"{message.author.name} a répondu à la question de la semaine et a gagné {line['nb_gemmes']} cristaux")




bot.run(Datas.bot_token)