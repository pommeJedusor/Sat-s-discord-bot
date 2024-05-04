import random, json

from datas.datas import Datas

from model import ModelPlayer

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
    player=ModelPlayer.Player(user.name,user.id)
    player.is_player()
    if not message.id in player.votes:
        player.votes.append(message.id)
        player.nb_gemmes+=1
        player.update_stats_player_fichier()
        return True
    return False