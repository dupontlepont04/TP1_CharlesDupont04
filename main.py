""" Prgramme qui permet de jouer au jeu Quoridor contre un serveur soit automtisé ou en mode manuel
    avec soit un affichage ASCII ou un affichage graphique"""

# Importation des modules nécessaires

import argparse
import copy
import api
import quoridorx

def analyser_commande():
    """Permet d'analyser ce que l'utilisateur
        écrit dans la ligne de commande"""

    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 3')
    parser.add_argument(metavar='idul', default='idul du joueur', dest='idul',
                        help='IDUL du joueur.')
    parser.add_argument('-a', '--automatique', dest='auto', action='store_const',
                        const=sum, default=False,
                        help='Activer le mode automatique.')
    parser.add_argument('-x', '--graphique', dest='graph', action='store_const',
                        const=sum, default=False,
                        help='Activer le mode graphique.')
    args = parser.parse_args()
    return args


def afficher_damier_ascii(dic):

    """Afficher le damier sur l'état de jeu"""

    premiere_ligne = 'Légende: 1=' + dic['joueurs'][0]['nom'] \
                     + ', 2=automate \n' + '   ' + '-' * 35 + '\n'
    plateau = [['.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' ', ' ', ' ',
                '.', ' | ', '\n',
                ' ', ' ', '|',
                ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|',
                ' ', '\n'
                ] for ligne in range(9)]

    y_1 = dic["joueurs"][0]['pos'][1]
    x_1 = dic["joueurs"][0]['pos'][0]
    y_2 = dic["joueurs"][1]['pos'][1]
    x_2 = dic["joueurs"][1]['pos'][0]

    plateau[8 - y_1 + 1][(x_1 - 1) * 4] = '1'
    plateau[8 - y_2 + 1][(x_2 - 1) * 4] = '2'

    for indice in range(9):
        plateau[indice].insert(0, str(9 - indice) + ' | ')

    plateau.append(['--|-----------------------------------\n'])
    plateau.append([' ', ' ', '| ', '1', '   2', '   3', '   4'
                       , '   5', '   6', '   7', '   8', '   9'])
    plateau[8] = plateau[8][:36]

    for pos in dic['murs']['horizontaux']:
        x, y = pos
        for e in range(7):
            plateau[9 - y][35 + x * 4 + e] = '-'

    for pos in dic['murs']['verticaux']:
        x, y = pos
        plateau[9 - y - 1][x * 4 - 5] = '|'
        plateau[9 - y - 1][34 + x * 4] = '|'
        plateau[9 - y][x * 4 - 5] = '|'

    print(premiere_ligne + ''.join(''.join(i for i in ligne) for ligne in plateau) + '\n')
