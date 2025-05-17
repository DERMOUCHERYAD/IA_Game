@echo off
:: Lancement automatique de Ultimate Tic-Tac-Toe

if exist dist\Ultimate_TicTacToe.exe (
  echo Lancement de Ultimate Tic-Tac-Toe...
  dist\Ultimate_TicTacToe.exe
) else (
  echo Exécutable non trouvé. Utilisez build_exe.bat pour le créer.
)

pause
