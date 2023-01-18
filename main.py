import discord, json, datetime
from discord.ext import commands
from datas.datas import Datas

import global_functions


intents = discord.Intents.all()
bot=commands.Bot(command_prefix="!", intents=intents)
            
@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.gems")
        await bot.load_extension("cogs.items_owned")
        await bot.load_extension("cogs.items")
        await bot.load_extension("cogs.powers")
        await bot.load_extension("cogs.tirage")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) }command(s)")
    except Exception as e:
        print(e)

    #check si y a des réponse à la question de la semaine et donne les gemmes correspondante si c'est le cas
    with open(Datas.question_file,"r") as f:
        line = json.loads(f.readline().replace("\n",""))
        channel_question=bot.get_channel(Datas.channel_question)
        async for message in channel_question.history(limit=100,oldest_first=True):
            if datetime.datetime.timestamp(message.created_at) > line["starttime"] and message.id != line["message_id"]:
                await on_message(message)

    #check si y a des nouveaux votes
    vote = bot.get_channel(Datas.hosts_id)
    async for pomme in vote.history(limit=1):
        poire=pomme
    for reaction in poire.reactions:
        async for user in reaction.users():
            global_functions.votes(user,poire)
    print("prêt")



@bot.event
async def on_raw_reaction_add(payload):
    channel=bot.get_channel(Datas.hosts_id)
    player=global_functions.Player(payload.member.name,payload.user_id)
    player.is_player()
    if payload.message_id ==channel.last_message_id and not payload.message_id in player.caracter[7]:
        player.caracter[7].append(payload.message_id)
        player.caracter[2]+=1
        player.update_stats_player_fichier()

@bot.event
async def on_message(message):
    with open(Datas.question_file,"r") as f:
        ligne = f.readline()
        if ligne:
            line=json.loads(ligne)
        else:
            line = {"id_users":["patate","poire",message.author.id]}
    if message.content.find("!question")==0 and global_functions.bon_role(message.author) and message.channel.id==Datas.channel_question:
        #si y a le !question dans le message et bon_role
        try:
            args=message.content.split(" ")
            args=args[1].split("_")
            args[0]=int(args[0])
            args[1]=int(args[1])*3600+int(str(datetime.datetime.timestamp(message.created_at)).split(".")[0])
            args={"nb_gemmes":args[0],"endtime":args[1],"id_users":[],"starttime":datetime.datetime.timestamp(message.created_at),"message_id":message.id}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))
        except:
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"<@{message.author.id}> erreur: le message doit absolument commencer par 'question A_B', A étant le nombre de gemmes et B le nombre d'heure, veuillez supprimer et renvoyer le message pour que cela puisse fonctionné")
    elif message.content.find("!question")==-1 and not message.author.id in line['id_users'] and int(str(datetime.datetime.timestamp(message.created_at)).split(".")[0])<line['endtime']: 
        player=global_functions.Player(message.author.name,message.author.id)
        player.is_player()
        player.caracter[2]+=line['nb_gemmes']
        line['id_users'].append(message.author.id)
        with open(Datas.question_file,"w") as f:
            f.write(json.dumps(line))
        player.update_stats_player_fichier()




bot.run(Datas.bot_token)