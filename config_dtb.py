import sqlite3

from datas.datas import Datas

TABLES = ["Items","Item_Effects","Players","Player_items","Questions","Powers","Hosts"]

def delete():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    for table in TABLES:
        cur.execute(f"DROP TABLE {table}")

    con.commit()

    cur.close()
    con.close()

def check():
    con = sqlite3.connect(Datas.DATABASE)
    cur = con.cursor()

    #item table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Items`
        (`item_id` INTEGER PRIMARY KEY NOT NULL, 
        `item_name` VARCHAR(65) UNIQUE NOT NULL, 
        `rarity` INTEGER NOT NULL, 
        `drop` INTEGER NOT NULL, 
        `image_link` TEXT, 
        `on_tirage` BOOL NOT NULL
        );""")
    
    #item effects
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Item_Effects`
        (`effect_id` INTEGER PRIMARY KEY NOT NULL,
        `effect` TEXT,
        `item_number_required` INTEGER NOT NULL DEFAULT 0,
        `item_id` INTEGER , 
        FOREIGN KEY(`item_id`) REFERENCES `Items`(`item_id`)
        );""")

    #player table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Players`
        (`player_id` INTEGER PRIMARY KEY NOT NULL,
        `gems_numbers` INTEGER NOT NULL DEFAULT 0, 
        `gems_spent` INTEGER NOT NULL DEFAULT 0, 
        `channel_id` INTEGER, 
        `Yato_tirage_number` INTEGER NOT NULL DEFAULT 0, 
        `pity_den_4` INTEGER NOT NULL DEFAULT 0, 
        `pity_den_5` INTEGER NOT NULL DEFAULT 0, 
        `pity_den_6` INTEGER NOT NULL DEFAULT 0, 
        `pity_num_4` INTEGER NOT NULL DEFAULT 0, 
        `pity_num_5` INTEGER NOT NULL DEFAULT 0, 
        `pity_num_6` INTEGER NOT NULL DEFAULT 0,
        `last_question_answerd_message_id` INTEGER,
        `last_vote_message_id` INTEGER
        );""")

    #player_items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Player_Items`
        (`id_player_items` INTEGER PRIMARY KEY, 
        `item_id` INTEGER , 
        `player_id` INTEGER , 
        `numbers` INTEGER NOT NULL, 
        `last_tirage` BOOL NOT NULL,
        FOREIGN KEY(`item_id`) REFERENCES `Items`(`item_id`), 
        FOREIGN KEY(`player_id`) REFERENCES `Players`(`player_id`)
        );""")
    
    #power table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Powers`
        (`power_id` INTEGER PRIMARY KEY, 
        `item_id` INT, 
        `player_id` INT, 
        `is_active` BOOL NOT NULL,
        FOREIGN KEY(`item_id`) REFERENCES `Items`(`item_id`), 
        FOREIGN KEY(`player_id`) REFERENCES `Players`(`player_id`)
        );""")

    #question table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Questions`
        (`questions_id` INTEGER PRIMARY KEY, 
        `reward` INTEGER NOT NULL, 
        `message_id` INTEGER NOT NULL
        );""")
    
    #hosts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Hosts`
        (`host_id` INTEGER PRIMARY KEY, 
        `message_id` INTEGER NOT NULL
        );""")

    con.commit()

    cur.close()
    con.close()

check()
delete()
check()