# Palof est un jeu de plateforme multijoueurs où l’on contrôle une palourde .Le jeu est composé de deux modes de jeu différent, le premier est le mode coopération où tous les joueurs doivent réussir à arriver à la ligne d’arriver, le second est le mode versus où les joueurs doivent se pousser entre eux afin de briser les palourdes des autres joueurs .Ces deux modes de jeu se jouent alors en multijoueurs via le bluetooth des ordinateurs . 

## La Physique du jeu 
La physique du jeu fonctionne à partir de la bibliotèque pygame .La bibliotèque pygame possède des objets Rect qui coorespondent à des rectangle et qui peuvent détecter si ils rentrent en collision avec d'autre objet de type Rect ou avec des points .Grâce à cela, nous pouvons premièrement détecter les collisions qui se déroule dans le jeu mais le problème est que nous pouvons utiliser seulement des rectangle pour former les collisions, cependant, notre personnage est une palourde donc un rectangle ne correspond pas à sa forme et nous empêche alors d'obtenir une physque proche de la réalité .C'est alors que nous avons deux choix pour effectuer les collisions de la palourde, le premier est de placer plusieurs Rect sur la palourde afin de se rapprocher d'un cercle, et le second est deplacer plusieurs points autour de la palourde et ainsi détecté les collisions avec les Rect des autre objets .Nous avons alors finalement choisi de garder la seconde option permettant de se rapprocher le plus possible de la forme de notre palourde
![image](https://user-images.githubusercontent.com/116309446/235143496-8c5c31ea-ba0a-4f39-a7cd-3370ac10744d.png)



## La Partie Reseau 
Le reseau fonctionne en Bluetooth par l'intermédiaire de la library socket. De plus, la gestion du réseau c'est à dire traiter les réponses et envoyer les requetes fonctionne grâce à la library selector (la réception) et threading. 

