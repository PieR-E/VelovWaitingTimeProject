# Velov Waiting Time Project

Application permettant à un utilisateur de connaitre les temps d'attentes moyens de stations Velov à partir d'une adresse indiquée.

Frontend en React (TS), Backend en Node/Express (TS), BDD postgreSQL (avec des scripts python pour le fetch et la mise à jour des données statistiques, fetch depuis l'API Gouvernmental Velov, et une API de carte tel Google Maps).

## Objectif
Imaginons le scénario suivant : il est 20H. Je rentre du sport ou d'un after-work avec mon Velo'v et j'habite à un endroit trés animé du centre ville de Lyon. Je sais qu'il y a quatre stations Velo'v à proximité : les stations A,B,C,D. Je sais aussi que chaque fois que je rentre chez moi à cette heure là : les quatres stations son complètes. En outre, j'ai remarqué que le délai de rafraichissement de l'application mobile est trop long pour que les disponibilités affichées sur mon smartphone reflètent la réalité ... Alors voilà, j'attends devant la station A, la plus proche de mon domicile et je ne sais pas quoi faire : dois-je attendre ici ; rejoindre une des station B,C,D pour plutôt y attendre la bas ; tourner selon un certain sens entre les stations A,B,C et D en espérant qu'une place se libère ; m'éloigner jusqu'a une autre station ? 
Le but de ce projet et de répondre à cette question d'une manière objective. Et de le faire automatiquement pour n'importe quelle adresse et horaire.

## TODO

1 : Certaines stations n'ont pas de nom. Par exemple, la numéro 2023, situéé au 1, quai Perrache, présente un name
qui vaut None.

2 : une mise ) jour automatiques toutes les 10 minutes même si aucun vélo n'é été pris ou déposé => problématique pour estimer un temps d'attente donc à traiter.
