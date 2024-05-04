import random, time, discord, json, asyncio
from discord.ext import commands
from discord import app_commands
from datas import Datas
from typing import Optional

def tirage(file,stars=None):
    is_exist=False
    with open(file,'r') as f:
        pomme=0
        for line in f:
            line=json.loads(line)
            if not stars or line[1]==stars:
                if line[2]!=0 and line[5]==True:
                    pomme+=line[2]
                    is_exist=True
    if is_exist:
        result = random.randint(1,pomme)
        with open(file,'r') as f:
            fined=False
            for line in f:
                line=json.loads(line)
                if not stars or line[1]==stars:
                    if line[2]!=0 and line[5]==True:
                        result-=line[2]
                        if result<=0 and not fined:
                            final_result={"name":line[0],"stars":line[1]}
                            fined=True
        return final_result
    else:
        return False
        


def update(self,file,num_param):
        """fichier, numero du parametre dans le fichier,actualise les données"""
        with open(file,"r") as f:
            text=""
            exist=False
            for line in f:
                line=json.loads(line)
                if line[num_param]==self.caracter[num_param]:
                    line=self.caracter
                    exist=True
                text+=json.dumps(line)+"\n"
        with open(file,"w") as f:
            f.write(text)
        if exist:
            return True
        else:
            return False
def add_line(self,file):
    """ajoute au fichier la ligne correspondant au self.caracter"""
    with open(file,"a") as f:
        f.write(json.dumps(self.caracter)+"\n")
def delete_line(self):
    """supprime du fichier la ligne correspondante à l'instance"""
    with open(self.file,"r") as f:
        text=""
        for line in f:
            if not json.loads(line)==self.caracter:
                text+=line
    with open(self.file,"w") as f:
        f.write(text)

def bon_role(user):
    for r in user.roles:
        if r.id in Datas.role_modo:
            return True

def votes(user,message):
    channel=bot.get_channel(Datas.hosts_id)
    player=Player(user.name,user.id)
    player.is_player()
    if not message.id in player.caracter[7]:
        player.caracter[7].append(message.id)
        player.caracter[2]+=1
        player.update_stats_player_fichier()

class Player:
    def __init__(self,name,id,nb_gemmes=0 ,gemmes_spend=0,items=[],salon=1040228357981343764,pity=[0,0,10,50],votes=[],powers=[],historique=[],yato_tirages=0):
        self.caracter=[name,id,nb_gemmes,gemmes_spend,items,salon,pity,votes,powers,historique,yato_tirages]
        self.file=Datas.player_file
    def update_stats_player_fichier(self):
        """actualise le fichier avec les données actuels de l'instance"""
        return update(self,self.file,1)
    def is_player(self):
        """
        vérifie l'occurence dans la base de donnés à partir de l'id si oui actualise les données de l'instance sinon le rajoute dans le fichier avec les données actuels de l'instance
        """
        with open(self.file,"r") as f:
            for line in f:
                line=json.loads(line)
                if line[1]==self.caracter[1]:
                    self.caracter = line
                    return True
        if not self.update_stats_player_fichier():
            add_line(self,self.file)
            return False
    def spend_gems(self,nb):
        """dépense les gemmes d'un joueur"""
        if self.caracter[2]>nb>0:
            self.caracter[2]-=nb
            self.caracter[3]+=nb
            self.update_stats_player_fichier
            return True
        else:
            return False
        
    def lose_item(self,item_id,nb):
        pomme=True
        item=Items("pomme",id=item_id)
        if item.is_item(x=6):
            x=0
            for item2 in self.caracter[4]:
                if item2['id']==item.caracter[6] and pomme and item2['nb']>nb:
                    item2['nb']-=nb
                    pomme=False
                elif item2['id']==item.caracter[6] and pomme and item2['nb']==nb:
                    del self.caracter[4][x]
                    power = lambda pow:pow["id"]==item2["id"]
                    powers = list(filter(power,self.caracter[8]))
                    print(powers)
                    pomme=0
                    if powers:
                        for i in range(len(self.caracter[8])):
                            print(powers[0])
                            print(self.caracter[8][i]["id"])
                            if self.caracter[8][i]["id"] == powers[0]["id"]:
                                print("yop")
                                pomme=i+1
                        if pomme:
                            del self.caracter[8][pomme-1]
                    pomme=False
                x+=1
        self.update_stats_player_fichier()
        if pomme:
            return False
        else:
            return True


    def add_item(self,items):
        """ajoute les items au joueur"""
        x=0
        for item in items:
            pomme=True
            is_item=Items("pomme",id=item['id'])
            for item2 in self.caracter[4]:
                if is_item.is_item(x=6) and (is_item.caracter[6]) == item2['id'] and pomme:
                    self.caracter[4][x]['nb']+=item["nb"]
                    pomme=False
                x+=1
            if pomme==True:
                self.caracter[4].append({"id":is_item.caracter[6],"nb":item["nb"]})
                pomme=False
                if is_item.caracter[6]==Datas.panda_id:
                    if not {"id":Datas.panda_id,"active":True} in self.caracter[8] or not {"id":Datas.panda_id,"active":False} in self.caracter[8]:
                        self.caracter[8].append({"id":Datas.panda_id,"active":True})
                elif is_item.caracter[6]==Datas.arsmote_id:
                    if not {"id":Datas.arsmote_id,"active":True} in self.caracter[8] or not {"id":Datas.arsmote_id,"active":False} in self.caracter[8]:
                        self.caracter[8].append({"id":Datas.arsmote_id,"active":True})
                elif is_item.caracter[6]==Datas.Yato_id:
                    if not {"id":Datas.Yato_id,"active":True} in self.caracter[8] or not {"id":Datas.Yato_id,"active":False} in self.caracter[8]:
                        self.caracter[8].append({"id":Datas.Yato_id,"active":True})
        self.update_stats_player_fichier()
    def tirages(self,nb_tirage,tirage_4=False):
        files=Datas.items_file
        all_items=[]
        for i in range(nb_tirage):
            result=None
            if tirage_4==False:
                if self.caracter[6][1]+1>=self.caracter[6][3]:
                    result =tirage(files,5)
                elif self.caracter[6][0]+1>=self.caracter[6][2]:
                    result = tirage(files,4)
                else:
                    result = tirage(files)
                if result and result['stars'] == 5:
                    self.caracter[6][1]=0
                    self.caracter[6][3]=50
                    self.caracter[6][0]+=1
                    self.spend_gems(1)
                elif result and result['stars'] == 4:
                    self.caracter[6][0]=0
                    self.caracter[6][2]=10
                    self.caracter[6][1]+=1
                    self.spend_gems(1)
                elif result:
                    self.caracter[6][0]+=1
                    self.caracter[6][1]+=1
                    self.spend_gems(1)
            else:
                result= tirage(files,4)
            if result:
                new_item=Items(result['name'])
                new_item.is_item()
                if new_item.caracter[6] == Datas.panda_id or Datas.arsmote_id:
                    if not {"id":new_item.caracter[6],"active":True} in self.caracter[8] and not {"id":new_item.caracter[6],"active":False} in self.caracter[8]:
                        self.caracter[8].append({"id":new_item.caracter[6],"active":True})
                self.add_item([{"id":new_item.caracter[6],"nb":1}])
                all_items.append(new_item)
        self.caracter[9]=[]
        for item in all_items:
            self.caracter[9].append(item.caracter[6])
        self.update_stats_player_fichier()
        return all_items
class Items:
    def __init__(self,name,stars=0,drop=0,url_img="",effects=[],on_tirage=True,id=random.randint(1,1000000000)):
        self.caracter=[name,stars,drop,url_img,effects,on_tirage,id]
        self.file=Datas.items_file
    def is_item(self,x=0):
        """vérifie si l'item existe renvoi et le retourne"""
        with open(self.file,"r") as f:
            for line in f:
                line=json.loads(line)
                if line[x]==self.caracter[x]:
                    self.caracter = line
                    return True
            return False
    def update_item(self):
        """actualise le fichier avec les données actuels de l'instance"""
        return update(self,self.file,6)
    def add_item(self):
        """ajoute l'item au fichier retourne faux si il existe déja"""
        if self.is_item():
            return False
        else:
            with open(self.file,"a") as f:
                f.write(json.dumps(self.caracter)+"\n")
                return True
    def delete_item(self):
        """supprime l'item du fichier si il existe"""
        if not self.is_item():
            return False
        else:
            delete_line(self)

            


intents = discord.Intents.all()
bot=commands.Bot(command_prefix="!", intents=intents)
            
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced) }command(s)")
    except Exception as e:
        print(e)

    #check si y a des réponse à la question de la semaine et donne les gemmes correspondante si c'est le cas
    channel_question=bot.get_channel(Datas.channel_question)
    pomme=True
    async for message in channel_question.history(limit=20,oldest_first=False):
        if pomme and message.content.find("!question")==-1:
            await on_message(message)
        else:
            pomme=False

    #check si y a des nouveaux votes
    vote = bot.get_channel(Datas.hosts_id)
    async for pomme in vote.history(limit=1):
        poire=pomme
    for reaction in poire.reactions:
        async for user in reaction.users():
            votes(user,poire)
    print("prêt")



@bot.tree.command(name="add_gems",description="permet à un modo d'ajouter à un joueur un nombre de gemmes choisis par l'éxécutant de la commande")
async def add_gems(interaction: discord.Interaction, nombre_de_gemmes: int, user: discord.Member):
    if bon_role(interaction.user) and nombre_de_gemmes>0:
        player = Player(user.name,user.id)
        player.is_player()
        player.caracter[2]+=nombre_de_gemmes
        player.update_stats_player_fichier()
        await interaction.response.send_message(f"les {nombre_de_gemmes} gemme(s) ont bien été ajoués à {user.name} ")
    elif nombre_de_gemmes==0:
        await interaction.response.send_message("euh.... ???? vous êtes sûr??? bon ... bah ... c'est fait.. je suppose???")
    elif nombre_de_gemmes<0:
        await interaction.response.send_message("les nombres nuls ou négatifs ne sont pas accepter veuillez utiliser la commande '/destroy_gems' ou son homologue '\spend_gems'")
    else:
        await interaction.response.send_message("vous n'avez pas le bon rôle")

@bot.tree.command(name="see_gems",description="permet de voir son nombre de gemmes possédés et dépensé ")
async def see_gems(interaction : discord.Interaction):
    player = Player(interaction.user.name,interaction.user.id)
    player.is_player()
    await interaction.response.send_message(f"vous possédez {player.caracter[2]} gemmes \n vous avez dépensez un total de {player.caracter[3]} gemmes ")

@bot.tree.command(name="see_gems_of_a_player",description="permet à un modo de voir les gemmes d'un joueur")
async def see_gems_of_a_player(interaction : discord.Interaction, user : discord.Member):
    if bon_role(interaction.user):
        player = Player(user.name,user.id)
        player.is_player()
        await interaction.response.send_message(f"{user.name} possede {player.caracter[2]} gemmes \n et a dépensé un total de {player.caracter[3]} gemmes ")
    else:
        await interaction.response.send_message(f"vous n'avez pas le bon rôle")

@bot.tree.command(name="create_item",description="permet à un modo de creer un item")
async def create_item(interaction:discord.Interaction,name:str,nombre_d_étoiles:int,indice_drop:int,img_link:str):
    item=Items(name,nombre_d_étoiles,indice_drop,img_link,id=random.randint(1,1000000000))
    if not item.is_item() and bon_role(interaction.user):
        if item.add_item():
            await interaction.response.send_message(f"l'item {name} {nombre_d_étoiles} étoiles avec un indice de drop {indice_drop} a bien été rajouté à la base de donnés")
        else:
            await interaction.response.send_message("l'ajout de l'item a échoué pour des raisons inconnus")
    elif not bon_role(interaction.user):
        await interaction.response.send_message("vous n'avez pas le bon role")
    else:
        await interaction.response.send_message(f"l'item {name} existe déja")

@bot.tree.command(name="edit_item",description="permet à un modo de modifier un item")
async def edit_item(interaction:discord.Interaction,name:str,nombre_d_étoiles:Optional[int],indice_drop:Optional[int],image_link:Optional[str],effets:Optional[str],tirage_active:Optional[bool],new_name:Optional[str]):
    item=Items(name)
    if item.is_item() and bon_role(interaction.user):
        item.caracter[0]=name
        message=f"l'item {name} a bien été modifié, et à comme caractéristique:\n"
        if new_name is not None:
            new_item=Items(new_name)
            if not new_item.is_item():
                item.caracter[0]=new_name
                message=f"l'item {name} ({new_name} maintenant) a bien été modifié, et à comme caractéristique:\n"
        if nombre_d_étoiles is not None:
            item.caracter[1]=nombre_d_étoiles
            message+=f"étoiles: {nombre_d_étoiles}\n"
        if indice_drop is not None:
            item.caracter[2]=indice_drop
            message+=f"indice de drop: {indice_drop}\n"
        if image_link is not None:
            item.caracter[3]=image_link
            message+=f"lien pour l'image: {image_link}\n"
        if effets is not None:
            effets=effets.split(",")
            item.caracter[4]=effets
            message+=f"effets: {effets}\n"
        if tirage_active is not None:
            item.caracter[5]=tirage_active
            if tirage_active:
                message+=f"est dans les tirages: oui\n"
            else:
                message+=f"est dans les tirages: non\n"
        item.update_item()
        await interaction.response.send_message(message)
    elif not bon_role(interaction.user):
        await interaction.response.send_message(f"vous n'avez pas le bon rôle ")
    else:
        await interaction.response.send_message(f"l'item {name} n'as pas été trouvé ")

@bot.tree.command(name="see_all_items",description="permet de voir tous les items")
async def see_all_items(interaction:discord.Interaction,stars:int=None,active:bool=None,drop:int=None):

    stars_filter = lambda ligne: stars==None or ligne[1]==stars
    active_filter = lambda ligne: active==None or ligne[5]==active
    drop_filter = lambda ligne: drop==None or ligne[2]==drop

    items=""
    lignes=[]
    with open(Datas.items_file,'r')as f:
        for ligne in f:
            ligne=json.loads(ligne)
            lignes.append(ligne)

    lignes = list(filter(active_filter,lignes))
    lignes = list(filter(stars_filter,lignes))
    lignes = list(filter(drop_filter,lignes))

    for ligne in lignes:
        items+=f"nom: {ligne[0]}, {ligne[1]} étoiles, drop:{ligne[2]}, effets:{ligne[4]}"
        if ligne[5]:
            items+=", est présent dans les tirages \n"
        else:
            items+=", est absent des tirages \n"
    await interaction.response.send_message(items)

@bot.tree.command(name="add_item_to_a_player",description="permet à un modo d'ajouter un item à un joueur")
async def add_item_to_a_player(interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
    if bon_role(interaction.user):
        player=Player(user.name,user.id)
        player.is_player()
        item=Items(name)
        if item.is_item() and nombre>0:
            player.add_item([{"id":item.caracter[6],"nb":nombre}])
            await interaction.response.send_message(f"l'item {name} a bien été ajouté à {user.name} en quantité de {nombre} ")
        elif not item.is_item():
            await interaction.response.send_message(f"{name} n'as pas été trouvé")
        else:
            await interaction.response.send_message(f"vous ne pouvez ajouter qu'un nombre positif d'objets à un joueur")
    else:
        await interaction.response.send_message(f"vous n'avez pas le bon role")

@bot.tree.command(name="remove_item_from_a_player",description="permet à un modo de retirer un item à un joueur")
async def remove_item_from_a_player(interaction:discord.Interaction,user:discord.Member,name:str,nombre:int=1):
    if bon_role(interaction.user):
        player=Player(user.name,user.id)
        player.is_player()
        item=Items(name)
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



@bot.tree.command(name="see_items",description="permet de voir ses items")
async def see_items(interaction:discord.Interaction):
    player = Player(interaction.user.name,interaction.user.id)
    player.is_player()
    text=""
    for item in player.caracter[4]:
        iteme=Items("pomme",id=item['id'])
        iteme.is_item(x=6)
        text+=f"{iteme.caracter[0]}: nombre:{item['nb']} \n"
    if not text:
        text="malheureusement vous ne possédez aucun item, n'hésitez pas à faire des tirages pour en avoir "
    await interaction.response.send_message(text)

@bot.tree.command(name="see_items_of_a_player",description="permet à un modo de voir les items d'un joueur")
async def see_items_of_a_player(interaction:discord.Interaction, user:discord.Member):
    if bon_role(interaction.user):
        player = Player(user.name,user.id)
        player.is_player()
        text=""
        for item in player.caracter[4]:
            iteme=Items("pomme",id=item['id'])
            iteme.is_item(x=6)
            text+=f"{iteme.caracter[0]}: nombre:{item['nb']} \n"
        if text:
            await interaction.response.send_message(text)
        else:
            await interaction.response.send_message("ce joueur n'as pas d'items")
    else:
        await interaction.response.send_message("vous n'avez pas le bon role")

@bot.tree.command(name="spend_gems",description="permet de dépenser les gemmes d'un joueur")
@app_commands.describe(depenser="True pour enlever les gemmes et augmenter 'les gemmes dépenser', False pour juste les enlever")
async def spend_gems(interaction:discord.Interaction,user:discord.Member,nombres_de_gemmes:int,depenser:bool=False):
    player=Player(user.name,user.id)
    player.is_player()
    if bon_role(interaction.user) and player.caracter[2]>=nombres_de_gemmes>0:
        player.caracter[2]-=nombres_de_gemmes
        if depenser:
            player.caracter[3]+=nombres_de_gemmes
        player.update_stats_player_fichier()
        await interaction.response.send_message(f"les {nombres_de_gemmes} gemmes de {user.name} ont bien été dépensé qui a maintenant {player.caracter[2]} gemmes ")
    elif not bon_role(interaction.user):
        await interaction.response.send_message("vous n'avez pas le bon role")
    elif not nombres_de_gemmes>0:
        await interaction.response.send_message("ous ne pouvez pas retirer un nombre nul ou négatif de gemmes user de la commande '/add_gems' pour cette effet")
    else:
        await interaction.response.send_message(f"vous ne pouvez pas retirer {nombres_de_gemmes} gemmes à un joueur qui en a moins ({player.caracter[2]}) ")
    
@bot.tree.command(name="tirage",description="permet de faire des tirages")
async def tirages(interaction:discord.Interaction,nombre_de_tirage:int):
    player = Player(interaction.user.id,interaction.user.id)
    player.is_player()
    channel_perso=bot.get_channel(player.caracter[5])
    if player.caracter[2]>=nombre_de_tirage and nombre_de_tirage<=10:
        await interaction.response.send_message(f"vous avez obtenus...")
        if nombre_de_tirage>player.caracter[10]:
            poire=player.caracter[10]
        else:
            poire=nombre_de_tirage
        patate=0
        for i in range(poire):
            if random.randint(1,5)==4:
                patate+=1
                nombre_de_tirage-=1
                player.caracter[1]+=2
                player.caracter[2]-=1
                player.caracter[3]+=1
            player.caracter[10]-=1
        for i in range(patate):
            await channel_perso.send("vous avez gagné 2 gemmes")
            if not interaction.channel==channel_perso:
                await interaction.channel.send("vous avez gagné 2 gemmes")
            await asyncio.sleep(2)
        player.update_stats_player_fichier()
        for i in player.tirages(nombre_de_tirage):
            i.is_item()
            await asyncio.sleep(i.caracter[1])
            if player.caracter[5]!=1040228357981343764:
                await channel_perso.send(f"{i.caracter[0]} : {i.caracter[1]} étoiles :")
            if not interaction.channel==channel_perso:
                await interaction.channel.send(f"{i.caracter[0]} : {i.caracter[1]} étoiles :")
            if i.caracter[3]:
                if player.caracter[5]!=1040228357981343764:
                    await channel_perso.send(f"{i.caracter[3]}")
                if not interaction.channel==channel_perso:
                    await interaction.channel.send(f"{i.caracter[3]}")
    elif nombre_de_tirage>10:
        await interaction.response.send_message("vous ne pouvez éffectuer qu'un maximum de 10 tirages à la fois")
    else:
        await interaction.response.send_message(f"il vous manque {nombre_de_tirage-player.caracter[2]} gemmes")

@bot.tree.command(name="delete_item",description="permet de supprimer un item")
async def delete_item(interaction:discord.Interaction,name:str):
    item=Items(name)
    if item.is_item() and bon_role(interaction.user):
        item.delete_item()
        await interaction.response.send_message(f"l'item {name} a été supprimé ")
    elif not bon_role(interaction.user):
        await interaction.response.send_message("vous n'avez pas le bon role")
    else:
        await interaction.response.send_message(f"l'item {name} n'as pas été trouvé")

@bot.tree.command(name="change_channel",description="permet de changer ou d'initialiser le channel d'un joueur")
async def change_channel(interaction:discord.Interaction,user:discord.Member):
    player = Player(user.name,user.id)
    player.is_player()
    if bon_role(interaction.user):
        player.caracter[5]=interaction.channel_id
        player.update_stats_player_fichier()
        await interaction.response.send_message(f"le nouveau channel perso de {user} est désormais {interaction.channel.name} ")
    else:
        await interaction.response.send_message("vous n'avez pas le bon role")

@bot.tree.command(name="see_image_item",description="permet de voir l'image d'un item")
async def change_channel(interaction:discord.Interaction,name_item:str):
    item=Items(name_item)
    if item.is_item() and item.caracter[3]:
        await interaction.response.send_message(item.caracter[3])
    elif not item.caracter[3]:
        await interaction.response.send_message(f"l'item {item} n'as pas d'image ")
    else:
        await interaction.response.send_message(f"l'item {item} n'as pas été trouvé")

@bot.tree.command(name="see_pity",description="permet de voir sa pity")
async def voir_sa_pity(interaction:discord.Interaction):
    player=Player(interaction.user.name,interaction.user.id)
    player.is_player()
    await interaction.response.send_message(f"pour l'obtention d'une 4 étoiles: {player.caracter[6][0]}/{player.caracter[6][2]} \n pour l'obtention d'une 5 étoiles: {player.caracter[6][1]}/{player.caracter[6][3]}")

@bot.tree.command(name="see_pity_of_a_player",description="permet de voir la pity d'un joueur")
async def see_pity_of_a_player(interaction:discord.Interaction,user:discord.Member):
    if bon_role(interaction.user):
        player=Player(user.name,user.id)
        player.is_player()
        await interaction.response.send_message(f"pour l'obtention d'une 4 étoiles: {player.caracter[6][0]}/{player.caracter[6][2]} \n pour l'obtention d'une 5 étoiles: {player.caracter[6][1]}/{player.caracter[6][3]}")
    else:
        await interaction.response.send_message("vous n'avez pas le bon role")
@bot.tree.command(name="see_effects",description="permet de voir ses effets")
async def see_effects(interaction: discord.Interaction):
    player = Player(interaction.user.name,interaction.user.id)
    player.is_player()
    text=""
    for i in player.caracter[4]:
        item=Items("pomme",id=i['id'])
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
        await interaction.response.send_message(f"vous n'avez aucun effet")

@bot.tree.command(name="see_effects_of_a_player",description="permet de voir les effets d'un joueur")
async def see_effects_of_a_player(interaction: discord.Interaction, user:discord.Member):
    if bon_role(interaction.user):
        player=Player(user.name,user.id)
        player.is_player()
        text=""
        for i in player.caracter[4]:
            item=Items("pomme",id=i['id'])
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

@bot.tree.command(name="panda",description=r"utilise la capacité de panda et réduit de 10% la pity a avoir")
async def panda(interaction: discord.Interaction):
    player=Player(interaction.user.name,interaction.user.id)
    player.is_player()
    if {"id":Datas.panda_id,"active":True} in player.caracter[8]:
        player.caracter[6][2]=9
        player.caracter[6][3]=45
        for power in player.caracter[8]:
            if power['id']==Datas.panda_id:
                power['active']=False
        player.update_stats_player_fichier()
        await interaction.response.send_message(f"votre pouvoir a bien été utilisé votre pity est désormais de : \n {player.caracter[6][0]}/{player.caracter[6][2]} pour les 4 étoiles \n {player.caracter[6][1]}/{player.caracter[6][3]} pour les 5 étoiles")
    elif {"id":Datas.panda_id,"active":False} in player.caracter[8]:
        await interaction.response.send_message("votre pouvoir est désactivé")
    else:
        await interaction.response.send_message("vous n'avez pas l'item requis pour effectuer cette commande")


@bot.tree.command(name="arsmote",description="permet de reroll un 4 étoile obtnu lors du dernier tirage pour en obtenir un autre")
async def arsmote(interaction: discord.Interaction,nom_du_4_étoiles:str):
    player=Player(interaction.user.name,interaction.user.id)
    player.is_player()
    item=Items(nom_du_4_étoiles)
    channel_perso=bot.get_channel(player.caracter[5])
    if {"id":Datas.arsmote_id,"active":True} in player.caracter[8] and item.is_item() and item.caracter[6] in player.caracter[9] and item.caracter[1]==4:
        if player.lose_item(item.caracter[6],1):
            text=""
            for i in player.tirages(1,tirage_4=True):
                text+=f"{i.caracter[0]}: {i.caracter[1]} étoiles \n"
            for power in player.caracter[8]:
                if power['id']==Datas.arsmote_id:
                    power['active']=False
            await interaction.response.send_message(text)
            await channel_perso.send(text)
            await interaction.channel.send(i.caracter[3])
            await channel_perso.send(i.caracter[3])
            player.update_stats_player_fichier()
        else:
            await interaction.response.send_message(f"l'item {item.caracter[0]} n'as pas réussis à être supprimé")
    elif {"id":Datas.arsmote_id,"active":False} in player.caracter[8]:
        await interaction.response.send_message("votre pouvoir est désactivé")
    elif not {"id":Datas.arsmote_id,"active":True} in player.caracter[8]:
        await interaction.response.send_message("vous n'avez pas l'item requis pour effectuer cette commande")
    elif not item.is_item():
        await interaction.response.send_message(f"l'item {nom_du_4_étoiles} n'as pas été trouvé")
    elif not item.caracter[6] in player.caracter[9]:
        await interaction.response.send_message(f"vous n'avez pas obtenu l'item {item.caracter[0]} lors de votre dernier tirage")
    else:
        await interaction.response.send_message(f"l'item {item.caracter[0]} n'est pas 4 étoiles mais {item.caracter[1]} étoiles ")

            

@bot.tree.command(name="reset_power",description="permet de réactivé les effets des persos panda et arsmote")
async def reset_power(interaction: discord.Interaction):
    if bon_role(interaction.user):
        text=""
        with open(Datas.player_file,"r") as f:
            for ligne in f:
                ligne=json.loads(ligne)
                for power in ligne[8]:
                    power['active']=True
                text+=json.dumps(ligne)+"\n"
        with open(Datas.player_file,"w") as f:
            f.write(text)
        await interaction.response.send_message("l'opération a réussis ")
    else:
        await interaction.response.send_message("vous n'avez pas le bon role")

@bot.tree.command(name="yato",description=r"20% de chances d'obtenir 2 cristaux durant 10 tirages l'reste=items")
async def yato(interaction: discord.Interaction):
    player=Player(interaction.user.name,interaction.user.id)
    player.is_player()
    if {"id":Datas.Yato_id,"active":True} in player.caracter[8] and not player.caracter[10]>0:
        player.caracter[10]=10
        for power in player.caracter[8]:
                if power['id']==Datas.Yato_id:
                    power['active']=False
        print("activé")
    elif  not {"id":Datas.Yato_id,"active":True} in player.caracter[8]:
        print("pouvoir désactivé")
    else:
        print("le pouvoir est encore actif")
    player.update_stats_player_fichier()


@bot.event
async def on_raw_reaction_add(payload):
    channel=bot.get_channel(Datas.hosts_id)
    player=Player(payload.member.name,payload.user_id)
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
    if message.content.find("!question")==0 and bon_role(message.author) and message.channel.id==Datas.channel_question:
        #si y a le !question dans le message et bon_role
        try:
            args=message.content.split(" ")
            args=args[1].split("_")
            args[0]=int(args[0])
            args[1]=int(args[1])*3600+int(str(time.time()).split(".")[0])
            args={"nb_gemmes":args[0],"time":args[1],"id_users":[]}
            with open(Datas.question_file,'w') as f:
                f.write(json.dumps(args))
        except:
            bot_channel = bot.get_channel(Datas.channel_message_bot)
            await bot_channel.send(f"<@{message.author.id}> erreur: le message doit absolument commencer par 'question A_B', A étant le nombre de gemmes et B le nombre d'heure, veuillez supprimer et renvoyer le message pour que cela puisse fonctionné")
    elif message.content.find("!question")==-1 and not message.author.id in line['id_users'] and int(str(time.time()).split(".")[0])<line['time']: 
        player=Player(message.author.name,message.author.id)
        player.is_player()
        player.caracter[2]+=line['nb_gemmes']
        line['id_users'].append(message.author.id)
        with open(Datas.question_file,"w") as f:
            f.write(json.dumps(line))
        player.update_stats_player_fichier()






bot.run(Datas.bot_token)