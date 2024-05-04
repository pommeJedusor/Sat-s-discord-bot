import random, json

from datas.datas import Datas

def tirage(file,stars=None):
    is_exist=False
    with open(file,'r') as f:
        pomme=0
        for line in f:
            line=json.loads(line)
            #si pas de nombre d'étoiles précise ou correspondante
            if stars==None or line[1]==stars:
                #si dispo dans les tirages
                if line[5]==True:
                    pomme+=line[2]
                    is_exist=True
    if is_exist:
        result = random.randint(1,pomme)
        with open(file,'r') as f:
            fined=False
            for line in f:
                line=json.loads(line)
                if stars==None or line[1]==stars:
                    if line[5]==True:
                        result-=line[2]
                        if result<=0 and not fined:
                            final_result={"name":line[0],"stars":line[1]}
                            break
        return final_result
    #si nombre d'étoiles détérminé non égal à zéro
    elif stars:
        return tirage(file,stars-1)
    else:
        return False
        


def update(self,file,num_param):
        """fichier, numero du parametre dans le fichier,actualise les données"""
        with open(file,"r") as f:
            text=""
            exist=False
            for line in f:
                line=json.loads(line)
                if line[num_param]==self.get_jsonline()[num_param]:
                    line=self.get_jsonline()
                    exist=True
                text+=json.dumps(line)+"\n"
        with open(file,"w") as f:
            f.write(text)
        if exist:
            return True
        else:
            return False
def add_line(self,file):
    """ajoute au fichier la ligne correspondant à l'item ou au joueur"""
    with open(file,"a") as f:
        f.write(json.dumps(self.get_jsonline())+"\n")
def delete_line(self):
    """supprime du fichier la ligne correspondante à l'instance"""
    with open(self.file,"r") as f:
        text=""
        for line in f:
            if not json.loads(line)==self.get_jsonline():
                text+=line
    with open(self.file,"w") as f:
        f.write(text)

def bon_role(user,animateur=False):
    for r in user.roles:
        if r.id in Datas.role_modo:
            return True
        if animateur and r.id in Datas.role_animateur:
            return True

def votes(user,message):
    player=Player(user.name,user.id)
    player.is_player()
    if not message.id in player.votes:
        player.votes.append(message.id)
        player.nb_gemmes+=1
        player.update_stats_player_fichier()
        return True
    return False

class Player:
    def __init__(self,name,id,nb_gemmes=0 ,gemmes_spend=0,items=[],salon=1040228357981343764,pity=[0,0,10,50,0,80],votes=[],powers=[],historique=[],yato_tirages=0):
        self.name = name
        self.id = id
        self.nb_gemmes = nb_gemmes
        self.gemmes_spend = gemmes_spend
        self.items = items
        self.salon = salon
        self.pity = pity
        self.votes = votes
        self.powers = powers
        self.historique = historique
        self.yato_tirages = yato_tirages
        self.file=Datas.player_file
    
    def get_jsonline(self):
        return [self.name,self.id,self.nb_gemmes,self.gemmes_spend,self.items,self.salon,self.pity,self.votes,self.powers,self.historique,self.yato_tirages]

    def update_from_json_line(self, jsonline):
        self.name,self.id,self.nb_gemmes,self.gemmes_spend,self.items,self.salon,self.pity,self.votes,self.powers,self.historique,self.yato_tirages = jsonline


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
                if line[1]==self.id:
                    self.update_from_json_line(line)
                    return True
        if not self.update_stats_player_fichier():
            add_line(self,self.file)
            return False
    def spend_gems(self,nb):
        """dépense les gemmes d'un joueur"""
        if self.nb_gemmes>=nb>0:
            self.nb_gemmes-=nb
            self.gemmes_spend+=nb
            self.update_stats_player_fichier()
            return True
        else:
            return False
        
    def lose_item(self,item_id,nb):
        pomme=True
        item=Items("pomme",id=item_id)
        if item.is_item(x=6):
            x=0
            for item2 in self.items:
                if item2['id']==item.id and pomme and item2['nb']>nb:
                    item2['nb']-=nb
                    pomme=False
                elif item2['id']==item.id and pomme and item2['nb']==nb:
                    del self.items[x]
                    power = lambda pow:pow["id"]==item2["id"]
                    powers = list(filter(power,self.powers))
                    print(powers)
                    pomme=0
                    if powers:
                        for i in range(len(self.powers)):
                            print(powers[0])
                            print(self.powers[i]["id"])
                            if self.powers[i]["id"] == powers[0]["id"]:
                                print("yop")
                                pomme=i+1
                        if pomme:
                            del self.powers[pomme-1]
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
            for item2 in self.items:
                if is_item.is_item(x=6) and (is_item.id) == item2['id'] and pomme:
                    self.items[x]['nb']+=item["nb"]
                    pomme=False
                x+=1
            if pomme==True:
                self.items.append({"id":is_item.id,"nb":item["nb"]})
                pomme=False
                if is_item.id==Datas.panda_id:
                    if not {"id":Datas.panda_id,"active":True} in self.powers or not {"id":Datas.panda_id,"active":False} in self.powers:
                        self.powers.append({"id":Datas.panda_id,"active":True})
                elif is_item.id==Datas.arsmote_id:
                    if not {"id":Datas.arsmote_id,"active":True} in self.powers or not {"id":Datas.arsmote_id,"active":False} in self.powers:
                        self.powers.append({"id":Datas.arsmote_id,"active":True})
                elif is_item.id==Datas.Yato_id:
                    if not {"id":Datas.Yato_id,"active":True} in self.powers or not {"id":Datas.Yato_id,"active":False} in self.powers:
                        self.powers.append({"id":Datas.Yato_id,"active":True})
        self.update_stats_player_fichier()
    def tirages(self,nb_tirage,tirage_4=False):
        files=Datas.items_file
        all_items=[]
        for i in range(nb_tirage):
            result=None
            aléa = random.randint(1,5)
            print(aléa)
            #yatoo
            if self.yato_tirages>0 and aléa==4:
                result = "2 cristaux d'expeditions"
                self.nb_gemmes+=2
                self.update_stats_player_fichier()
                self.spend_gems(1)
                all_items.append(result)
            else:
                if tirage_4==False:
                    print(self.pity)
                    #pity 6 étoiles
                    if self.pity[4]+1>=self.pity[5]:
                        result = tirage(files,6)
                        if result:
                            stars=6
                        else:
                            stars=0
                    #pity 5 étoiles
                    elif self.pity[1]+1>=self.pity[3]:
                        result =tirage(files,5)
                        if result:
                            stars=5
                        else:
                            stars=0
                    #pity 4 étoiles
                    elif self.pity[0]+1>=self.pity[2]:
                        result = tirage(files,4)
                        if result:
                            stars=4
                        else:
                            stars=0
                    #tirage classique
                    else:
                        result = tirage(files)
                        if result:
                            stars=result['stars']
                        else:
                            stars=0
                    #ajuste la pity en fonction du résultat
                    #reset panda dès l'obtention d'une min 4 étoiles
                    if stars >= 4:
                        self.pity[5]=80
                        self.pity[3]=50
                        self.pity[2]=10
                    if stars == 6:
                        self.pity[4]=0
                        self.pity[0]+=1
                        self.pity[1]+=1
                        self.spend_gems(1)
                    elif stars == 5:
                        self.pity[1]=0
                        self.pity[4]+=1
                        self.pity[0]+=1
                        self.spend_gems(1)
                    elif stars== 4:
                        self.pity[0]=0
                        self.pity[4]+=1
                        self.pity[1]+=1
                        self.spend_gems(1)
                    elif stars:
                        self.pity[0]+=1
                        self.pity[1]+=1
                        self.pity[4]+=1
                        self.spend_gems(1)
                else:
                    result= tirage(files,4)
                if result:
                    new_item=Items(result['name'])
                    new_item.is_item()
                    self.add_item([{"id":new_item.id,"nb":1}])
                    all_items.append(new_item)
            #réduit de 1 la variable yato
            if self.yato_tirages>0:
                self.yato_tirages-=1
        self.historique=[]
        for item in all_items:
            if not item=="2 cristaux d'expeditions":
                self.historique.append(item.id)
        self.update_stats_player_fichier()
        return all_items
class Items:
    def __init__(self,name,stars=0,drop=0,url_img="",effects=[],on_tirage=True,id=random.randint(1,1000000000)):
        self.name = name
        self.stars = stars
        self.drop = drop
        self.url_img = url_img
        self.effects = effects
        self.on_tirage = on_tirage
        self.id = id
        self.file=Datas.items_file

    def get_jsonline(self):
        return [self.name,self.stars,self.drop,self.url_img,self.effects,self.on_tirage,self.id]

    def update_from_json_line(self, jsonline):
        self.name,self.stars,self.drop,self.url_img,self.effects,self.on_tirage,self.id=jsonline

    def is_item(self,x=0):
        """vérifie si l'item existe renvoi et le retourne"""
        with open(self.file,"r") as f:
            for line in f:
                line=json.loads(line)
                if line[x]==self.get_jsonline()[x]:
                    self.update_from_json_line(line)
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
                f.write(json.dumps(self.get_jsonline())+"\n")
                return True
    def delete_item(self):
        """supprime l'item du fichier si il existe"""
        if not self.is_item():
            return False
        else:
            delete_line(self)