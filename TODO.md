# TODO List

## In Progress


## Bug Fixes
- [x] Corriger l'erreur de DLL manquante dans l'exécutable

## Planned Features
- [ ] Debug de l'interface PyQt6
    - [ ] Vérifier le fonctionnement des boutons
    - [ ] Tester le redimensionnement de la fenêtre
    - [ ] Valider l'affichage des aperçus PDF
    - [ ] Vérifier la gestion des erreurs
    - [ ] Ajouter un message d'avertissement dans l'interface Qt


## Improvements
- [ ] Système de mise à jour automatique

## Version 1.1.1
- [x] Extraction de texte
    - [x] Ajouter un bouton "Get Text"
    - [x] Implémenter la fonction d'extraction de texte
    - [x] Copie du texte extrait dans le presse papier
- [x] Mise à jour du numéro de version
    - [x] Update version_info pour éviter d'être detecté comme dangereux
- [x] Création de l'exécutable
    - [x] instruction : pyinstaller --onefile --windowed --icon=icon.ico --name="PDF_Editor_v1.1.1" --version-file=version_info.txt e:\Github\PDF_editor\PDF_Editor.py

## Version 1.0.0
- [x] Création de l'exécutable
    - [x] Ajouter une icône pour l'application
    - [x] Résoudre l'erreur d'ordinal 380
    - [x] Tester l'exécutable sur différentes versions de Windows
        - [x] Test sur Window 11
        - [x] Test sur Window 10
    - [x] Vérifier que toutes les dépendances sont incluses
    - [x] Ajouter un numéro de version à l'exécutable