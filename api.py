"""Programme qui communique avec le serveur"""



import requests

##test
#test2
url_initial = 'https://python.gel.ulaval.ca/quoridor/api/'

def lister_parties(idul):
    """Lister les parties"""
    rep = requests.get(url_initial+'lister/', params={'idul': idul})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep.keys():
            raise RuntimeError(rep['message'])
        return rep['parties']
    return f"Le GET sur {url_initial+'lister/'} a produit le code d'erreur {rep.status_code}."


def débuter_partie(idul):
    """Débuter une partie"""
    rep = requests.post(u+'débuter/', data={'idul': idul})
    if rep.status_code == 200:
        rep = rep.json()
        if 'message' in rep.keys():
            raise RuntimeError(rep['message'])
        return (rep['id'], rep['état'])
    return f"Le POST sur {url_initial+'débuter/'} a produit le code d'erreur {rep.status_code}."


def jouer_coup(id_partie, type_coup, position):
    """Jouer un coup"""
    rep = requests.post(url_initial+'jouer/', data={'id': id_partie, 'type' : type_coup,
                                          'pos' : position})
    if rep.status_code == 200:
        rep = rep.json()
        if 'gagnant' in rep.keys():
            raise StopIteration(rep['gagnant'])
        if 'message' in rep.keys():
            raise RuntimeError(rep['message'])
        return rep['état']
    return f"Le POST sur {url_initial+'jouer/'} a produit le code d'erreur {rep.status_code}."