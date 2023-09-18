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

    cur.execute("INSERT INTO `Players`(`player_id`,`pity_den_4`,`pity_den_5`,`pity_den_6`) VALUES (?,?,?,?)", (player_id,10,50,80))
    con.commit()

    cur.close()
    con.close()

    return True

def get_player(player_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Players` WHERE `player_id`=?",(player_id,))
    player = cur.fetchone()
    print(player)

    cur.close()
    con.close()

    return player

def get_players():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Players`")
    players = cur.fetchall()

    cur.close()
    con.close()

    return players

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
                `last_question_answerd_message_id`=? , `last_vote_message_id`=?
                WHERE `player_id`=?;"""
                ,(gems_numbers, gems_spent, channel_id, Yato_tirage_number, pity_den_4, pity_den_5, pity_den_6, pity_num_4, pity_num_5, pity_num_6, last_question_answerd, last_vote_message_id,player_id))
    con.commit()

    cur.close()
    con.close()

    return True

def update_player_simple(player):
    return update_player(player[0],player[1],player[2],player[3],player[4],player[5],player[6],player[7],player[8],player[9],player[10],player[11],player[12])

#item effects
def get_effects(item_id=False, effect_id=False, nb_items=100):
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
    if not get_effects(effect_id=effect_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("DELETE FROM `Item_Effects` WHERE `effect_id`=?",(effect_id,))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_effect(effect_id, effect, item_number_required):
    if not get_effects(effect_id=effect_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Item_Effects` 
                SET `effect`=?, `item_number_required`=?
                WHERE `effect_id`=?;"""
                ,(effect, item_number_required, effect_id))
    con.commit()

    cur.close()
    con.close()

    return True

#player items
def get_player_item(player_id, item_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Player_Items` WHERE `item_id`=? AND `player_id`=?",(item_id,player_id))
    player_item = cur.fetchone()

    cur.close()
    con.close()

    return player_item

def get_player_items(player_id=False, item_id=False):
    if not player_id and not item_id:
        return False
    if player_id and item_id:
        return get_player_item(player_id,item_id)
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    if player_id:
        cur.execute("SELECT * FROM `Player_Items` WHERE `player_id`=?",(player_id,))
    else:
        cur.execute("SELECT * FROM `Player_Items` WHERE `item_id`=?",(item_id,))
    player_items = cur.fetchall()

    cur.close()
    con.close()

    return player_items

def add_player_item(item_id, player_id, numbers, last_tirage):
    if get_player_item(item_id=item_id, player_id=player_id):
        return False
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Player_Items`(`item_id`,`player_id`,`numbers`,`last_tirage`) VALUES(?,?,?,?)",(item_id, player_id, numbers, last_tirage))
    con.commit()

    cur.close()
    con.close()

    return True

def delete_player_item(item_id, player_id):
    if not get_player_item(player_id=player_id, item_id=item_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("DELETE FROM `Player_Items` WHERE `item_id`=? and `player_id`=?;",(item_id,player_id))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_player_item(item_id, player_id, numbers, last_tirage):
    if not get_player_item(item_id=item_id, player_id=player_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Player_Items` 
                SET `numbers`=?, `last_tirage`=?
                WHERE `item_id`=? and `player_id`=?;"""
                ,(numbers, last_tirage, item_id, player_id))
    con.commit()

    cur.close()
    con.close()

    return True

def delast_player_item(player_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Player_Items` 
                SET `last_tirage`=?
                WHERE `player_id`=?;"""
                ,(False, player_id))
    con.commit()

    cur.close()
    con.close()

#hosts
def get_host():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Hosts`;")
    host = cur.fetchone()

    cur.close()
    con.close()

    return host

def add_host(message_id):
    if get_host():
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Hosts`(`message_id`) VALUES(?)",(message_id,))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_host(message_id):
    if not get_host():
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Hosts` 
                SET `message_id`=?"""
                ,(message_id,))
    con.commit()

    cur.close()
    con.close()

    return True

#Questions
def get_question():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Questions`;")
    question = cur.fetchone()

    cur.close()
    con.close()

    return question

def add_question(message_id, reward):
    if get_question():
        delete_question()
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Questions`(`message_id`,`reward`) VALUES(?,?)",(message_id, reward))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_question(reward):
    if not get_question():
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Questions` 
                SET `reward`=?;"""
                ,(reward, ))
    con.commit()

    cur.close()
    con.close()

    return True

def delete_question():
    if not get_question():
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("DELETE FROM `Questions`;")
    con.commit()

    cur.close()
    con.close()

    return True

#Powers
def get_power(item_id, player_id):
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("SELECT * FROM `Powers` WHERE `item_id`=? AND `player_id`=?;",(item_id, player_id))
    power = cur.fetchone()

    cur.close()
    con.close()

    return power


def add_power(item_id, player_id, is_active):
    if get_power(item_id, player_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("INSERT INTO `Powers`(`item_id`,`player_id`,`is_active`) VALUES(?,?,?)",(item_id, player_id, is_active))
    con.commit()

    cur.close()
    con.close()

    return True

def edit_power(item_id, player_id, is_active):
    if not get_power(item_id, player_id):
        return False
    
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    cur.execute("""
                UPDATE `Powers` 
                SET `is_active`=?
                WHERE `item_id`=? AND `player_id`=?;"""
                ,(is_active, item_id, player_id))
    con.commit()

    cur.close()
    con.close()

    return True
