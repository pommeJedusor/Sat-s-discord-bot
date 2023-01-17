-au lancement vérifie si il y a de nouvelles réponses à la question de la semaine et si il y a de nouveaux votes(hosts)
-indice de drop : au moment du tirage si pity non complète le bot assomme les indices de drop et tire au sort un nombre au hasard et renvoy l'objet correspondant exemple: pomme: 1 , poire: 2 , patate: 5
le bot fait la somme 1+2+5=8 tire au sort un nombre entier entre 1 et 8 compris puis si 1 donne pomme, si 2 ou 3 donne poire et de 4 à 8 donne patate
(si la somme total est de cent cela équivaut à un pourcentage et si de milles ou dix milles cela l'inclut avec les virgules. exemple: pomme: 40, poire: 10 patate: 50. la pomme auras 40% de chance d'être tirés)



modo:
-add_gems : permet d'ajouter un nombre de gemmes à un joueur (le nombre de gemmes doit être positif)
-see_gems_of_a_player: permet à un modo de voir les gemmes possédés et dépensé par un joueur
-create_item: permet à un modo de creer un item avec comme données: son nom, son nombre d'étoiles, le lien renvoyant vers son image, son indice de drop(ne pas mettre de virgule)
-edit_item: permet de modifier un item : effets(sont à séparés par une virgule de telle sorte que le premier soit si il en as que un, le deuxième si il en as deux, etc. si le joueur en as plus le bot considéras le dernier)
tirage_active True si dans les tirages,False sinon, new_name pour changer le nom de l'objets
-add_item_to_a_player: permet d'ajouter un objet à un joueur en spécifiant son nom parfaitement bien ortographié
-see_items_of_a_player: permet de voir les items possédés par un joueur incluant leurs nombre
-spend_gems: permet de réduire le nombre de gemmes d'un joueur dépenser=True si vous voulez qu'il soit contabiliser dans les dépenses(par défaut sur False)
-delete_item: permet de supprimer un item de la base de données,marche mal si déja obtenu par des joueurs mais utiliser plutôt /edit_item pour le retirer des items des tirages
-change_channel: permet de changer/d'attribuer un channel personnelle à un joueur pour afficher le résultat de ces tirages
-reset_power: permet de réactiver les pouvoirs panda et arsmote des joueurs

players:
-see_gems: permet de voir le nombre de gemmes possédés et dépensés par soi même
-see_all_items: permet de voir tous les items(le nom,les étoiles,l'indice de drop, et les effets)
-see_items: permet de voir ses items et leurs nombres
-tirage: permet de faire des tirages max 10 en dépensant 1 gemmes par tirages(ne marche pas si pas assez de gemmes)
-see_image_item: permet de voir l'image d'un item
-see_pity: permet de voir l'état de sa pity
-see_effects: permet de voir tous les effets attribués par vos objets
-panda: réduit de 10% la pity pas réutilisable jusqu'à ce que les modos le réactive, nécéssite l'item panda
-arsmote: permet de relancer le tirage d'un item 4 étoiles obtenu lors du dernier tirage(peut réobtenir le même si pas de chance)