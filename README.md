
| au lancement |
|--------------|
|check si nouveaux messages dans question et agit en conséquence|
|vérifie si il y a de nouveaux votes(hosts)|

au moment du tirage si pity non complète le bot additionne les indices de drop et tire au sort un nombre au hasard et renvoy l'objet correspondant exemple: pomme: 1 , poire: 2 , patate: 5 le bot fait la somme 1+2+5=8 tire au sort un nombre entier entre 1 et 8 compris puis si 1 donne pomme, si 2 ou 3 donne poire et de 4 à 8 donne patate (si la somme total est de cent cela équivaut à un pourcentage et si de milles ou dix milles cela l'inclut avec les virgules. exemple: pomme: 40, poire: 10 patate: 50. la pomme auras 40% de chance d'être tirés)

pour la question de la semaine, vous pouvez mettre au début la commande "!question x_y", x étant égal au nombre de gemmes que recevront les joueurs répondant à la question(si répondent plusieur fois ne donne qu'une fois les gemmes) et y étant égal au nombre d'heures pendant lequelles les joueur répondant pourront obtenir la récompense(si nouvelle question l'ancienne question ne donneras quoi qu'il arrive plus de récompense)

|commandes|pour les modos|
|---------|--------------|
|add_gems |permet d'ajouter un des gemmes à un joueur|
|see_gems_of_a_player|permet de voir les gemmes possédés et dépensé par un joueur|
|create_item|permet de creer un item données: son nom, son nombre d'étoiles, le lien renvoyant vers son image, son indice de drop|
|edit_item|permet de modifier un item : effets(sont à séparés par une virgule de telle sorte que le premier soit si il en as que un, le deuxième si il en as deux, etc. si le joueur en as plus le bot considéras le dernier)|
|add_item_to_a_player|permet d'ajouter un objet à un joueur en spécifiant son nom parfaitement bien ortographié|
|see_all_items|permet de voir tous les items et leurs stats|
|remove_item_from_a_player|permet de retirer un item à un joueur,nombre = 1 par défaut|
|see_items_of_a_player|permet de voir les items possédés par un joueur incluant leurs nombre|
|spend_gems|permet de réduire le nombre de gemmes d'un joueur dépenser=True si vous voulez qu'il soit contabiliser dans les dépenses(par défaut sur False)|
|delete_item|permet de supprimer un item de la base de données,marche mal si déja obtenu par des joueurs mais utiliser plutôt /edit_item pour le retirer des items des tirages|
|change_channel|permet de changer/d'attribuer un channel personnelle à un joueur pour afficher le résultat de ces tirages|
|reset_power|permet de réactiver les pouvoirs Yato, panda et arsmote des joueurs|
|see_effects_of_a_player|permet de voir les effets d'un joueur|
|see_pity_of_a_player|permet de voir la pity d'un joueur|

|commandes|pour les joueurs|
|---------|----------------|
|see_gems|permet de voir le nombre de gemmes possédés et dépensés|
|see_all_items|permet de voir tous les items(le nom,les étoiles,l'indice de drop, et les effets)|
|see_items|permet de voir ses items et leurs nombres|
|tirage|permet de faire des tirages max 10 en dépensant 1 gemmes par tirage|
|see_image_item|permet de voir l'image d'un item|
|see_pity|permet de voir l'état de sa pity|
|see_effects|permet de voir tous les effets attribués par vos objets|
|panda|réduit de 10% la pity pas réutilisable jusqu'à ce que les modos le réactive, nécéssite l'item panda|
|arsmote|permet de relancer le tirage d'un item 4 étoiles obtenu lors du dernier tirage(peut réobtenir le même si pas de chance)|
|yato|nécéssite Yato, pour les 10 prochains tirages 20% de chance de gagner 2 gemmes à la place|
