from datetime import datetime
import psutil

# Créé par Nathan

def showMessage(text, *args) -> None:
    """Affiche un texte avec la date de l'affichage

    Args:
        text (n'importe quel type): élément à afficher
    """
    
    date = datetime.now().strftime('%H:%M:%S')
    print(f"[{date}]",text, *args)

def checkValueList(keys : list, list : list) -> bool:
    """Vérifie si dans une liste, il ya les éléments keys bien présentent

    Args:
        keys (list): éléments qui doivent être présents dans la list
        list (list): liste qui doit contenir les éléments

    Returns:
        bool: si tous éléments sont présents dans la liste, cela renvoie True sinon False
    """

    for key in keys:
        if key not in list:
            return False
    return True


def convertHexToBase36(hexValue : int) -> str:
    """Permet de convertir un nombre en base de 10 en base de 36

    Args:
        hexValue (int): nombre en base de 10 à convertir

    Returns:
        str: nombre en base de 36
    """
    hexValue = int(hexValue, 16)

    code = {
        0 : 0,
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        5 : 5,
        6 : 6,
        7 : 7,
        8 : 8,
        9 : 9,
        10 : "a",
        11 : "b",
        12 : "c",
        13 : "d",
        14 : "e",
        15 : "f",
        16 : "g",
        17 : "h",
        18 : "i",
        19 : "j",
        20 : "k",
        21 : "l",
        22 : "m",
        23 : "n",
        24 : "o",
        25 : "p",
        26 : "q",
        27 : "r",
        28 : "s",
        29 : "t",
        30 : "u",
        31 : "v",
        32 : "w",
        33 : "x",
        34 : "y",
        35 : "z",

    }
    result = []
    while hexValue >= 36:
        result.append(hexValue%36)
        hexValue = hexValue // 36
    result.append(hexValue % 36)

    return ("".join([str(code[l]) for l in result])).lower()

def convertBase36ToHex(base36 : str) -> int:
    """Convertit un nombre en base de 36 en base de 10

    Args:
        base36 (str): nombre en base de 36 à convertir

    Returns:
        int: nombre en base de 10
    """
    code = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 
    'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19, 'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29, 'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35}

    decimal = 0
    i = 0
    for n in base36.lower():
        decimal += code[n] * 36**i
        i += 1
    
    return hex(decimal)[2:]

def formatAddress(address : str) -> str:
    """Ajouter les deux points

    Args:
        address (str): adresse où il fait y ajouter les deux points

    Returns:
        str: addresse avec les deux points
    """

    # Ajoute des 0 si l'adresse manque à cause de la compression 36
    if len(address) < 12:
        address += "0"* (12 - len(address))

    address = address[:2 ]+ "".join( [":" +address[i:i+2]for i in range(2,11,2)])

    return address.upper()

def getMacBluetooth():
    """Donne l'addresse mac et le code

    Returns:
        tuple(str, str): donne l'addresse mac et le code 
    """
     
    address = ""
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if 'Bluetooth' in interface:
                if addr.family == psutil.AF_LINK:
                   address = addr.address
                   return address.replace("-",":"), convertHexToBase36(addr.address.replace("-",""))

if __name__ =="__main__":
    mac = "002200220022"
    convert = convertHexToBase36(mac)
    print(convert)
    convert = convertBase36ToHex(convert)
    print(convert)