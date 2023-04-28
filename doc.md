# Description technique du projet


## La Physique du jeu 
La physique du jeu fonctionne à partir de la bibliotèque pygame .La bibliotèque pygame possède des objets Rect qui coorespondent à des rectangle et qui peuvent détecter si ils rentrent en collision avec d'autre objet de type Rect ou avec des points .Grâce à cela, nous pouvons premièrement détecter les collisions qui se déroule dans le jeu mais le problème est que nous pouvons utiliser seulement des rectangle pour former les collisions, cependant, notre personnage est une palourde donc un rectangle ne correspond pas à sa forme et nous empêche alors d'obtenir une physque proche de la réalité .C'est alors que nous avons deux choix pour effectuer les collisions de la palourde, le premier est de placer plusieurs Rect sur la palourde afin de se rapprocher d'un cercle, et le second est deplacer plusieurs points autour de la palourde et ainsi détecté les collisions avec les Rect des autre objets .Nous avons alors finalement choisi de garder la seconde option permettant de se rapprocher le plus possible de la forme de notre palourde

Image de la palourde avec ses points de collision

<img src="https://user-images.githubusercontent.com/116309446/235143496-8c5c31ea-ba0a-4f39-a7cd-3370ac10744d.png" alt="My cool logo" width="300"/>

Pour ce qui est de la réaction aux collision, nous essayons dans un premier temps de détecter quelle type de collision nous avons entre une collision avec le sol, une collision avec le côté droit d'un mur ou le côté gauche d'un mur et une collision avec la bas d'un Rect .Après que la palourde détecte une collision, en fonction du type elle va mettre sa vitesse à la racine carré de son oposée ou juste la remettre à 0 .

De plus, nous avons aussi ajouté un moyen pour la palourde de tourner sur elle même et donc subir la gravité lorsque se trouve sur le sol sans faire de mouvement

Cependant la physique n'est pas parfaite, Nous pouvons encrore trouver quelque bugs de collision avec les murs et avec le sol, ce qui arrive lorsque'la palourde avance à une trop grande vitesse ou entre en collision avec un Rect dans le mauvais angle

### La Partie Reseau 
Le reseau fonctionne en Bluetooth par l'intermédiaire de la library socket. De plus, la gestion du réseau c'est à dire traiter les réponses et envoyer les requetes fonctionne grâce à la library selector (la réception) et threading. 


### Les mouvements du jeu
Afin d'avoir un mouvement qui ressemble à celui d'un objet ovale qui roule, nous avons utilisé la fonction cosinus étant donné que sa courbe ressemble à un grand point à celle de l'accélération d'un objet ovale qui roule en fonction de son angle de rotation .Avec la valeur de cosinus, nous ajoutons une valeur suplémentaire correspondant à la force de la palourde qui est utilisé afin de se déplacer

<img src="https://user-images.githubusercontent.com/116309446/235167732-ee1b32a9-7e25-4862-acdd-ca46155a0562.jpg" alt="My cool logo" width="200"/>


### La caméra
Nous faisons l'usage d'une caméra dans notre jeu, pour cela, nous devons faire déplacer tous les objets se trouvants dans la carte actuel, puis nous affichons et testons les collisions de seulement ceux qui se trouve à une certaine distance de la palourde, nous pouvons le savoir grâce à une recherche dichotomique .Donc lors des déplacements de la palourde nous ne devons pas trop changer les coordonnées de la palourde parce que sinon la palourde finira par être afficher en dehors de la limite de l'écran daffichage (vous pouvez vous référencier au schéma ci-dessous) .Pour contrer cela, notre palourde possède deux groupes deux variable de coordonnée, le prier est regroupe la variable x et y (qui correspond alors à l'endroit où la palourde s'affichera sur l'écran) et le second regroupe les variable xCamera et yCamera (qui correspond aux coordonnées de la caméra) .Alors lorsque la palourde se déplace, les coordonnées xCamera et yCamera sont ceux qui change alors kes varialbel x et y reste les même à part lorsque la palourde rentre en collision, ses coordonnées x et y sont changer afin de pouvoir effectuer les collision (mais sont remis à leur valeur d'origine après un mouvement fluide de la camera)

<img src="https://user-images.githubusercontent.com/116309446/235170924-1d803e5d-6fc7-4a2e-9d93-f3046e7f6ce7.PNG" alt="My cool logo" width="800"/>


## Le Reseau Bluetooth
Le réseau était une partie assez complexe et très intéressante à la fois car d'une part j'avais jamais utilisé les bibliothèques threading et socket, mais d'une autre part ce projet m'a permit d'apprendre beaucoup sur la programmation concurrentielle et surtout les interfaces réseaux Bluetooth en Python. 


### Requète Json
Les requètes se présentent sous la forme d'un format JSON contenant une clé **"code"** pour la siginifcation de la requète et une clé **"data"** pour les données envoyées.

<img src="https://user-images.githubusercontent.com/86235354/235190388-9e52aa9b-90a9-41aa-a49d-0f68ffd4050c.png" alt="requete" width="200"/>


### Le Threading
L'une des première notion importante est la programmation concurrentielle qui permet à l'ordinateur de faire plusieurs taches à la fois comme par exemple en utilisant des Thread. Ce type de programmation peut être comparé à un restaurant de burger. Par exemple, vous programmez de manière linéaire chaques étapes du burger se fait à la suite ainsi si je prends 2 minutes pour chaques étapes (griller le pain, cuire le steak...) à la fais je vais arriver à 12min si j'en ai 6. Si maintenant, je le fais de manière concurrentielle, je lance mais steak à cuire puis en même temps je commence à cuire mon pain et par conséquence à la place de prendre 12min je vais prendre 3-4 minutes. De plus le threading est nécessaire car sans ça le jeu ne pourrait pas tourner en même temps et recevoir les nouvelles données en arrière-plan sans avoir de latence.


### Les Selectors
Cette technologie permet la gestion des réponses de manière efficace pour pouvoir attendre les réponses des autres interfaces en même temps sans utiliser une boucle par connexion. Cette bibliothèque fonctionne avec les méthodes **register** et **unregister permettant d'identifier qui envoie la requête. Elle attend une réponse pour commencer après à rechercher une autre réponse.

Du cotés serveur, elle se comporte en deux étapes une requete qui entre chez le serveur et demande à se connecter activer la méthode **acceptClient** qui s'occupera de l'initialisation de ce nouveau client avec notemment l'objet **InteractClient** et si une requete arrive et qu'il est déja connu de le selector envoit les données vers la méthode **read** propre à l'objet **InteractClient**.

Du cotés client une seule étape est nécessaire car dés lors il est connecté au serveur il reçoit toujours le même type de requete.

Cependant ce qui peut survenir est que la requète d'avant et celle la requète actuelle du client se retrouve ensemble dans la réception chez le serveur ce qui peut donner par exemple *'{"code" : X, "data" : X}{"code" : X, "data" : X}'*. Ceci est une forme de surcharge qui pousse à vérifier si il y a plusieurs requete en vérifiant si *'{"code"'* est plusieurs fois. Cette mécanique est utiliser pour envoyer plusieurs requètes cotés client comme par exemple lorsqu'un joueur pousse un autre joueur.


### Socket
Le seveur bluetooth tourne sur le port **30** pour fonctionner avec une adresse MAC propre à chaque machine.

Pour que le socket focntionne en bluetooth, il comporte 3 arguments :
- **AF_BLUETOOTH** : correspond au protocole Bluetooth
- **SOCK_STREAM** : le type de socket (celui par defaut)
- **BTPROTO_RFCOMM** -> Protocole pour accepter les interfaces réseaux(accepte (bdaddr, channel))


### Server
La partie complexe était de gérer la partie client host de l'objet serveur et la partie gestions des autres clients donc la nécessité de bien s'organiser en créant un objet de base réseau **NetowrkObject** et de créer un objet spécial pour la gestion de chaque client coté serveur **InteractClient** avec un objet principal **Server**. La gestion de la réponse d'un client se fait par un dictionnaire **MANAGEMENT_RESPONSE** qui contient un code lié à une méthode.


### Client
La première chose que fait le client après avoir initialisé est la demande de son ID et des paramètres pour que le serveur et le client fonctionne bien et travaille sur les mêmes choses.



## Game Design

### Traitement json
Les maps des niveaux et les éléments des différentes scènes sont stockés dans des fichiers json sous forme de dictionnaire. Pour chaque élément ont vérifie si il possède des coordonnées, une image ou une couleur (si il n'y en a pas, la couleur par défaut est le noir). Le rect et l'image de chaque élément est mis dans une liste en fonction de la couche auquel il appartient (1er plan, 2eme plan, 3eme plan).  De plus si des éléments ont un type (comme les boutons) et que ce type existe un objet est instancié. Cette liste est envoyée à la caméra quand la map est chargé pour qu'elle les affiches.


### Menu
Le menu est composé de différentes scènes, l'écran titre, l'écran du choix du mode, l'écran du choix du niveau, et l'écran pour se connecter en réseau. Pour changer de scène change la variable map qui stocke le chemin d'accès du fichier json correspondant et on charge la carte. Pour savoir quand changer scène on regarde les collisions de la palourde avec les bords de l'écran et on regarde les différents boutons. Ces derniers peuvent prendre une fonction et des arguments et lorsqu'ils sont presser ils les exécutent.
