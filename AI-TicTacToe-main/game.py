# -----------------------------------------------------------------------------
# game.py — Implémentation complète du Morpion Ultime (Ultimate Tic‑Tac‑Toe)
# -----------------------------------------------------------------------------
# Ce module définit :
#   • PetitPlateau  : sous‑grille classique 3 × 3 (un « petit » morpion)
#   • MorpionUltime : plateau global 3 × 3 de PetitPlateau
#   • Deux modes console             : humain_vs_humain et humain_vs_ia
#
#  > Toutes les règles du « Morpion Ultime » sont implémentées :
#       – lorsqu’un joueur joue dans la cellule (r, c) d’un sous‑plateau,
#         l’adversaire est forcé de jouer dans le sous‑plateau (r, c) global ;
#       – si ce sous‑plateau est déjà terminé, le choix est libre ;
#       – victoire d’un sous‑plateau = lettre inscrite sur le plateau global ;
#       – trois sous‑plateaux gagnés alignés = victoire de la partie globale ;
#       – si plus aucune victoire n’est possible → match nul.
#
#  > AUCUNE LOGIQUE DE JEU N’A ÉTÉ MODIFIÉE.
#    Seuls des commentaires abondants ont été ajoutés pour expliquer en détail
#    chaque portion de code.
# -----------------------------------------------------------------------------

# =============================================================================
# Classe « PetitPlateau » — un morpion 3 × 3 classique
# =============================================================================
class PetitPlateau:
    """Sous‑grille 3 × 3.
    
    Attributs
    ---------
    plateau      : list[list[str]]  — contient 'X', 'O' ou ' ' (vide)
    vainqueur    : str | None       — 'X', 'O', "DRAW" ou None si en cours
    jeu_termine  : bool             — True lorsque ce sous‑plateau est terminé
    """

    def __init__(self):
        # Appelle directement la méthode qui (re)met tout à zéro
        self.reinitialiser()
    
    # -----------------------------------------------------------------
    # Méthodes internes
    # -----------------------------------------------------------------
    def reinitialiser(self):
        """Vide le plateau et remet les états à leur valeur initiale."""
        self.plateau     = [[' ' for _ in range(3)] for _ in range(3)]  # Grille vide
        self.vainqueur   = None     # Pas de gagnant
        self.jeu_termine = False    # Sous‑partie encore active

    def coup_valide(self, ligne, colonne):
        """Renvoie True si la case (ligne, colonne) est jouable."""
        return (
            0 <= ligne < 3 and
            0 <= colonne < 3 and
            self.plateau[ligne][colonne] == ' ' and  # Case vide
            not self.jeu_termine                     # Sous‑plateau encore en cours
        )

    def jouer_coup(self, ligne, colonne, joueur):
        """Effectue le coup du joueur ; renvoie False si le coup n’est pas légal."""
        if self.coup_valide(ligne, colonne):
            self.plateau[ligne][colonne] = joueur         # Place le symbole
            self.verifier_etat(joueur)                    # Met à jour vainqueur/nul
            return True
        return False

    def verifier_etat(self, joueur):
        """Après chaque coup, vérifie victoire ou match nul."""
        # --- 3 lignes horizontales + 3 colonnes ------------------------
        for i in range(3):
            if all(self.plateau[i][j] == joueur for j in range(3)):
                self.vainqueur, self.jeu_termine = joueur, True; return
            if all(self.plateau[j][i] == joueur for j in range(3)):
                self.vainqueur, self.jeu_termine = joueur, True; return
        # --- 2 diagonales ----------------------------------------------
        if (self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] == joueur) or \
           (self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] == joueur):
            self.vainqueur, self.jeu_termine = joueur, True; return
        # --- Match nul --------------------------------------------------
        if self.est_nul():
            self.vainqueur, self.jeu_termine = "DRAW", True  # Plateau rempli

    def est_nul(self):
        """True si plus aucune case vide et aucun vainqueur."""
        return all(self.plateau[i][j] != ' ' for i in range(3) for j in range(3))

    # -----------------------------------------------------------------
    # Méthodes utilitaires
    # -----------------------------------------------------------------
    def obtenir_vainqueur(self):
        """Renvoie le vainqueur actuel ('X', 'O', 'DRAW') ou None."""
        return self.vainqueur

    def dupliquer(self):
        """Retourne une DEEP‑COPY de ce PetitPlateau (pour l’IA)."""
        nouveau               = PetitPlateau()
        nouveau.plateau       = [ligne[:] for ligne in self.plateau]  # Copie chaque ligne
        nouveau.vainqueur     = self.vainqueur
        nouveau.jeu_termine   = self.jeu_termine
        return nouveau

    # -----------------------------------------------------------------
    # Représentation ASCII (facilite le debug)
    # -----------------------------------------------------------------
    def __str__(self):
        return "\n".join(" ".join(ligne) for ligne in self.plateau)


# =============================================================================
# Classe « MorpionUltime » — plateau global 3 × 3 de PetitPlateau
# =============================================================================
class MorpionUltime:
    """Implémente toutes les règles du Morpion Ultime."""

    def __init__(self):
        self.reinitialiser()

    # -----------------------------------------------------------------
    # (Ré)initialise l’état global
    # -----------------------------------------------------------------
    def reinitialiser(self):
        self.plateaux       = [[PetitPlateau() for _ in range(3)] for _ in range(3)]
        self.joueur_courant = 'X'       # Le joueur qui doit jouer maintenant
        self.plateau_actif  = None      # None -> le prochain coup est « libre »
        self.jeu_termine    = False
        self.vainqueur      = None

    # -----------------------------------------------------------------
    # Validation globale d’un coup
    # -----------------------------------------------------------------
    def coup_valide(self, sp_l, sp_c, cel_l, cel_c):
        """Teste si le coup (sousPlateau, cellule) est légal dans le contexte actuel."""
        if not (0 <= sp_l < 3 and 0 <= sp_c < 3):
            return False                                   # Indices hors limites
        plateau = self.plateaux[sp_l][sp_c]
        if plateau.jeu_termine:
            return False                                   # Sous‑plateau fini
        if self.plateau_actif is not None and (sp_l, sp_c) != self.plateau_actif:
            return False                                   # Doit jouer dans le sous‑plateau imposé
        return plateau.coup_valide(cel_l, cel_c)

    def jouer_coup(self, sp_l, sp_c, cel_l, cel_c):
        """Joue le coup ; met ensuite à jour plateau_actif et change de joueur."""
        if not self.coup_valide(sp_l, sp_c, cel_l, cel_c) or self.jeu_termine:
            return False
        
        # Place le coup dans le sous‑plateau ciblé ------------------------
        plateau = self.plateaux[sp_l][sp_c]
        if not plateau.jouer_coup(cel_l, cel_c, self.joueur_courant):
            return False  # (Sécurité)

        # Met à jour l’état global (victoires/partie nulle)
        self.mettre_a_jour_etat_global()
        
        # Détermine le prochain sous‑plateau imposé -----------------------
        prochain = (cel_l, cel_c)
        self.plateau_actif = None if self.plateaux[prochain[0]][prochain[1]].jeu_termine else prochain

        # Change de joueur si la partie continue -------------------------
        if not self.jeu_termine:
            self.joueur_courant = 'O' if self.joueur_courant == 'X' else 'X'
        return True

    # -----------------------------------------------------------------
    # Passe en revue tous les sous‑plateaux pour déterminer la situation globale
    # -----------------------------------------------------------------
    def mettre_a_jour_etat_global(self):
        """Analyse l’état des sous‑plateaux pour savoir si la partie est gagnée/nulle."""
        # 1) Crée une grille virtuelle indiquant le vainqueur de chaque sous‑plateau
        global_p = [[' ' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                vainq = self.plateaux[i][j].obtenir_vainqueur()
                global_p[i][j] = vainq if vainq is not None else ' '

        # 2) Recherche d’une ligne/colonne/diagonale complète (victoire globale)
        for i in range(3):
            # Ligne horizontale i
            if global_p[i][0] != ' ' and global_p[i][0] != "DRAW" and \
               all(global_p[i][j] == global_p[i][0] for j in range(3)):
                self.vainqueur, self.jeu_termine = global_p[i][0], True; return
            # Ligne verticale i
            if global_p[0][i] != ' ' and global_p[0][i] != "DRAW" and \
               all(global_p[j][i] == global_p[0][i] for j in range(3)):
                self.vainqueur, self.jeu_termine = global_p[0][i], True; return
        # Diagonale principale
        if global_p[0][0] != ' ' and global_p[0][0] != "DRAW" and \
           global_p[0][0] == global_p[1][1] == global_p[2][2]:
            self.vainqueur, self.jeu_termine = global_p[0][0], True; return
        # Diagonale secondaire
        if global_p[0][2] != ' ' and global_p[0][2] != "DRAW" and \
           global_p[0][2] == global_p[1][1] == global_p[2][0]:
            self.vainqueur, self.jeu_termine = global_p[0][2], True; return

        # 3) Match nul global : plus aucun sous‑plateau jouable
        if all(self.plateaux[i][j].jeu_termine for i in range(3) for j in range(3)):
            self.jeu_termine, self.vainqueur = True, None; return

        # 4) Option « nulle anticipée » : plus aucune victoire théorique possible
        combinaisons = [
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
        ]
        def peut_encore_gagner(joueur):
            return any(all(global_p[r][c] in [joueur,' '] for (r,c) in combo) for combo in combinaisons)
        if not peut_encore_gagner('X') and not peut_encore_gagner('O'):
            self.jeu_termine, self.vainqueur = True, None

    # -----------------------------------------------------------------
    # Méthodes utilitaires
    # -----------------------------------------------------------------
    def obtenir_coups_valides(self):
        """Retourne la liste de TOUS les coups légaux dans l’état présent."""
        coups = []
        if self.plateau_actif is not None:
            sp_l, sp_c = self.plateau_actif
            plateau = self.plateaux[sp_l][sp_c]
            for i in range(3):
                for j in range(3):
                    if plateau.coup_valide(i, j):
                        coups.append((sp_l, sp_c, i, j))
        else:
            # Parcourt tous les sous‑plateaux non terminés
            for sp_l in range(3):
                for sp_c in range(3):
                    plateau = self.plateaux[sp_l][sp_c]
                    if plateau.jeu_termine:
                        continue
                    for i in range(3):
                        for j in range(3):
                            if plateau.coup_valide(i, j):
                                coups.append((sp_l, sp_c, i, j))
        return coups

    def obtenir_vainqueur(self):
        """Renvoie le vainqueur ('X', 'O') ou None (nulle/en cours)."""
        return self.vainqueur

    def dupliquer(self):
        """Copie profonde complète (utilisée par l’IA pour simuler)."""
        clone = MorpionUltime()
        clone.plateaux       = [[self.plateaux[i][j].dupliquer() for j in range(3)] for i in range(3)]
        clone.joueur_courant = self.joueur_courant
        clone.plateau_actif  = self.plateau_actif
        clone.jeu_termine    = self.jeu_termine
        clone.vainqueur      = self.vainqueur
        return clone

    # -----------------------------------------------------------------
    # Affichage console — format grille ASCII 9 × 9
    # -----------------------------------------------------------------
    def afficher_plateau(self):
        lignes = []
        for grand_l in range(3):
            for petit_l in range(3):
                ligne = ""
                for grand_c in range(3):
                    plateau = self.plateaux[grand_l][grand_c]
                    ligne += " " + "|".join(plateau.plateau[petit_l]) + " "
                    if grand_c < 2:
                        ligne += "||"
                lignes.append(ligne)
            if grand_l < 2:
                lignes.append("=" * len(ligne))   # Séparateur horizontal
        print("\n".join(lignes))
        print("Prochain coup :", "n'importe quel plateau" if self.plateau_actif is None else f"plateau {self.plateau_actif}")
        print(f"Joueur courant : {self.joueur_courant}")


# =============================================================================
# Fonctions console — 2 joueurs humains ou Humain vs IA
# =============================================================================
def humain_vs_humain():
    """Lance une partie en local entre deux joueurs humains."""
    jeu = MorpionUltime()
    while not jeu.jeu_termine:
        jeu.afficher_plateau()
        print(f"Tour du joueur {jeu.joueur_courant}")
        try:
            print("Entrez : sp_l sp_c cel_l cel_c (0-2)")
            entree = input("Votre coup : ").split()
            if len(entree) != 4:
                print("Merci d'entrer 4 nombres séparés par des espaces."); continue
            sp_l, sp_c, cel_l, cel_c = map(int, entree)
            if not jeu.jouer_coup(sp_l, sp_c, cel_l, cel_c):
                print("Coup invalide ! Réessayez.")
        except ValueError:
            print("Veuillez entrer des nombres valides.")
    jeu.afficher_plateau()
    gagnant = jeu.obtenir_vainqueur()
    print("Résultat :", f"le joueur {gagnant} gagne !" if gagnant else "Match nul !")


def humain_vs_ia(ia):
    """Fait s’affronter un joueur humain (X) contre une instance d’IA (O)."""
    jeu = MorpionUltime()
    joueur_humain, joueur_ia = 'X', 'O'
    print(f"Vous jouez {joueur_humain} contre {ia.nom}")
    while not jeu.jeu_termine:
        jeu.afficher_plateau()
        if jeu.joueur_courant == joueur_humain:
            try:
                print("Votre tour — saisissez : sp_l sp_c cel_l cel_c (0-2)")
                entree = input("Votre coup : ").split()
                if len(entree) != 4:
                    print("Merci d'entrer 4 nombres."); continue
                sp_l, sp_c, cel_l, cel_c = map(int, entree)
                if not jeu.jouer_coup(sp_l, sp_c, cel_l, cel_c):
                    print("Coup invalide ! Réessayez.")
            except ValueError:
                print("Veuillez entrer des nombres valides.")
        else:
            print(f"{ia.nom} réfléchit...")
            coup = ia.get_move(jeu)                # L’IA calcule son coup
            if coup is None:                       # Cas limite (pas de coup possible)
                print("Aucun coup valide pour l'IA !"); break
            jeu.jouer_coup(*coup)
            print(f"{ia.nom} a joué plateau {coup[0],coup[1]} cellule {coup[2],coup[3]}")
    jeu.afficher_plateau()
    gagnant = jeu.obtenir_vainqueur()
    if gagnant == joueur_humain:
        print("Vous gagnez !")
    elif gagnant == joueur_ia:
        print(f"{ia.nom} gagne !")
    else:
        print("Match nul !")