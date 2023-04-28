import socket
import selectors
from time import sleep
import threading

try:
    from Package.network.usily import showMessage, checkValueList, getMacBluetooth
    from Package.network.networkCode import *
except:
    from usily import showMessage, checkValueList, getMacBluetooth
    from networkCode import *



class Server:
    """Objet serveur pemettant la gestion d'un serveur de jeu palourde
    """

    def __init__(self, palourde) -> None:
        """Méthode pour initialiser l'objet 

        Args:
            palourde (Palourde): objet palourde du joueur HOST
        """

        # ============= CONSTANTES ============
        # PARAMETRES SERVER
        self.PORT : int = 30
        self.MAC_SERVER, self.CODE  = getMacBluetooth()

        self.TIME_SPEED_REQUEST : float = 0.01 # La vitesse en seconde entre chaque traitement de requetes
        self.TIME_SPEED_RESPONSE : float = 0.002 # La vitesse en seconde entre chaque traitement de reponses

        self.ID_CLIENT_HOST : int = 1

        self.PALOURDE = palourde

        # ============= VARAIABLES =============
        self.lastId : int = 1
        self.gameStarted : bool = False

        self.data : dict = {self.ID_CLIENT_HOST : {'x' : 0, 'y': 0, "angle" : 0, "connected":True, "sante":100}}
        self.connectedClient : dict = {}

        self.levelName = ""
        self.mode = ""

        self.serverRun = False

        self.socket : socket.socket= socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        # AF_BLUETOOTH -> Bluetooth
        # SOCK_STREAM -> Type socket (defaut)
        # BTPROTO_RFCOMM -> Protocole (accepte (bdaddr, channel))

        self.selector : selectors.DefaultSelector = selectors.DefaultSelector()

        # self.hostClient = HostClient()

        # ============= PARAMETRAGE =============
        # PARAMETRES SOCKET
        self.socket.settimeout(1)
        self.socket.bind((self.MAC_SERVER, self.PORT))
        self.socket.listen(100)
        self.socket.setblocking(False)

        # PARAMETRES SELECTOR (pour la réception)
        self.selector.register(self.socket, selectors.EVENT_READ, self.acceptClient)

    # ============ METHODES ==============

    # Methodes de Gestion du serveur
    def startServer(self) -> None:
        """Permet de lancer le serveur et la liaison de client
        """
        showMessage(f"Le serveur se lance sur l'adresse '{self.MAC_SERVER}' au port {self.PORT}")
        showMessage(f"Le code est {self.CODE}")
        self.serverRun = True

        while self.serverRun:
            events = self.selector.select()
            
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

            sleep(self.TIME_SPEED_RESPONSE)
    
    def close(self, text : str ="Le serveur s'arrete") -> str:
        """Arrête le serveur avec un message

        Args:
            text (str, optional): message affiché lors de l'arrêt. Defaults to "Le serveur s'arrete".

        Returns:
            str: raison de l'arrêt
        """
        self.sendAll(CODE_DISCONECTED, text)
        showMessage(text)
        self.serverRun = False

        # Remet à zéro

        self.data : dict = {self.ID_CLIENT_HOST : {'x' : 0, 'y': 0, "angle" : 0, "connected":True, "sante":100}}
        self.connectedClient : dict = {}

        self.gameStarted = False
        self.lastId : int = 0

        self.socket.close()

        return text

    def sendAll(self, code : int, data) -> None:
        """Envoie à tous les clients la même requete en même temps (par les threads)

        Args:
            code (int): code de la requete
            data (n'importe): données transmises
        """
        listThreads : list = []

        # On lance les threads
        for socket in self.connectedClient.copy().values(): # évite les erreurs de modification de variable lors de la boucle
            threadRequest = threading.Thread(target=socket.sendData, args= (code, data,))
            threadRequest.start()
            listThreads.append(threadRequest)

        # Pour attendre tous les thread
        for threadRequest in listThreads:
            threadRequest.join()  

    def acceptClient(self, *args) -> None:
        """Mettre en place les systèmes pour la gestion de ce nouveau client
        """

        if self.serverRun:
            conn, addr = self.socket.accept()
            idClient = self.generateId()

            client = InteractClient(self, conn, addr, idClient)

            self.connectedClient[client.ID_CLIENT] = client
            client.socket.setblocking(False)        
            self.selector.register(client.socket, selectors.EVENT_READ, client.read) # en mode lecture

            showMessage("Nouvelle connexion : ", client.ID_CLIENT, "avec l'adresse",addr[0])

    def delPlayer(self, id : int):
        """Supprime un joueur par son id

        Args:
            id (int): id du joueur qui doit disparaitre
        """

        if id in self.connectedClient:
                self.connectedClient.pop(id)
        if id in self.data.keys():
            self.data.pop(id)

    # Methodes de Gestion du jeu
    def setTypeGame(self, mode: str, levelName : str) -> None:
        """Met en mémoire le level à joueur dans un but de l'envoyer aux clients

        Args:
            mode (str): mode du jeu 
            levelName (str): nom du fichier du level
        """
        self.levelName = levelName
        self.mode = mode

    def startGame(self) -> None:
        """Lance le jeu en envoyant une requete à tous les clients 
        """

        self.gameStarted = True
        showMessage("Le jeu se lance")
        threading.Thread(target=self.boucleGame, daemon=True).start()
        self.sendAll(CODE_START_GAME, "Le jeu se lance")

    def boucleGame(self) -> None:
        """Lancement de la boucle qui envoie les données du jeu tous les x secondes
        """

        while self.gameStarted and self.serverRun:
            x, y =self.PALOURDE.updateTotalCo() # le joueur host
            self.updateDataClientHost(x, y, self.PALOURDE.angle, self.PALOURDE.sante)
            self.sendAll(CODE_GAME_DATA, self.data)

            sleep(self.TIME_SPEED_REQUEST)
    
    def addTemporyParameter(self,)->None:
        self.data

    def updateGameData(self, idClient : int, x : int | float, y: int | float , angle: int |float, sante : int |float) -> None: 
        """Permet de mettre à jour les données du jeu d'un client

        Args:
            idClient (int): l'id du client
            x (int | float): la coordonnée x dans la partie
            y (int | float): la cooronnée y dans la partie
            angle (int | float): l'angle du joueur dans la partie
            sante (int | float): sante du joueur dans la partie
        """
        if idClient not in self.data:
            self.data[idClient] = {}

        self.data[idClient]["x"] = x
        self.data[idClient]["y"] = y
        self.data[idClient]["angle"] = angle
        self.data[idClient]["sante"] = sante
        self.data[idClient]["connected"] = True

    def stopGame(self) -> None:
        """Arrête le jeu pour tous les joueurs
        """
        self.sendAll(CODE_STOP_GAME, "Le jeu s'arrête'")

    # Methodes Client Host
    def generateId(self) -> int:
        """Augmente le nombre de joueur connecté de 1 (pour créer les ids)

        Returns:
            int: le dernier id donné à un client
        """
         
        self.lastId += 1

        return self.lastId
    
    def getData(self) -> dict:
        return self.data.copy()
    
    def updateDataClientHost(self, x : int | float , y : int | float, angle: int | float, sante: int | float) -> None:
        """Met à jou les données envoyées par le serveur du joueur HOST

        Args:
            x (int | float): coordonnée x du joueur host
            y (int | float): coordonnée y du joueur host
            angle (int | float): angle du joueur host
            sante (int | float): sante du joueur host
        """

        self.data[self.ID_CLIENT_HOST] = {"x" : x, "y" : y, "angle": angle, "connected":True, "sante":sante}

    def sendTemporyParameterFromOtherClient(self,idClient, data)->None:
        if int(idClient) == self.ID_CLIENT_HOST:
            self.PALOURDE.coupSubi(data)
        elif idClient in self.connectedClient :
            self.connectedClient[idClient].surchageData(CODE_COUPS, data)

    def sendTemporyParameter(self, parameter,value,idClient)->None:
        if idClient in self.connectedClient :
            self.connectedClient[idClient].surchageData(CODE_COUPS, {"idClient" : idClient, parameter : value})
            sleep(self.TIME_SPEED_REQUEST*2)

class InteractClient(NetowrkObject):
    """Objet qui représente un client qui permet la gestion d'un client coté serveur
    """

    def __init__(self, server : Server, connection : socket.socket, address : tuple, idClient : int) -> None:
        """Méthode qui initialise l'objet

        Args:
            server (Server): l'objet serveur qui s'occupe de la gestion de ce client
            connection (socket.socket): socket du client (permet de communiquer)
            address (tuple): adresse MAC du client
            idClient (int): id du client
        """
        super().__init__(connection, address[0], address[1])

         # ============= CONSTANTES ============
        self.ID_CLIENT : int = idClient
        self.LOCK = threading.Lock()

        self.MANAGEMENT_RESPONSE : dict = {
            CODE_SETTINGS : self.sendSettings,
            CODE_GAME_DATA : self.receveGameData,
            CODE_COUPS : self.receveCoups,
        }
        
        # ============= VARAIABLES =============
        self.server : Server = server


    # ============== METHODES =================

    # Méthode gestion du client
    def read(self, *args) -> None:
        """Est exécuté par le selector lorsqu'il reçoit une requete de ce client
        """

        data : dict = self.receve()

        if data["code"] != None and "data" in data and data["code"] in self.MANAGEMENT_RESPONSE:
            threading.Thread(target=self.management, args=(data["code"],data["data"],)).start()
          
        else:
            listRequest = self.surchageRequest(data["data"])
            if listRequest:
                for request in listRequest:
                    data = self.checkJson(request)

                    if data["code"]:
                        self.MANAGEMENT_RESPONSE[data["code"]](data["data"])
            else:
                showMessage("Le client", self.ID_CLIENT, "se ferme")
                self.server.selector.unregister(self.socket)
                self.socket.close()

                if self.ID_CLIENT in self.server.data:
                    self.server.data[self.ID_CLIENT]["connected"] = False
                if self.ID_CLIENT in self.server.connectedClient:
                    self.server.connectedClient.pop(self.ID_CLIENT)

    def management(self, code : int,  data) -> None :
        """Gère le fonctionnement des requetes reçus

        Args:
            code (int): code pour le type de requete
            data (n'importe): donné provenant de la requete
        """
        
        self.MANAGEMENT_RESPONSE[code](data)

    # Méthode pour la fonction management (répondre à la requete)
    def sendSettings(self, *args) -> None:
        """Envoie les paramètres nécessaires pour le fonctionnement du client
        """

        self.sendData(CODE_SETTINGS, {"id" : self.ID_CLIENT, "levelName" : self.server.levelName, "mode":self.server.mode})

    def receveGameData(self, data :dict, *args) -> None:
        """Permet de vérifier que la requete a les bons paramètres puis de mettre à jour les données du
           client coté serveur afin de renvoyer après

        Args:
            data (dict): les données du jeu qui sont renvoyées tous les x secondes
        """

        if checkValueList(("x", "y", "angle", "sante"),data.keys()) :
            self.server.updateGameData(self.ID_CLIENT, data["x"], data["y"], data["angle"],  data["sante"])

    def receveCoups(self,data)->None:
        self.LOCK.acquire()
        self.server.sendTemporyParameterFromOtherClient(data["idClient"], data)
        self.LOCK.release()
