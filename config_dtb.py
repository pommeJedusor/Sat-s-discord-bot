"""
edit the votes datas (for now it's a list of all votes) to keep only the last vote
"""


import sqlite3

DATABASE = "SatBotDTB.DB"
TABLES = ["Items","Item_Effects","Players","Player_items","Hosts","Questions","Answers","Powers"]

def delete():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    for table in TABLES:
        cur.execute(f"DROP TABLE {table}")

    con.commit()

    cur.close()
    con.close()

def check():
    con = sqlite3.connect(DATABASE)
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
        `item_number_required` INTEGER NOT NULL DEFAULT 0
        );""")

    #player table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Players`
        (`player_id` INTEGER PRIMARY KEY NOT NULL, 
        `player_name` VARCHAR(65) NOT NULL,
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
        `last_vote` INTEGER,
        FOREIGN KEY(`last_vote`) REFERENCES `Hosts`(`id_host`)
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

    #answer table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Answers`
        (`answer_id` INTEGER PRIMARY KEY, 
        `question_id` INT, 
        `player_id` INT,
        FOREIGN KEY(`question_id`) REFERENCES `Questions`(`question_id`), 
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

    #host table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Hosts`
        (`id_host` INTEGER PRIMARY KEY, 
        `is_last` BOOL NOT NULL
        );""")
    
    #question table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS `Questions`
        (`question_id` INTEGER PRIMARY KEY, 
        `reward` INTEGER NOT NULL, 
        `is_last` BOOL NOT NULL, 
        `timestamp` INTEGER NOT NULL
        );""")

    con.commit()

    cur.close()
    con.close()

check()