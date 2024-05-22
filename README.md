# pacman-python-si4

Ce projet a été réalisé dans le cadre du cours d'introduction à l'intelligence artificielle. Le but de ce projet est de créer une version autonome du jeu Pac-Man.

## Table des matières

1. [Introduction](#introduction)
2. [Fonctionnalités](#fonctionnalités)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Contributeurs](#contributeurs)

## Introduction

Ce projet vise à implémenter une version autonome du jeu Pac-Man où l'agent Pac-Man est capable de prendre des décisions intelligentes pour éviter les fantômes et collecter tous les points dans le labyrinthe. 

## Fonctionnalités

- Mouvement autonome de Pac-Man: 
   - 3 modes de déplacement : recherche, fuite et chasse
   - mode recherche par défaut : pac-man va chercher la pac-gomme la plus proche
   - mode fuite si un fantôme est trop proche de pac-man jusqu'à ce que qu'il soit assez loin
   - mode chasse lorsque pac-man mange une super pac-gomme, il se met à chasser les fantômes.
- Movement autonome des fantômes.
- Système de scoring
- Interface graphique pour visualiser le jeu.

## Prérequis

- Python 3.x
- Tkinter (`pip install tk`)

## Installation

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/Matt307082/pacman-python-si4
    cd pacman-python-si4
    ```

## Utilisation

Lancement du script principal :
```bash
python PACMAN.py
```

## Contributeurs

Matteo BEGHELLI : [Github Profile](https://github.com/Matt307082)  
Timothée DUMAS : [Github Profile](https://github.com/71m07h33)