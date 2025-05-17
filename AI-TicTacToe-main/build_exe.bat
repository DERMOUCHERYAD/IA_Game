@echo off
:: Script pour créer l'exécutable de Ultimate Tic-Tac-Toe avec PyInstaller

:: Vérification de Python et PyInstaller
python --version >nul 2>&1 || (
  echo Python n'est pas installé. Veuillez installer Python 3.7+.
  exit /b
)

pip show pyinstaller >nul 2>&1 || (
  echo PyInstaller n'est pas installé. Installation...
  pip install pyinstaller
)

:: Création de l'exécutable avec PyInstaller via Python
python -m PyInstaller --onefile --name "Ultimate_TicTacToe" main.py

:: Résultat
if exist dist\Ultimate_TicTacToe.exe (
  echo Exécutable créé avec succès dans le dossier dist\.
  echo Vous pouvez le lancer avec launch_tictactoe.bat
) else (
  echo Erreur lors de la création de l'exécutable.
)

pause
