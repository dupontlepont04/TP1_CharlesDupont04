"""Programme introduisant une classe pour jouer au jeu Quoridor
sur une interface graphique"""


class QuoridorX(quoridor.Quoridor):

    """Permet d'afficher l'état actuel du damier dans une fenêtre graphique """

    def __init__(self, joueurs, murs=None):
        super().__init__(self,joueurs, murs)

