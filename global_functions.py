import random, json

from datas.datas import Datas

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
        if self.caracter[2]>=nb>0:
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