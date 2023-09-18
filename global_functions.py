import random, json

from datas.datas import Datas
import dtb_funcs

ITEM_NAME = 1
ITEM_STARS = 2
ITEM_DROP = 3

PITYN4 = 0
PITYD4 = 1
PITYN5 = 2
PITYD5 = 3
PITYN6 = 4
PITYD6 = 5

def tirage(stars=None):
    is_exist = False
    total_drop = 0
    items = dtb_funcs.get_items_ontirage()
    for item in items:
        if stars==None or item[ITEM_STARS]==stars:
            total_drop+=item[ITEM_DROP]
            is_exist = True

    if is_exist:
        result_drop = random.randint(1, total_drop)
        for item in items:
            if stars==None or item[ITEM_STARS]==stars:
                result_drop-=item[ITEM_DROP]
                if result_drop <= 0:
                    final_result={"name":item[ITEM_NAME],"stars":item[ITEM_STARS]}
                    break
        return final_result
    elif stars:
        return tirage(stars-1)
    else:
        return False

def bon_role(user):
    for r in user.roles:
        if r.id in Datas.role_modo:
            return True

def votes(user,message):
    player=Player(user.name,user.id)
    player.is_player()
    if not message.id == player.last_vote:
        player.last_vote = message.id
        player.nb_gemmes+=1
        player.update_stats_player()
        return True
    return False

class Player:
    def __init__(self,name,id,nb_gemmes=0 ,gemmes_spend=0,items=[],salon=1040228357981343764,pity=[0,0,10,50,0,80],last_vote=None,powers=[],historique=[],yato_tirages=0, last_question_answerd=None):
        self.id = id
        self.name = name
        self.nb_gemmes = nb_gemmes
        self.gemmes_spend = gemmes_spend
        self.salon = salon
        self.pity = pity
        self.yato_tirages = yato_tirages
        self.last_vote = last_vote
        self.last_question_answerd = last_question_answerd
        self.items = items
        self.powers = powers
    

    def update_from_sql(self, sql):
        self.id,self.nb_gemmes,self.gemmes_spend,self.salon,self.yato_tirages,dp4,dp5,dp6,np4,np5,np6,self.last_question_answerd,self.last_vote = sql
        self.pity = [np4,dp4,np5,dp5,np6,dp6]
        self.items
        self.powers

    def update_stats_player(self):
        """actualise la base de données avec les données actuels de l'instance"""
        return dtb_funcs.update_player(self.id, self.nb_gemmes, self.gemmes_spend, self.salon, self.yato_tirages, self.pity[PITYD4], self.pity[PITYD5], self.pity[PITYD6], self.pity[PITYN4], self.pity[PITYN5], self.pity[PITYN6],self.last_question_answerd,self.last_vote)
    
    def is_player(self):
        """
        vérifie l'occurence dans la base de donnés à partir de l'id si présent actualise les données de l'instance sinon le rajoute dans le fichier avec les données actuels de l'instance
        """
        player = dtb_funcs.get_player(self.id)
        if player:
            self.update_from_sql(player)
            return True
        
        dtb_funcs.add_player(self.id)
        
    def spend_gems(self,nb):
        """dépense les gemmes d'un joueur"""
        if self.nb_gemmes>=nb>0:
            self.nb_gemmes-=nb
            self.gemmes_spend+=nb
            self.update_stats_player()
            return True
        else:
            return False
        
    def lose_item(self,item_id,nb):
        item = dtb_funcs.get_player_item(self.id, item_id)
        #if he's still gonna have the item after
        if item[3] > nb:
            dtb_funcs.edit_player_item(item_id=item_id,player_id=self.id,numbers=item[3]-nb,last_tirage=item[4])
            return True
        elif item[3] == nb:
            dtb_funcs.delete_player_item(item_id, self.id)
            return True
        else:
            return False


    def add_items(self,items,tirage=False):
        """ajoute les items au joueur"""
        for item in items:
            item_db = dtb_funcs.get_player_item(item_id=item["id"],player_id=self.id)
            if item_db and tirage:
                print("test")
                dtb_funcs.edit_player_item(item_db[1],item_db[2],item_db[3]+item["nb"],True)
            elif item_db:
                print("test2")
                dtb_funcs.edit_player_item(item_db[1],item_db[2],item_db[3]+item["nb"],item_db[4])
            else:
                print("test3")
                dtb_funcs.add_player_item(item["id"],self.id,item["nb"],tirage)

    def tirages(self,nb_tirage,tirage_4=False):
        all_items=[]
        for i in range(nb_tirage):
            result=None
            yato_aléa = random.randint(1,5)
            print(yato_aléa)
            #yatoo
            if self.yato_tirages>0 and yato_aléa==4:
                result = "2 cristaux d'expeditions"
                self.nb_gemmes+=2
                self.spend_gems(1)
                self.update_stats_player_fichier()
                all_items.append(result)
            else:
                #arsmote
                if tirage_4==True:
                    #potentiel problème si pas de 4 étoiles
                    result = tirage(4)

                else:
                    print(self.pity)
                    #pity 6 étoiles
                    if self.pity[4]+1>=self.pity[5]:
                        result = tirage(6)
                        if result:
                            stars=6
                        else:
                            stars=0
                    #pity 5 étoiles
                    elif self.pity[1]+1>=self.pity[3]:
                        result =tirage(5)
                        if result:
                            stars=5
                        else:
                            stars=0
                    #pity 4 étoiles
                    elif self.pity[0]+1>=self.pity[2]:
                        result = tirage(4)
                        if result:
                            stars=4
                        else:
                            stars=0
                    #tirage classique
                    else:
                        result = tirage()
                        if result:
                            stars=result['stars']
                        else:
                            stars=0
                    #ajuste la pity en fonction du résultat
                    #reset panda dès l'obtention d'une min 4 étoiles
                    if stars >= 4:
                        self.pity[PITYD6]=80
                        self.pity[PITYD5]=50
                        self.pity[PITYD4]=10
                    if stars == 6:
                        self.pity[PITYN6]=0
                        self.pity[PITYN4]+=1
                        self.pity[PITYN5]+=1
                        self.spend_gems(1)
                    elif stars == 5:
                        self.pity[PITYN5]=0
                        self.pity[PITYN4]+=1
                        self.pity[PITYN6]+=1
                        self.spend_gems(1)
                    elif stars== 4:
                        self.pity[PITYN4]=0
                        self.pity[PITYN5]+=1
                        self.pity[PITYN6]+=1
                        self.spend_gems(1)
                    elif stars:
                        self.pity[PITYN4]+=1
                        self.pity[PITYN5]+=1
                        self.pity[PITYN6]+=1
                        self.spend_gems(1)
                if result:
                    new_item=Items(result['name'])
                    new_item.is_item()
                    self.add_items([{"id":new_item.id,"nb":1}],tirage=True)
                    all_items.append(new_item)
            #réduit de 1 la variable yato
            if self.yato_tirages>0:
                self.yato_tirages-=1
                
        self.update_stats_player()
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
    
    def update_from_sql_r(self, sql_r):
        self.id, self.name, self.stars, self.drop, self.url_img, self.on_tirage=sql_r
        effects = dtb_funcs.get_effects(item_id=self.id)
        self.effects = [{"effect":effect[1],"number_required":effect[2]} for effect in effects]

    def is_item(self, by_name=True):
        """vérifie si l'item existe renvoi et le retourne"""
        if by_name:
            item = dtb_funcs.get_item(item_name=self.name)
            if item:
                self.update_from_sql_r(item)
                return True

        else:
            item = dtb_funcs.get_item(item_id=self.id)
            if item:
                self.update_from_sql_r(item)
                return True
        
        return False
    
    def update_item(self):
        return dtb_funcs.update_item(self.id, self.name, self.stars, self.drop, self.url_img, self.on_tirage)

    def add_item(self):
        """créer l'item retourne faux si il existe déja"""
        if self.is_item():
            return False
        else:
            dtb_funcs.add_item(self.name, self.stars, self.drop, self.url_img, self.on_tirage)
            return True

    def delete_item(self):
        """supprime l'item du fichier si il existe"""
        return dtb_funcs.delete_item(self.id)