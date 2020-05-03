import networkx as nx


class Quoridor:
    def __init__(self, joueurs, murs=None):
        # S'assurer que l'argument joueurs soit un itérable
        if not hasattr(joueurs, '__iter__'):
            # Sinon QuoridorError
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")

            # S'assurer que le nombre de joueurs est différent de deux
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux.")

            # S'assurer que le nombre de murs est entre 0 et 10
        if not (self.joueurs[0]['murs'] or self.joueurs[1]['murs']) in range(0, 11):
            raise QuoridorError("Le nombre de murs qu'un joueur peut placer est plus grand que 10,ou négatif.")

            # S'assurer que la position d'un joueur soit valide
        if isinstance(joueurs[0], dict) or isinstance(joueurs[1], dict):
            for i in joueurs[0].get('pos'):
                if i not in range(1, 10):
                    raise QuoridorError("La position d'un joueur est invalide.")
            for i in joueurs[1].get('pos'):
                if i not in range(1, 10):
                    raise QuoridorError("La position d'un joueur est invalide.")
            # Par défaut, aucun mur n'est placé sur le jeu
        if murs is None:
            self.murs = {'horizontaux': [],
                         'verticaux': []
                         }

            # S'assurer que l'argument murs soit un dictionnaire
        elif not hasattr(murs, '__dict__'):
            raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")

        self.joueurs = joueurs
        # première option : joueur est une chaîne de caractère
        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [{'nom': joueurs[0],
                             'murs': 10,
                             'pos': (5, 1)},
                            {'nom': joueurs[1],
                             'murs': 10,
                             'pos': (5, 9)}]

        # S'assurer que le total des murs placés soit égale à 20.
        if self.joueurs[0]['murs'] + \
                self.joueurs[1]['murs'] + \
                len(self.murs['horizontaux']) + \
                len(self.murs['verticaux']) != 20:
            raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20.")

            # S'assurer que la position verticales et horizontales des murs soient valides
            # Murs Horizontaux
        for murs_horizontaux in self.murs['horizontaux']:
            # Tuple de la position des murs horizontaux
            x, y = murs_horizontaux
            # Vérifier si chacun des positions sont dans l'intervalle demandé
            if x not in range(1, 9) or y not in range(2, 10):
                raise QuoridorError("La position d'un mur est invalide.")
                # Murs Verticaux
        for murs_verticaux in self.murs['verticaux']:
            x, y = murs_verticaux
            if x not in range(2, 10) or y not in range(1, 9):
                raise QuoridorError("La position d'un mur est invalide.")

    def __str__(self):

        grille = [['.', ' ', ' ', ' ',
                   '.', ' ', ' ', ' ',
                   '.', ' ', ' ', ' ',
                   '.', ' ', ' ', '.',
                   ' ', ' ', ' ', ' ',
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

        ligne1 = 'Légende: 1=' + self.joueurs[0]['nom'] + ', ' + '2=' + \
                 self.joueurs[1]['nom'] + '\n' + '   ' + '-' * 35 + '\n'

        grille[8 - self.joueurs[0]['pos'][1] + 1][(self.joueurs[0]['pos'][0] - 1) * 4] = '1'
        grille[8 - self.joueurs[1]['pos'][1] + 1][(self.joueurs[1]['pos'][0] - 1) * 4] = '2'

        for chiffres_verticaux in range(9):
            grille[chiffres_verticaux].insert(0, str(9 - chiffres_verticaux) + ' | ')

        grille.append(['--|-----------------------------------\n'])
        grille.append([' ', ' ', '| ', '1', '   2', '   3', '   4', '   5', '   6', '   7', '   8', '   9'])
        grille[8] = grille[8][:36]

        for position in self.murs['horizontaux']:
            a, b = position

            for element in range(7):
                grille[9 - b][35 + a * 4 + element] = '-'

        for pos in self.murs['verticaux']:
            a, b = pos
            grille[9 - b - 1][a * 4 - 5] = '|'
            grille[9 - b - 1][34 + a * 4] = '|'
            grille[9 - b][a * 4 - 5] = '|'

        return ligne1 + ''.join(''.join(i for i in ligne) for ligne in grille) + '\n'

    def déplacer_jeton(self, joueur, position):
        for pos in position:
            if not 1 <= pos <= 9:
                raise QuoridorError('La position est invalide (en dehors du damier).')
            if not joueur == 1 or not joueur == 2:
                raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        # État actuel de la partie

    def état_partie(self):

        état_present = {'joueurs': [{'nom': self.joueurs[0]['nom'],
                                     'murs': self.joueurs[0]['murs'],
                                     'pos': self.joueurs[0]['pos']},
                                    {'nom': self.joueurs[1]['nom'],
                                     'murs': self.joueurs[1]['murs'],
                                     'pos': self.joueurs[1]['pos']}],
                        'murs': {'horizontaux': self.murs['horizontaux'],
                                 'verticaux': self.murs['verticaux']}}
        return état_present

    def jouer_coup(self, joueur):

        # S'asssurer que le numéro du joueur soit 1 ou 2
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

        if self.partie_terminée():
            raise QuoridorError(" La partie est déjà terminée.")

        # Effectuer le chemin le plus court pour le joueur 1
        chemin_joueur_1 = nx.shortest_path(self.construire_graphe(), self.joueurs[0]['pos'], 'B1')

        # Effectuer le chemin le plus court pour le joueur 2
        chemin_joueur_2 = nx.shortest_path(self.construire_graphe(), self.joueurs[1]['pos'], 'B2')

        if joueur == 1:

            if len(chemin_joueur_1) > len(chemin_joueur_2):

                if self.joueurs[0]['murs'] > 1:

                    try:
                        self.placer_mur(1, self.joueurs[1]['pos'], 'horizontal')

                    except QuoridorError:

                        try:
                            self.placer_mur(1, (self.joueurs[1]['pos'][0] - 1,
                                                self.joueurs[1]['pos'][1]), 'horizontal')

                        except QuoridorError:

                            try:
                                self.placer_mur(1, (self.joueurs[1]['pos'][0],
                                                    self.joueurs[1]['pos'][1] - 1), 'horizontal')

                            except QuoridorError:

                                try:
                                    self.placer_mur(1, (self.joueurs[1]['pos'][0] - 1,
                                                        self.joueurs[1]['pos'][1] - 1), 'horizontal')

                                except QuoridorError:

                                    try:
                                        self.placer_mur(
                                            1, (self.joueurs[1]['pos'][0],
                                                self.joueurs[1]['pos'][1] - 1), 'vertical')

                                    except QuoridorError:

                                        try:
                                            self.placer_mur(
                                                1, (self.joueurs[1]['pos'][0] + 1,
                                                    self.joueurs[1]['pos'][1] - 1), 'vertical')

                                        except QuoridorError:
                                            self.déplacer_jeton(1, chemin_joueur_1[1])
                else:

                    if self.joueurs[1]['pos'][1] == 2:

                        try:

                            self.placer_mur(1, self.joueurs[1]['pos'], 'horizontal')

                        except QuoridorError:

                            try:
                                self.placer_mur(1, (self.joueurs[1]['pos'][0] - 1,
                                                    self.joueurs[1]['pos'][1]), 'horizontal')

                            except QuoridorError:

                                self.déplacer_jeton(1, chemin_joueur_1[1])

                    else:
                        self.déplacer_jeton(1, chemin_joueur_1[1])

            else:
                self.déplacer_jeton(1, chemin_joueur_1[1])

        elif joueur == 2:

            if len(chemin_joueur_2) > len(chemin_joueur_1):

                try:
                    self.placer_mur(2, (self.joueurs[0]['pos'][0], self.joueurs[0]['pos'][1] + 1), 'horizontal')

                except QuoridorError:

                    try:
                        self.placer_mur(2, self.joueurs[0]['pos'], 'vertical')
                    except QuoridorError:
                        self.déplacer_jeton(2, chemin_joueur_2[1])

            else:
                self.déplacer_jeton(2, chemin_joueur_2[1])

                # Vérifier si le numéro du joueur est bien 1 ou 2
        else:
            raise QuoridorError('Le numéro du joueur doit être 1 ou 2.')


    def partie_terminée(self):

        # si le premier joueur atteint le mur opposé
        if self.joueurs[0]['pos'][1] == 9:
            return self.joueurs[0]['nom']

        # si le deuxième joueur atteint le mur oppposé
        if self.joueurs[1]['pos'][1] == 1:
            return self.joueurs[1]['nom']

        return False

    def placer_mur(self, joueur, position, orientation):
        # S'assurer qu'il reste des murs a placé sur le jeu
        if self.joueurs[0]['murs'] == 0 or self.joueurs[1]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')

        # S'assurer que la position voulue ne soit pas déjà occupé par un mur
        if position in self.murs['verticaux'] or position in self.murs['horizontaux']:
            raise QuoridorError('Un mur occupe déjà cette position.')

        if orientation != 'horizontaux':
            raise QuoridorError("La position est invalide pour cette orientation. (Ce n'est pas un mur horizontal)")
        else:
            # Sinon les positions appartienent à l'argument 'position'
            a, b = position
            if a not in range(2, 10) or b not in range(1, 9):
                raise QuoridorError("La position d'un mur est invalide.")

            # S'assurer que le placement d'un mur horizontal n'est pas en superposition avec un autre mur
            if ((position[0] + 1, position[1]) in self.murs['horizontaux']) or (position[0] - 1, position[1]) in \
                    self.murs['horizontaux']:
                raise QuoridorError("Position d'un mur horizontal est invalide : superposition avec un autre mur")

            # S'assurer que les murs ne se croisent pas
            for vertical_walls in self.murs['verticaux']:
                if (vertical_walls[0] - position[0]) + (vertical_walls[1] - position[1]) == 0:
                    raise QuoridorError("Position d'un mur horizontal est invalide : les murs se croisent")
            self.murs['horizontaux'].append(position)
            self.joueurs[joueur - 1]['murs'] -= 1

            # S'assurer que les murs n'enferment pas un joueur
            if not nx.has_path(self.construire_graphe(), self.joueurs[0]['pos'], 'B1'
                               ) or not nx.has_path(self.construire_graphe(),
                                                    self.joueurs[1]['pos'], 'B2'):
                self.murs['horizontaux'].remove(position)
                raise QuoridorError("Position d'un mur est invalide : les murs enferment un joueur")

        if orientation != 'verticaux':
            raise QuoridorError("La position est invalide pour cette orientation. (Ce n'est pas un mur vertical)")
        else:
            a, b = position
            if a not in range(1, ) or b not in range(2, 10):
                raise QuoridorError("La position d'un mur est invalide.")

        # S'assurer que le placement d'un mur vertical n'est pas en superposition avec un autre mur
        if ((position[0] + 1, position[1]) in self.murs['verticaux']) or (position[0] - 1, position[1])\
                in self.murs['verticaux']:
            raise QuoridorError("Position d'un mur vertical est invalide : superposition avec un autre mur")

        # S'assurer que les murs ne se croisent pas
        for horizontal_walls in self.murs['horizontaux']:
            if (horizontal_walls[0] - position[0]) + (horizontal_walls[1] - position[1]) == 0:
                raise QuoridorError("Position d'un mur vertical est invalide : les murs se croisent")

        self.murs['verticaux'].append(position)
        self.joueurs[joueur - 1]['murs'] -= 1

        # S'assurer que les murs n'enferment pas un joueur
        if not nx.has_path(self.construire_graphe(), self.joueurs[0]['pos'], 'B1'
                           ) or not nx.has_path(self.construire_graphe(),
                                                self.joueurs[1]['pos'], 'B2'):
            self.murs['verticaux'].remove(position)
            raise QuoridorError("Position d'un mur est invalide : les murs enferment un joueur")

        # S'assurer que les numéros des joueurs soit bien de 1 ou 2
        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2.")

    def construire_graphe(self):
        joueurs = [self.état_partie()['joueurs'][0]['pos'], self.état_partie()['joueurs'][1]['pos']]
        murs_horizontaux = self.état_partie()['murs']['horizontaux']
        murs_verticaux = self.état_partie()['murs']['verticaux']
        graphe = nx.DiGraph()

        # pour chaque colonne du damier
        for x in range(1, 10):
            # pour chaque ligne du damier
            for y in range(1, 10):
                # ajouter les arcs de tous les déplacements possibles pour cette tuile
                if x > 1:
                    graphe.add_edge((x, y), (x - 1, y))
                if x < 9:
                    graphe.add_edge((x, y), (x + 1, y))
                if y > 1:
                    graphe.add_edge((x, y), (x, y - 1))
                if y < 9:
                    graphe.add_edge((x, y), (x, y + 1))

        # retirer tous les arcs qui croisent les murs horizontaux
        for x, y in murs_horizontaux:
            graphe.remove_edge((x, y - 1), (x, y))
            graphe.remove_edge((x, y), (x, y - 1))
            graphe.remove_edge((x + 1, y - 1), (x + 1, y))
            graphe.remove_edge((x + 1, y), (x + 1, y - 1))

        # retirer tous les arcs qui croisent les murs verticaux
        for x, y in murs_verticaux:
            graphe.remove_edge((x - 1, y), (x, y))
            graphe.remove_edge((x, y), (x - 1, y))
            graphe.remove_edge((x - 1, y + 1), (x, y + 1))
            graphe.remove_edge((x, y + 1), (x - 1, y + 1))

        # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
        j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

        # traiter le cas des joueurs adjacents
        if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

            # retirer les liens entre les joueurs
            graphe.remove_edge(j1, j2)
            graphe.remove_edge(j2, j1)

            def ajouter_lien_sauteur(noeud, voisin):
                """
                :param noeud: noeud de départ du lien.
                :param voisin: voisin par dessus lequel il faut sauter.
                """
                saut = 2 * voisin[0] - noeud[0], 2 * voisin[1] - noeud[1]

                # ajouter le saut en ligne droite
                if saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

                else:

                    for saut in graphe.successors(voisin):
                        graphe.add_edge(noeud, saut)

            ajouter_lien_sauteur(j1, j2)
            ajouter_lien_sauteur(j2, j1)

        # ajouter les destinations finales des joueurs
        for x in range(1, 10):
            graphe.add_edge((x, 9), 'B1')
            graphe.add_edge((x, 1), 'B2')

        return graphe


class QuoridorError(Exception):
    """Classe pour détecter les erreurs du jeu Quoridor"""
