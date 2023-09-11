import sqlite3

from datas.datas import Datas


#items
def add_item(item_name, rarity, drop, image_link, on_tirage):
    if get_item(item_name=item_name):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Items` VALUES (?,?,?,?,?,?)", (None, item_name, rarity, drop, image_link, on_tirage))
    con.commit()

    cur.close()
    con.close()

    return True

def get_items_ontirage():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Items` WHERE `on_tirage`=true")
    items = cur.fetchall()

    cur.close()
    con.close()

    return items

def get_item(item_name=False, item_id=False):
    #check if only one of the two have a value
    if (item_name and item_id) or (not item_name and not item_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    if item_name:
        cur.execute("SELECT * FROM `Items` WHERE `item_name`=?",(item_name,))
    if item_id:
        cur.execute("SELECT * FROM `Items` WHERE `item_id`=?",(item_id,))
    item = cur.fetchone()

    cur.close()
    con.close()

    return item

def update_item(item_id, item_name, rarity, drop, image_link, on_tirage):
    if not get_item(item_id=item_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Items` 
                SET `item_name`=?, `rarity`=?, 
                `drop`=?, `image_link`=?, 
                `on_tirage`=? 
                WHERE `item_id`=?;"""
                ,(item_name, rarity, drop, image_link, on_tirage, item_id))
    con.commit()

    cur.close()
    con.close()

    return True

def delete_item(item_id):
    if not get_item(item_id=item_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("DELETE FROM `Items` WHERE `item_id`=?",(item_id,))
    con.commit()

    cur.close()
    con.close()

    return True

#players
def add_player(player_id):
    if get_player(player_id=player_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Players`(`player_id`) VALUES (?)", (player_id,))
    con.commit()

    cur.close()
    con.close()

    return True

def get_player(player_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Players` WHERE `player_id`=?",(player_id,))
    player = cur.fetchone()

    cur.close()
    con.close()

    return player

def update_player(player_id, gems_numbers, gems_spent, channel_id, Yato_tirage_number, pity_den_4, pity_den_5, pity_den_6, pity_num_4, pity_num_5, pity_num_6, last_question_answerd, last_vote_message_id):
    if not get_player(player_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Players` 
                SET `gems_numbers`=?, `gems_spent`=?, 
                `channel_id`=?, `Yato_tirage_number`=?, 
                `pity_den_4`=? , `pity_den_5`=?,
                `pity_den_6`=? , `pity_num_4`=?,
                `pity_num_5`=? , `pity_num_6`=?,
                `last_question_answerd`=? , `last_vote_message_id`=?
                WHERE `player_id`=?;"""
                ,(gems_numbers, gems_spent, channel_id, Yato_tirage_number, pity_den_4, pity_den_5, pity_den_6, pity_num_4, pity_num_5, pity_num_6, last_question_answerd, last_vote_message_id,player_id))
    con.commit()

    cur.close()
    con.close()

    return True

def update_player_simple(player):
    return update_player(player[0],player[1],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12])

#item effects
def get_effect(item_id=False, effect_id=False, nb_items=100):
    if (not effect_id and not item_id):
        return False
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    if item_id:
        cur.execute("SELECT * FROM `Item_Effects` WHERE `item_id`=? AND `item_number_required`<=?",(item_id,nb_items))
    else:
        cur.execute("SELECT * FROM `Item_Effects` WHERE `effect_id`=? AND `item_number_required`<=?",(effect_id,nb_items))
    item_effects = cur.fetchall()

    cur.close()
    con.close()

    return item_effects


def add_effect(effect, item_number_required, item_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Item_Effects`(`effect`,`item_number_required`,`item_id`) VALUES(?,?,?)",(effect, item_number_required, item_id))
    con.commit()

    cur.close()
    con.close()

    return True

def delete_effect(effect_id):
    if not get_effect(effect_id=effect_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("DELETE FROM `Item_Effects` WHERE `effect_id`=?",(effect_id,))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_effect():
    pass