# -----------------------------------------------------------------------------
# ai.py — Module des intelligences artificielles pour le Morpion Ultime
# -----------------------------------------------------------------------------
#  Trois niveaux d’intelligence sont fournis :
#      • IAFacile      — recherche sur un seul coup à l’avance.
#      • IAMoyenne     — algorithme Minimax profondeur 3 (sans élagage),
#                         avec un pourcentage d’erreurs volontaires pour
#                         “humaniser” la difficulté.
#      • IADifficile   — Minimax profondeur 4 avec élagage alpha-beta + une
#                         heuristique plus fine (prise en compte des fourches
#                         et de la mobilité).
#
#  Chaque classe hérite de la base « IA » afin de partager :
#      – le symbole (« X » ou « O ») de l’IA et celui de l’adversaire ;
#      – un compteur des nœuds évalués (coups_evalues) ;
#      – un champ pour stocker le score heuristique du dernier coup ;
#      – une méthode utilitaire pour récupérer les coups légaux.
#
#  Deux fonctions d’évaluation (heuristiques) existent :
#      • evaluer_ultime(partie, joueur)
#          > évalue l’état global à partir de la somme :
#              1) des sous-plateaux déjà gagnés / perdus ; et
#              2) de l’état interne des sous-plateaux non finis.
#      • evaluer_difficile(partie, joueur)
#          > reprend la précédente et ajoute :
#              – un bonus proportionnel au nombre de coups encore jouables ;
#              – un bonus/malus pour les positions de “double-menace” (fourches).
#
#  Toutes les méthodes retournant un coup renvoient un quadruplet :
#      (sousPlateau_ligne, sousPlateau_colonne, cellule_ligne, cellule_colonne)
# -----------------------------------------------------------------------------

import random
import math

# =============================================================================
# Classe de base — attributs et utilitaires communs à toutes les IA
# =============================================================================
class IA:
    """Classe mère de toutes les IA.
    
    Paramètres
    ----------
    joueur : str
        Symbole joué par l’IA ('X' ou 'O').
    
    Attributs
    ---------
    adversaire : str
        Symbole de l’adversaire ('O' si IA est 'X', et inversement).
    nom : str
        Nom lisible de l’IA (surchargé dans les classes filles).
    coups_evalues : int
        Compteur de nœuds évalués lors du dernier appel à `get_move`.
    score_dernier_coup : float | None
        Score heuristique du coup choisi lors du dernier appel à `get_move`.
    """

    def __init__(self, joueur):
        self.joueur             = joueur                                 # Symbole IA
        self.adversaire         = 'O' if joueur == 'X' else 'X'          # Symbole adv.
        self.nom                = "IA de Base"                           # Nom par défaut
        self.coups_evalues      = 0                                        # Compteur reset
        self.score_dernier_coup = None                                     # Score du dernier coup

    # -----------------------------------------------------------------
    # Méthodes d’interface
    # -----------------------------------------------------------------
    def obtenir_coups_valides(self, partie):
        """Renvoie la liste des coups légaux pour l’état `partie` fourni.
        
        Délègue simplement à l’objet `partie` (instance de MorpionUltime)."""
        return partie.obtenir_coups_valides()


# =============================================================================
# Heuristique de base — Sert à IAFacile & IAMoyenne
# =============================================================================
def evaluer_ligne(ligne, joueur):
    """Attribue un score à une ligne / colonne / diagonale.
    L’idée : plus il y a de symboles « joueur » alignés sans blocage adverse,
    plus la valeur augmente exponentiellement (10ⁿ).
    Inversement, si la ligne appartient à l’adversaire, la valeur est négative.
    Si les deux symboles sont présents, la ligne est “bloquée” → 0."""
    adversaire = 'O' if joueur == 'X' else 'X'
    if joueur in ligne and adversaire in ligne:      # Ligne mixte → bloquée
        return 0
    if joueur in ligne:                              # Ligne à notre avantage
        return 10 ** ligne.count(joueur)
    if adversaire in ligne:                          # Ligne à l’adversaire
        return -(10 ** ligne.count(adversaire))
    return 0                                         # Ligne vide (neutre)


def evaluer_sous_plateau(plateau, joueur):
    """Score d’un PetitPlateau non fini (contrôle centre + alignements)."""
    score = 0
    # Contrôle du centre : très important dans le morpion ----------------
    if plateau.plateau[1][1] == joueur:
        score += 20
    elif plateau.plateau[1][1] == ('O' if joueur == 'X' else 'X'):
        score -= 20
    # Parcourt les 3 lignes horizontales ---------------------------------
    for r in range(3):
        score += evaluer_ligne(plateau.plateau[r], joueur)
    # Parcourt les 3 lignes verticales -----------------------------------
    for c in range(3):
        colonne = [plateau.plateau[r][c] for r in range(3)]
        score += evaluer_ligne(colonne, joueur)
    # Ajoute les 2 diagonales --------------------------------------------
    diag1 = [plateau.plateau[i][i]   for i in range(3)]
    diag2 = [plateau.plateau[i][2-i] for i in range(3)]
    score += evaluer_ligne(diag1, joueur)
    score += evaluer_ligne(diag2, joueur)
    return score


def evaluer_ultime(partie, joueur):
    """Heuristique globale — mixe :
       1) plaques déjà gagnées/perdues  2) état interne des autres plaques."""
    adversaire = 'O' if joueur == 'X' else 'X'
    score = 0
    # 1. Parcourt les 9 sous-plateaux et gère ceux déjà décidés ----------
    for i in range(3):
        for j in range(3):
            sp = partie.plateaux[i][j]
            if sp.vainqueur == joueur:
                score += 10000                   # Grosse récompense
            elif sp.vainqueur == adversaire:
                score -= 10000                   # Grosse pénalité
            else:
                score += evaluer_sous_plateau(sp, joueur)
    # 2. Convertit en plateau global virtuel et réévalue ----------------
    pg = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            w = partie.plateaux[i][j].vainqueur
            pg[i][j] = w if w and w != 'DRAW' else ' '
    for r in range(3):
        score += evaluer_ligne(pg[r], joueur) * 10
    for c in range(3):
        score += evaluer_ligne([pg[r][c] for r in range(3)], joueur) * 10
    diag1 = [pg[i][i]   for i in range(3)]
    diag2 = [pg[i][2-i] for i in range(3)]
    score += evaluer_ligne(diag1, joueur) * 10
    score += evaluer_ligne(diag2, joueur) * 10
    return score


# =============================================================================
# Heuristique avancée (Version Difficile) — ajoute mobilité & fourches
# =============================================================================
def evaluer_difficile(partie, joueur):
    """Version améliorée :
       • reprend evaluer_ultime
       • ajoute un petit bonus pour le nombre de coups disponibles
       • détecte les « fourches » (double-menace dans un sous-plateau)."""
    adversaire = 'O' if joueur == 'X' else 'X'
    score = evaluer_ultime(partie, joueur)                    # Base héritée
    score += len(partie.obtenir_coups_valides())              # Mobilité
    # Boucle sur sous-plateaux non terminés -------------------------
    for i in range(3):
        for j in range(3):
            sp = partie.plateaux[i][j]
            if sp.jeu_termine:
                continue
            men_joueur = men_adv = 0
            lignes = []
            lignes.extend(sp.plateau)                             # 3 lignes
            lignes.extend([[sp.plateau[r][c] for r in range(3)]   # 3 colonnes
                           for c in range(3)])
            lignes.append([sp.plateau[k][k]   for k in range(3)]) # diag \
            lignes.append([sp.plateau[k][2-k] for k in range(3)]) # diag /
            # Comptage des menaces immédiates ----------------------
            for ligne in lignes:
                if ligne.count(joueur) == 2 and ligne.count(' ') == 1:
                    men_joueur += 1
                if ligne.count(adversaire) == 2 and ligne.count(' ') == 1:
                    men_adv += 1
            if men_joueur >= 2:   # Deux menaces distinctes = fourche
                score += 300
            if men_adv >= 2:
                score -= 300
    return score


# =============================================================================
# IAFacile — évalue chaque coup sur une profondeur de 1
# =============================================================================
class IAFacile(IA):
    def __init__(self, joueur):
        super().__init__(joueur)
        self.nom            = "IA Facile"
        self.profondeur_max = 1  # Profondeur maximale (non utilisée ici)

    def get_move(self, partie):
        """Teste tous les coups et renvoie celui au meilleur score heuristique."""
        # self.coups_evalues = 0  # Statistiques désactivées
        meilleur_score     = -math.inf
        meilleur_coup      = None
        # Boucle d’évaluation brute ---------------------------------------
        for mv in self.obtenir_coups_valides(partie):
            clone = partie.dupliquer(); clone.jouer_coup(*mv)
            # self.coups_evalues += 1                          # Statistiques
            sc = evaluer_ultime(clone, self.joueur)
            if sc > meilleur_score:
                meilleur_score, meilleur_coup = sc, mv
        self.score_dernier_coup = meilleur_score
        return meilleur_coup


# =============================================================================
# IAMoyenne — Minimax sans élagage, profondeur 3, avec erreurs possibles
# =============================================================================
class IAMoyenne(IA):
    def __init__(self, joueur):
        super().__init__(joueur)
        self.nom                      = "IA Moyenne"
        self.profondeur_max          = 3
        self.taux_erreur_strategique = 0.3  # 30 % de coups “aléatoires”

    # -----------------------------------------------------------------
    # Minimax récursif (sans alpha-beta)
    # -----------------------------------------------------------------
    def minimax(self, partie, profondeur, est_max):
        """Retourne la valeur minimax du nœud `partie` (récursion)."""
        # self.coups_evalues += 1
        if partie.jeu_termine or profondeur == self.profondeur_max:
            return evaluer_ultime(partie, self.joueur)
        if est_max:
            meilleur = -math.inf
            for mv in partie.obtenir_coups_valides():
                clone = partie.dupliquer(); clone.jouer_coup(*mv)
                meilleur = max(meilleur, self.minimax(clone, profondeur+1, False))
            return meilleur
        else:
            pire = math.inf
            for mv in partie.obtenir_coups_valides():
                clone = partie.dupliquer(); clone.jouer_coup(*mv)
                pire = min(pire, self.minimax(clone, profondeur+1, True))
            return pire

    def get_move(self, partie):
        """Renvoie le meilleur coup, ou un coup aléatoire selon le taux d’erreur."""
        # self.coups_evalues = 0
        # Introduit de l’aléa pour simuler des erreurs stratégiques ------
        if random.random() < self.taux_erreur_strategique:
            mv = random.choice(self.obtenir_coups_valides(partie))
            clone = partie.dupliquer(); clone.jouer_coup(*mv)
            self.score_dernier_coup = evaluer_ultime(clone, self.joueur)
            return mv
        meilleur_score = -math.inf
        meilleurs      = []
        for mv in self.obtenir_coups_valides(partie):
            clone = partie.dupliquer(); clone.jouer_coup(*mv)
            sc = self.minimax(clone, 1, False)               # Prochaine couche = “min”
            if sc > meilleur_score:
                meilleur_score, meilleurs = sc, [mv]
            elif sc == meilleur_score:
                meilleurs.append(mv)
        self.score_dernier_coup = meilleur_score
        return random.choice(meilleurs)


# =============================================================================
# IADifficile — Minimax profondeur 4 avec élagage alpha-beta + heuristique avancée
# =============================================================================
class IADifficile(IA):
    def __init__(self, joueur):
        super().__init__(joueur)
        self.nom             = "IA Difficile"
        self.profondeur_max  = 4

    # -----------------------------------------------------------------
    # Minimax alpha-beta
    # -----------------------------------------------------------------
    def minimax(self, partie, profondeur, alpha, beta, est_max):
        """Recherche alpha-beta. `alpha` = valeur max garantie, `beta` = valeur min garantie."""
        # self.coups_evalues += 1
        if partie.jeu_termine or profondeur == self.profondeur_max:
            return evaluer_difficile(partie, self.joueur)
        if est_max:
            val = -math.inf
            for mv in partie.obtenir_coups_valides():
                clone = partie.dupliquer(); clone.jouer_coup(*mv)
                val = max(val, self.minimax(clone, profondeur+1, alpha, beta, False))
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val
        else:
            val = math.inf
            for mv in partie.obtenir_coups_valides():
                clone = partie.dupliquer(); clone.jouer_coup(*mv)
                val = min(val, self.minimax(clone, profondeur+1, alpha, beta, True))
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val

    def get_move(self, partie):
        """Évalue tous les coups racine avec minimax αβ et renvoie le meilleur."""
        # self.coups_evalues = 0
        meilleur_score     = -math.inf
        meilleur_coup      = None
        alpha, beta        = -math.inf, math.inf
        for mv in self.obtenir_coups_valides(partie):
            clone = partie.dupliquer(); clone.jouer_coup(*mv)
            sc = self.minimax(clone, 1, alpha, beta, False)
            if sc > meilleur_score:
                meilleur_score, meilleur_coup = sc, mv
            alpha = max(alpha, meilleur_score)          # Mise à jour α
        self.score_dernier_coup = meilleur_score
        return meilleur_coup
