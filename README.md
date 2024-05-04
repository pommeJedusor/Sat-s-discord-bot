#commandes pour les joueurs

|gemmes||
|---------|----------------|
|see_gems|permet de voir le nombre de gemmes que vous possédez et que vous avez dépensés|

|tirages||
|---------|----------------|
|tirage|permet de faire des tirages de max 10 à la fois en dépensant 1 gemmes par tirage|
|see_pity|permet de voir l'état de sa pity|

|objets||
|---------|----------------|
|see_items|permet de voir ses items et leurs nombres|
|see_effects|permet de voir tous les effets attribués par vos objets|
|see_all_items|permet de voir tous les items(le nom,les étoiles,l'indice de drop, et les effets)|
|see_image_item|permet de voir l'image d'un item|

|pouvoirs||
|---------|----------------|
|yato|nécéssite Yato, pour les 10 prochains tirages 20% de chance de gagner 2 gemmes à la place(si déja activé indique le nombre de tirage actif restant)|
|panda|réduit de 10% la pity pas réutilisable jusqu'à ce que les modos le réactive, nécéssite l'item panda|
|arsmote|permet de relancer le tirage d'un item 4 étoiles obtenu lors du dernier tirage(peut réobtenir le même si pas de chance)|

|autres||
|---------|----------------|
|help|permet d'accéder aux commandes, de faire une suggestion ou de report un bug|


#commandes pour les modos

|gemmes||
|---------|----------------|
|add_gems |permet d'ajouter des gemmes à un joueur|
|see_gems_of_a_player|permet de voir les gemmes possédés et dépensé par un joueur|
|spend_gems|permet de réduire le nombre de gemmes d'un joueur dépenser=True si vous voulez qu'il soit contabiliser dans les dépenses(par défaut sur False)|
|see_all_gems|permet de voir les gemmes de tous les joueurs, possibilité de trier par nom ou par gemmes|

|tirages||
|---------|----------------|
|change_channel|permet de changer/d'attribuer un channel personnelle à un joueur pour afficher le résultat de ces tirages|
|see_pity_of_a_player|permet de voir la pity d'un joueur|
|edit_pity_of_a_player|permet de modifier la pity 4, 5 ou 6 étoiles d'un joueur|

|objets||
|---------|----------------|
|add_item_to_a_player|permet d'ajouter un objet à un joueur en spécifiant son nom parfaitement bien ortographié|
|remove_item_from_a_player|permet de retirer un item à un joueur,nombre = 1 par défaut|
|see_items_of_a_player|permet de voir les items possédés par un joueur incluant leurs nombre|
|see_effects_of_a_player|permet de voir les effets d'un joueur|
|create_item|permet de creer un item; données: son nom, son nombre d'étoiles, le lien renvoyant vers son image, son indice de drop|
|edit_item|permet de modifier un item : effets(sont à séparés par une virgule de telle sorte que le premier soit si il en as que un,  le deuxième si il en as deux, etc. si le joueur en as plus le bot considéras le dernier)|
|delete_item|permet de supprimer un item de la base de données,marche mal si déja obtenu par des joueurs donc utiliser plutôt /edit_item pour le retirer des items des tirages|

|pouvoirs||
|---------|----------------|
|reset_power|permet de réactiver les pouvoirs Yato, panda et arsmote des joueurs|

|autres||
|---------|----------------|
|help|permet d'accéder aux commandes|
|recompense_question_semaine|à utiliser après avoir poser la question, permet de changer les récompense de la question de la semaine actuelle !attention effet retrospectif donc si quelqu'un a déja répondus les gemmes reçus changeront en bien ou en mal|
|oubli_question|dans le cas où la mention a été oublié puis ajouté par edit ou mis en dessous puis supprimé, si énième_message=1 prend le dernier message pour la question, si 2 l'avant dernier, etc|


##précision
au lancement  
- check si nouveaux messages dans question et agit en conséquence  
- vérifie si il y a de nouveaux votes(hosts)  

au moment du tirage si pity non complète le bot additionne les indices de drop et tire au sort un nombre au hasard et renvoy l'objet correspondant exemple: pomme: 1 , poire: 2 , patate: 5 le bot fait la somme 1+2+5=8 tire au sort un nombre entier entre 1 et 8 compris puis si 1 donne pomme, si 2 ou 3 donne poire et de 4 à 8 donne patate (si la somme total est de cent cela équivaut à un pourcentage et si de milles ou dix milles cela l'inclut avec les virgules. exemple: pomme: 40, poire: 10 patate: 50. la pomme auras 40% de chance d'être tirés)

pour poser la question de la semaine suffit de mettre un @everyone et d'être modo