# Ultimate Tic-Tac-Toe avec Intelligence Artificielle

## 📌 Présentation

Bienvenue dans le projet **Ultimate Tic-Tac-Toe**, une version avancée du jeu classique Tic-Tac-Toe (Morpion) intégrant des intelligences artificielles de différents niveaux. Ce projet a été réalisé dans le cadre d’un cours d’Intelligence Artificielle pour explorer la modélisation de jeu, les algorithmes de décision et l’évaluation de performances d’IA.

## 🎯 Objectifs pédagogiques

* Modéliser un jeu à information parfaite (Ultimate Tic-Tac-Toe).
* Implémenter trois niveaux d’intelligence artificielle :

  * IA Facile : heuristique simple avec choix aléatoire.
  * IA Moyenne : algorithme Minimax avec profondeur limitée.
  * IA Difficile : Minimax avec élagage alpha-bêta et heuristiques avancées.
* Comparer les performances des IA à travers des tournois automatisés.

## 🚀 Installation

### Prérequis

* Windows avec Python 3.7+ installé.
* PyInstaller (installé automatiquement avec `build_exe.bat`).

### Création de l’exécutable

1. Double-cliquez sur le fichier `build_exe.bat`.
2. L’exécutable `Ultimate_TicTacToe.exe` sera créé dans le dossier `dist/`.

### Lancement du jeu

* Double-cliquez sur `launch_tictactoe.bat` pour lancer le jeu directement.
* Si vous préférez utiliser l’exécutable directement :

  ```
  dist\Ultimate_TicTacToe.exe
  ```

### ⚠️ Remarque pour utilisateurs MacOS/Linux

Cet exécutable est conçu pour Windows uniquement. Sur MacOS/Linux, il ne fonctionnera probablement pas. Vous pouvez exécuter le jeu directement avec Python :

```bash
python main.py
```

Si vous souhaitez créer un exécutable pour MacOS/Linux, utilisez :

```bash
python -m PyInstaller --onefile --name "Ultimate_TicTacToe" main.py
```

## 🎮 Règles du jeu

* Ultimate Tic-Tac-Toe se joue sur un grand plateau de 9 sous-plateaux 3x3.
* Un joueur doit gagner trois sous-plateaux alignés pour remporter la partie.
* Chaque coup envoie l’adversaire dans un sous-plateau précis.
* Une IA peut remplacer l’adversaire humain selon votre choix.

## 💡 Options de jeu

* Humain vs Humain
* Humain vs IA Facile
* Humain vs IA Moyenne
* Humain vs IA Difficile
* Tournoi d'IA (IA Facile vs IA Moyenne vs IA Difficile)

## ⚡ Architecture du code

* **main.py** : point d'entrée, lance le menu principal.
* **game.py** : logique du jeu (gestion des plateaux).
* **ai.py** : trois niveaux d’intelligence artificielle.
* **tournament.py** : module de gestion des tournois d’IA.

## 📂 Distribution

* `build_exe.bat` : créer l’exécutable `.exe`.
* `launch_tictactoe.bat` : lancer directement l’exécutable.
* `dist/Ultimate_TicTacToe.exe` : le jeu prêt à être lancé.

## 🔧 Dépannage

* Si l’exécutable ne se lance pas, vérifiez que Python est bien installé et que PyInstaller est à jour.
* Si vous rencontrez une erreur, contactez-nous.

## 📞 Contact

Mohammed Ryad DERMOUCHE
Email : [dermoucheryad.com](mailto:votre-email@example.com)

Abdelwaheb SEBA
Email : [abdelwaheb.seba@gmail.com](mailto:votre-email@example.com)
