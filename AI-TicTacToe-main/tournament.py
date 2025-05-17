# -----------------------------------------------------------------------------
# tournament.py — Lancement automatique de confrontations entre IAs
# -----------------------------------------------------------------------------
#  Ce module permet :
#     • de faire s’affronter deux IAs sur une série de parties          (lancer_match)
#     • d’enchaîner tous les duels possibles entre un ensemble d’IAs    (tournoi_complet)
#     • de proposer un petit menu interactif console                     (menu_principal)
# -----------------------------------------------------------------------------

import time
from game import MorpionUltime
from ai import IAFacile, IAMoyenne, IADifficile

class Tournoi:
    """Orchestre des matchs entre deux IAs et collecte statistiques & résultats."""

    def __init__(self):
        # Dictionnaires pouvant être utilisés plus tard pour exporter les stats
        self.resultats = {}
        self.stats_performance = {}

    # -----------------------------------------------------------------
    # Lancer une série de parties entre deux IAs (aller-retour alterné)
    # -----------------------------------------------------------------
    def lancer_match(self, ia1, ia2, nb_parties=10):
        """Fait jouer ia1 et ia2 sur `nb_parties` manches.

        Retourne un tuple (resultats, performance) :
            resultats   : {'IA-1': N, 'IA-2': M, 'nuls': D}
            performance : dict  (temps total, moyenne, nœuds évalués, …)
        """
        # Compteurs initiaux
        resultats = {ia1.nom: 0, ia2.nom: 0, 'nuls': 0}
        total_coups_ia1 = total_coups_ia2 = 0
        total_score_ia1 = total_score_ia2 = 0
        move_count_ia1 = move_count_ia2 = 0
        debut = time.time()

        # -----------------------------------------------------------------
        # Boucle principale sur chaque partie
        # -----------------------------------------------------------------
        for num_partie in range(nb_parties):
            jeu = MorpionUltime()

            # Alterne qui commence en jouant 'X' pour éviter le biais
            if num_partie % 2 == 0:
                joueurs = {'X': ia1, 'O': ia2}
            else:
                joueurs = {'X': ia2, 'O': ia1}

            # Met à jour dynamiquement les symboles de chaque IA
            for symbole, ia in joueurs.items():
                ia.joueur = symbole
                ia.adversaire = 'O' if symbole == 'X' else 'X'

            # --- Boucle tour par tour -----------------------------------
            while not jeu.jeu_termine:
                ia_courante = joueurs[jeu.joueur_courant]
                coup = ia_courante.get_move(jeu)    # IA choisit son action
                if coup is None:                    # Sécurité (ne devrait pas arriver)
                    break

                # Comptabilise le nombre de positions examinées par l’IA
                if ia_courante == ia1:
                    total_coups_ia1 += ia_courante.coups_evalues
                else:
                    total_coups_ia2 += ia_courante.coups_evalues

                # Comptabilise le score heuristique du coup choisi
                sc = ia_courante.score_dernier_coup
                if sc is not None:
                    if ia_courante == ia1:
                        total_score_ia1 += sc
                        move_count_ia1 += 1
                    else:
                        total_score_ia2 += sc
                        move_count_ia2 += 1

                # Applique le coup sur la partie réelle
                jeu.jouer_coup(*coup)

            # --- Fin d’une partie : met à jour le tableau des scores -----
            gagnant = jeu.obtenir_vainqueur()
            if gagnant:
                ia_gagnante = joueurs[gagnant]
                resultats[ia_gagnante.nom] += 1
            else:
                resultats['nuls'] += 1

        # -----------------------------------------------------------------
        # Statistiques de performance globales
        # -----------------------------------------------------------------
        temps_total = time.time() - debut
        perf = {
            'temps_total': temps_total,
            'moyenne_par_partie': temps_total / nb_parties,
            'ia1_score_total': total_score_ia1,
            'ia2_score_total': total_score_ia2,
            'ia1_score_moyen_par_coup': (total_score_ia1 / move_count_ia1) if move_count_ia1 else 0,
            'ia2_score_moyen_par_coup': (total_score_ia2 / move_count_ia2) if move_count_ia2 else 0,
        }

        return resultats, perf

    # -----------------------------------------------------------------
    # Enchaîne tous les duels possibles entre un ensemble d’IAs
    # -----------------------------------------------------------------
    def tournoi_complet(self, nb_parties=10):
        """Lance un tournoi “tous contre tous” entre IAFacile, IAMoyenne, IADifficile."""
        # Liste des concurrents
        ias = [
            IAFacile('X'),
            IAMoyenne('O'),
            IADifficile('X')
        ]

        res_global = []

        print(f"\n=== Lancement du tournoi avec {nb_parties} parties par duel ===\n")

        # Double boucle pour parcourir toutes les paires (sans doublons)
        for i in range(len(ias)):
            for j in range(i + 1, len(ias)):
                ia1, ia2 = ias[i], ias[j]

                print(f"Match : {ia1.nom} vs {ia2.nom}")
                res_duel, perf = self.lancer_match(ia1, ia2, nb_parties)

                # Calculs de pourcentages pour affichage lisible
                taux_ia1  = (res_duel[ia1.nom] / nb_parties) * 100
                taux_ia2  = (res_duel[ia2.nom] / nb_parties) * 100
                taux_nuls = (res_duel['nuls']   / nb_parties) * 100

                # ---------------------- Affichage console -----------------
                print("Résultats :")
                print(f"  {ia1.nom} victoires : {res_duel[ia1.nom]} ({taux_ia1:.1f}%)")
                print(f"  {ia2.nom} victoires : {res_duel[ia2.nom]} ({taux_ia2:.1f}%)")
                print(f"  Nuls : {res_duel['nuls']} ({taux_nuls:.1f}%)")
                print("Performance :")
                print(f"  Temps total : {perf['temps_total']:.2f}s")
                print(f"  Moyenne par partie : {perf['moyenne_par_partie']:.4f}s")
                print(f"  {ia1.nom} score total : {perf['ia1_score_total']:.2f}")
                print(f"  {ia2.nom} score total : {perf['ia2_score_total']:.2f}")
                print(f"  {ia1.nom} score moyen par coup : {perf['ia1_score_moyen_par_coup']:.2f}")
                print(f"  {ia2.nom} score moyen par coup : {perf['ia2_score_moyen_par_coup']:.2f}")
                print()

                # Stocke les infos pour un éventuel export/reporting
                res_global.append({
                    'duel': f"{ia1.nom} vs {ia2.nom}",
                    'resultats': res_duel,
                    'performance': perf
                })

        return res_global


# =============================================================================
# Interface console basique — permet de tester le jeu et les IAs directement
# =============================================================================
def menu_principal():
    """Affiche un menu texte pour démarrer des parties ou un tournoi."""
    from game import humain_vs_humain, humain_vs_ia
    from ai import IAFacile, IAMoyenne, IADifficile

    print("\n=== Projet Morpion Ultime & IA ===")
    print("1. Humain vs Humain")
    print("2. Humain vs IA Facile")
    print("3. Humain vs IA Moyenne")
    print("4. Humain vs IA Difficile")
    print("5. Lancer un tournoi d'IA")
    print("6. Quitter")

    choix = input("Votre choix (1-6) : ")

    # ------------------ Redirige selon le choix utilisateur ------------------
    if choix == '1':
        humain_vs_humain()
    elif choix == '2':
        humain_vs_ia(IAFacile('O'))
    elif choix == '3':
        humain_vs_ia(IAMoyenne('O'))
    elif choix == '4':
        humain_vs_ia(IADifficile('O'))
    elif choix == '5':
        parties = int(input("Nombre de parties par duel (défaut 10) : ") or 10)
        tournoi = Tournoi()
        tournoi.tournoi_complet(parties)
    elif choix == '6':
        print("Au revoir !")
        return
    else:
        print("Choix invalide. Veuillez réessayer.")

    # Après une partie ou un tournoi, propose de revenir au menu principal
    if choix != '6':
        input("\nAppuyez sur Entrée pour revenir au menu...")
        menu_principal()


# Point d’entrée du script ----------------------------------------------------
if __name__ == "__main__":
    menu_principal()
