# -----------------------------------------------------------------------------
# main.py — Point d’entrée du projet
# -----------------------------------------------------------------------------
# Ce fichier lance simplement le menu principal en console, qui permet :
#   • de jouer en local (humain vs humain)
#   • de jouer contre une IA (facile, moyenne ou difficile)
#   • de lancer un tournoi automatique entre IA
#
# > Le cœur du jeu et des IA se trouve dans les fichiers :
#     - game.py       → logiques de plateau, règles du jeu
#     - ai.py         → heuristiques, IA Facile/Moyenne/Difficile
#     - tournament.py → menu console + tournois automatisés
# -----------------------------------------------------------------------------

from tournament import menu_principal  # Importe le menu principal (console)

# Lancement principal du programme si exécuté directement
if __name__ == "__main__":
    menu_principal()  # Affiche le menu interactif (voir tournament.py)
