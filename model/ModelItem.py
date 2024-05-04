import json, random

from datas.datas import Datas

from model import global_functions

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
        return global_functions.update(self,self.file,6)
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
            global_functions.delete_line(self)