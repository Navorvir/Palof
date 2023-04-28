<img src="https://user-images.githubusercontent.com/86235354/235141848-fd58dc04-27b8-4409-95d7-c04cdf88341c.png" alt="My cool logo" width="100"/>
Palof est un jeu de plateforme multijoueur où l’on contrôle une palourde. Le jeu est composé de deux modes de jeu différents, le premier est le mode coopération où tous les joueurs doivent réussir à arriver à la ligne d’arrivée, le second est le mode versus où les joueurs doivent se pousser entre eux afin de briser les palourdes des autres joueurs. Ces deux modes de jeu se jouent alors en multijoueurs via le Bluetooth des ordinateurs.
-

## Pré-requis
Il est nécessaire d'avoir une version python supèrieur à **python 3.10**. De plus, pour pouvoir lancer ce jeu vous aurez besoins de différentes bibliothèques tels que:
- une bibliothèque graphique : *pygame*, 
- des bibliothèques d'interface reseau : soket, *selectors*, *psutill* et *threading*
- des bibliothèques utilitaires : *time*, *os*, *sys*, *json*, *random* et *math*

Si la bibliothèque n'est pas installée, vous devez les installer par cette commande:
py -m pip <nom de la bibothèque python>

Si vous voulez jouer à plusieurs, vous devez choisir un joueur hôte qui permettra le lien entre tous les appareils. Pour ce faire, le joueur hôte doit s'appairer aux différents appareils clients pour permettre la connexion Bluetooth. Si vous ne savez pas comment faire **[cliquer ici!](https://support.microsoft.com/fr-fr/windows/coupler-un-p%C3%A9riph%C3%A9rique-bluetooth-dans-windows-2be7b51f-6ae9-b757-a3b9-95ee40c3e242)**

## Lancement

### Le joueur hôte:
Le joueur hote doit d'abord aller vers la *gauche* pour accéder au menu mode. Ici il doit choisir le mode qu'il veut jouer soit **les niveaux coopératifs** ou le mode **versus** en *cliquant dessus*.

<img src="https://user-images.githubusercontent.com/86235354/235151493-e0b61485-ea4a-4d1e-9ab8-26c16741b686.png" alt="My cool logo" width="400"/>

Ensuite si vous avez cliquer sur le **les niveaux coopératifs** il y a une étape de plus le choix du niveau où vous devez *cliquer* sur un **niveau**. A partir de ce moment vous devez avoir le menu si dessous qui vous propose de jouer en solo ou en multijoueur, vue que nous voullons jouer en multijoueur il faut *cliquer* sur le **bouton multijoueur**.

<img src="https://user-images.githubusercontent.com/86235354/235151566-5ea5451a-7ddf-4f5b-80d2-5e269c6df150.png" alt="My cool logo" width="400"/>

Cette dernière interface pour le joueur hote lui permettra de lancer le jeu quand tous les joueurs clients seront connectés en *cliquant* sur le bouton **lancer le jeu**. Le code qui s'affiche est important car il permet au client de se connecter au serveur car en réalité ce code représente l'adresse mac bluetooth du serveur en base 36.

<img src="https://user-images.githubusercontent.com/86235354/235151674-fc62c70c-dfed-42e2-a60f-6a6bb5d24f4a.png" alt="My cool logo" width="400"/>

### Les autres joueur clients:
En allant à gauche le joueur tombe sur le menu qui propose un champ de texte pour *écrire* le **code qui se trouve chez le joueur hôte**. Après avoir écrit le code en faisant attention au "o", "0" et "O" faites *entrer* pour lancer une tentative de connexion. Si le texte affiché dit que **"Le client s'est connecté. Attend que le serveur lance la partie..."**,  Bravo!! Vous avez réussis à vous connecter au joueur hote et il ne manque plus qu'il lance la partie. Sinon si le champ n'apparait, il faut juste se déplacer et il apparaitra ou si il affiche un autre texte cela peut venir que **le serveur n'a pas été lancé**, **le code n'est pas bon** ou que **le bluetooth n'est activé pas sur la machine**.

<img src="https://user-images.githubusercontent.com/86235354/235150065-ce04bc3a-bb9a-4ba3-98c3-73d018c3242d.png" alt="My cool logo" width="400"/>

## Les contrôles

- q / flèche directionnel gauche : rouler à gauche
- d / flèche directionnel droite : rouler à droite
- barre espace / flèche directionnel haut : sauter
- left shift : taper (s'active seulement dans le mode versus)
- double échap : retourner au menu

## liste des images utiliés :
-[background_palof.png](./source/Assets/Background/background_palof.png)
