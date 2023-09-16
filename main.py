import discord, json, datetime
from discord.ext import commands
from datas.datas import Datas

import global_functions, dtb_funcs

cogs = ["gems","items_owned","items","powers","tirage","arsmote","question","help"]

intents = discord.Intents.all()
bot=commands.Bot(command_prefix="!", intents=intents)
            
@bot.event
async def on_ready():
    try:
        for cog in cogs:
            await bot.load_extension(f"cogs.{cog}")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)

    bot_channel = bot.get_channel(Datas.channel_message_bot)
    #check si y a des réponse à la question de la semaine et donne les gemmes correspondante si c'est le cas
    channel_question=bot.get_channel(Datas.channel_question)
    question = dtb_funcs.get_question()
    async for message in channel_question.history(oldest_first=False):
        if not question or message.id == question[2]:
            last_question=message
            break
    async for message in channel_question.history(after=last_question,oldest_first=True):
        await on_message(message)

    #check si y a des nouveaux votes
    vote_channel = bot.get_channel(Datas.hosts_id)
    host = dtb_funcs.get_host()
    async for message in vote_channel.history(limit=5,oldest_first=False):
        host_message = message
        if host and host[1]==message.id:
            break

    if not host:
        dtb_funcs.add_host(host_message.id)
    else:
        dtb_funcs.edit_host(host_message.id)

    async for message in vote_channel.history(after=host_message,oldest_first=True):
        for reaction in message.reactions:
            async for user in reaction.users():
                if global_functions.votes(user,message):
                    await bot_channel.send(f"{user.name} a voté pour le host et gagné 1 gemme ")
        dtb_funcs.edit_host(message.id)

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
    if payload.message_id == channel.last_message_id and not payload.message_id == player.last_vote:
        player.last_vote = payload.message_id
        player.nb_gemmes+=1
        player.update_stats_player()
        bot_channel = bot.get_channel(Datas.channel_message_bot)
        await bot_channel.send(f"{payload.member.name} a voté pour le host et gagné 1 gemme ")

@bot.event
async def on_message(message):
    if message.channel.id == Datas.channel_question and not message.author.bot:
        question = dtb_funcs.get_question()
        player=global_functions.Player(message.author.name,message.author.id)
        player.is_player()

        #si y a le @everyone dans le message et bon_role
        if message.content.find("@everyone")>=0 and global_functions.bon_role(message.author):
            dtb_funcs.add_question(message_id=message.id,reward=2)
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"la question de la semaine a été posée avec succès")

        #si un joueur réponds à la question
        elif question and not player.last_question_answerd==question[2]:
            player.nb_gemmes+=question[1]
            player.last_question_answerd = question[2]
            player.update_stats_player()
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"{message.author.name} a répondu à la question de la semaine et a gagné {question[1]} cristaux")

    elif message.channel.id == Datas.hosts_id:
        dtb_funcs.edit_host(message.id)



bot.run(Datas.bot_token)