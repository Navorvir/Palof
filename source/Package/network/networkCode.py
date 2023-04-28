import socket
import json

# Créé par Nathan


# Codes de communication
CODE_DISCONECTED: int = 0
CODE_START_GAME: int = 1
CODE_GAME_DATA: int = 2
CODE_STOP_GAME: int = 3
CODE_COUPS: int = 4
CODE_ERROR: int = -1
CODE_SETTINGS: int = -2


class NetowrkObject(object):
    """Objet de base client avec des méthodes pour les échanges réseaux.
    """

    def __init__(self, socket : socket.socket, macSever : str, port : int) -> None:
        """Méthode d'initialisation de l'objet NetowrkObject

        Args:
            socket (socket.socket): objet socket utiliser pour les méthodes de cet objet
            macSever (str): adresse mac du serveur
            port (int): port où le socket écoute
        """
     
        self.MAC_SERVER : str =  macSever
        self.PORT : int = port
        self.surchage : dict = {"code":None,"data":None}
        self.run = True

        self.socket : socket.socket = socket
 
    def send(self, msg) -> None:
        """Permet d'envoyer des données sur un serveur (défénis lors du start)

        Args:
            msg : données a envoyé au serveur
        """

        if not self.socket._closed:
            try:
                self.socket.send(msg.encode())
            except:
                pass

    def surchageData(self, code : int, data):
            self.surchage : dict = {"code":code,"data":data}


    def sendData(self, code : int, element) -> None:
        """Envoie des requètes structurées en json avec la clé code et data

        Args:
            code (int): le type de requète
            element : élément envoyé
        """
        if self.surchage["code"] != None:
            self.send(json.dumps({"code" : code, "data" : element}) + json.dumps(self.surchage))
            self.surchage = {"code":None,"data":None}
        else:
            self.send(json.dumps({"code" : code, "data" : element}))

    def surchageRequest(self, probleme :bytes | str) -> list:
        """Permet de sépérarer les requetes si on en reçoit plusieurs à la fois. Par exemple:
           b"{"code":1,"data" : "test"}{"code":1,"data" : "test"}"

        Args:
            probleme (bytes | str): élément qui pose problème pouvant être une double requête

        Returns:
            list: contient soit les requetes séparées où rien si ce n'est pas des requetes collées
        """
        probleme = str(probleme)
        if probleme:
            probleme = probleme[:-1]
            requetes = probleme.split('{"code":')
            if len(requetes) > 1:
                return ['{"code":'+requete for requete in requetes[1:]]
        return []

    def checkJson(self, data : str | bytes) -> dict:
        """Permet de vérifier si on peut transformer la requete en format json puis 
           vérifier si elle contient bien la clée code et data et renvoyer le dictionnaire

        Args:
            data (str | bytes): donnée à vérifier et à transformer

        Returns:
            dict: si tout s'est bien passé renvoyé les données en dictionnaire sinon renvoyer
            {"code" : None, "data":[les données qui fonctionne pas]}
        """

        if data:
            try:
                data = json.loads(data)
            except: pass
            else:
                if "code" in data and "data" in data:
                    return data
            
                
        return {"code" : None, "data":data}

    def receve(self) -> dict:
        """Gère la réception des données du socket

        Returns:
            dict: dictionnaire qui contient les données provenant d'un autre socket
        """
        if not self.socket._closed and self.run:

            data = self.socket.recv(1024)
            return self.checkJson(data)
        else:
            return {"code":None,"data":None}