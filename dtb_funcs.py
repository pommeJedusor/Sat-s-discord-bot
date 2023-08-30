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