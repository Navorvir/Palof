import socket
from time import sleep
import selectors
import threading


try:
    from Package.network.usily import showMessage, convertBase36ToHex, formatAddress
    from Package.network.networkCode import *
except:
    from usily import showMessage, convertBase36ToHex, formatAddress
    from networkCode import *


class Client(NetowrkObject):
    """Objet coté client permettant de communiquer avec le serveur du jeu

    Args:
        NetowrkObject (_type_): _description_
    """

    def __init__(self, palourde) -> None:
        """Méthode d'initialisation de l'objet Client

        Args:
            palourde (Palourde): objet palourde du joueur HOST
        """
        super().__init__(socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM),"",30)
        # AF_BLUETOOTH -> Bluetooth
        # SOCK_STREAM -> Type socket (defaut)
        # BTPROTO_RFCOMM -> Protocole (accepte (bdaddr, channel))
        
        # ============= CONSTANTES ============
        self.LOCK = threading.Lock()

        self.PALOURDE = palourde

        self.MANAGEMENT_RESPONSE : dict = {
            CODE_START_GAME : self.startGame,
            CODE_STOP_GAME : self.stopGame,
            CODE_GAME_DATA : self.setData,
            CODE_SETTINGS : self.setSettings,
            CODE_DISCONECTED : self.close,
            CODE_COUPS : self.PALOURDE.coupSubi,
        }

        self.TIME_SPEED_REQUEST : float = 0.01 # La vitesse en seconde entre chaque traitement de requetes

        # ============= VARAIABLES =============
   

        self.selector : selectors.DefaultSelector = selectors.DefaultSelector()

        self.ID_CLIENT_HOST : str = None
        self.data : dict = {}

        self.connectionDone : bool = False
        self.gameStarted : bool = False

        self.levelName : str = ""
        self.mode : str = ""

        # ============= PARAMETRAGE =============
        # PARAMETRES SELECTOR
        self.selector.register(self.socket, selectors.EVENT_READ, self.read)

    # ============== METHODES =================

    # Méthode gestion du client
    def setMacServerAddress(self, code : str) -> None:
        """Mettre en place l'adresse mac du serveur à partir du code du serveur

        Args:
            code (str): texte qui provient du serveur pour pouvoir y se connecter
        """

        self.MAC_SERVER = formatAddress(convertBase36ToHex(code))

    def read(self, *args) -> None:
        """Méthode utilisée pour la bibiothèque selector qui s'execute à chaque respection de nouvelles données
        """

        data = self.receve()

        if data["code"] != None and "data" in data and data["code"] in self.MANAGEMENT_RESPONSE:
            
            self.MANAGEMENT_RESPONSE[data["code"]](data["data"])
        else:
            listRequest = self.surchageRequest(data["data"])
            if listRequest:
                for request in listRequest:
                    data = self.checkJson(request)
                    if data["code"]:
                        self.MANAGEMENT_RESPONSE[data["code"]](data["data"])
            else:
                showMessage("Connexion fermée")
                self.socket.close()
                self.selector.unregister(self.socket)
                self.connectionDone = False
                self.gameStarted = False

    def startClient(self) -> None:
        """Lance la conexion du client au serveur (doit défénir avant l'adresse du serveur)
        """
        try:
            self.socket.connect((self.MAC_SERVER, self.PORT))
            self.connectionDone = True
        except OSError: # le bluetooth n'est pas activé
            showMessage("Activer le bluetooth ou le serveur n'est pas lancé")
            self.problem = "Activer le bluetooth ou le serveur n'a pas été lancé"
            return False
        else:
            threading.Thread(target=self.boucleRecept, daemon=True).start()
            self.problem = ""
            return True
            

    def boucleRecept(self):
        self.sendData(CODE_SETTINGS, "id")
        showMessage("Le client se lance")
        threading.Timer(2.0, self.checkId).start() # si il y a un problème de requete

        while self.connectionDone:
            events = self.selector.select()
                        
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def close(self, data : str = "Le serveur s'arrete") -> None:
        """Fermer le client

        Args:
            data (str, optional): texte affichant la cause de cette feremture. Defaults to "Le serveur s'arrete".
        """
        self.connectionDone = False
        self.socket.close()

        showMessage(data)
    
    def checkId(self)-> None:
        """Vérifie si l'adresse MAC du serveur a bien été défnis et si ce n'est pas le cas il envoie une nouvelle
           requête 
        """
        if self.ID_CLIENT_HOST == None:
            self.sendData(CODE_SETTINGS, "id")
    
    # Méthode gestion du jeu  
    def gameBoucle(self) -> None:
        """Lance la boucle qui gère l'envoi des données toutes les x secondes
        """

        showMessage("Lancement de la boucle pour les données du jeu")
        while self.gameStarted and self.connectionDone:

            self.LOCK.acquire() # permet prendre la main sur un l'envoi des données
            x, y =self.PALOURDE.updateTotalCo()
            self.sendData(CODE_GAME_DATA, {"x" : x,"y" : y,"angle" : self.PALOURDE.angle, "sante": self.PALOURDE.sante})
            self.LOCK.release()
            sleep(self.TIME_SPEED_REQUEST)
        self.gameStarted = False

    def startGame(self, *args) -> None:
        """Permet de lancer le jeu 
        """

        if not self.gameStarted:
            self.gameStarted = True
            threading.Thread(target=self.gameBoucle, daemon=True).start()
   
    def getData(self) -> dict:
        """Retourne 

        Returns:
            dict: _description_
        """
        return self.data.copy()
    

    # Gestionnaire requetes
    def stopGame(self, *args)-> None:
        """Arrête le jeu
        """
        self.close("le jeu est terminé")

    def setSettings(self, data : dict) -> None:
        """Paramètre les données utiles tel que l'id du client et le level

        Args:
            data (dict): dictionnaire qui contient les données pour le bon paramètrage
        """

        self.ID_CLIENT_HOST = data["id"]
        self.mode = data["mode"]
        self.levelName = data["levelName"]

    def setData(self, data : dict) -> None:
        """Met à jour la variable qui contient les données des autres palourdres

        Args:
            data (dict): les nouvelles données
        """
        self.data = data

    def sendTemporyParameter(self, parameter,value,idClient)->None:
        self.LOCK.acquire()
        self.surchageData(CODE_COUPS, {"idClient" : idClient, parameter : value})
        self.LOCK.release()
