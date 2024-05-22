# region Imports

import random, time
import tkinter as tk
from tkinter import font as tkfont
import numpy as np

# endregion


##############################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
##############################################################################


# region Plan

#########################################################################
#   Plan du labyrinthe
#########################################################################

# 0 : Vide
# 1 : Mur
# 2 : Maison des fantomes, ils peuvent circuler mais pas pacman


# Transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
    return T


TBL = CreateArray(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
)

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]

# endregion


# region Classes


# region Perso

#########################################################################
#   Perso : Définit personnage du jeux
#########################################################################


class Perso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = {
            "up": TBL[self.x][self.y - 1],
            "down": TBL[self.x][self.y + 1],
            "right": TBL[self.x + 1][self.y],
            "left": TBL[self.x - 1][self.y],
        }

    def refreshDirection(self):
        self.directions = {
            "up": TBL[self.x][self.y - 1],
            "down": TBL[self.x][self.y + 1],
            "right": TBL[self.x + 1][self.y],
            "left": TBL[self.x - 1][self.y],
        }


# endregion

# region PacMan


#########################################################################
#   PacMan : Définit pacman, héritant de perso
#########################################################################
class PacMan(Perso):
    def __init__(self, x, y):
        Perso.__init__(self, x, y)
        self.modes = ["recherche", "fuite", "chasse"]
        self.currentMode = "recherche"

    def change_mode(self, newMode):
      if(newMode in self.modes):
         self.currentMode = newMode

    def checkPacGum(self):
        global score
        timer = -1
        if GUM[self.x][self.y] == 1:
            score += 100
            GUM[self.x][self.y] = 0
            self.change_mode("chasse")
            timer = time.time()
        return timer

    def checkForModeChange(self):
        if self.currentMode != "chasse":
            if DIST_GHOSTS[self.x][self.y] < 4:
                self.change_mode("fuite")
            else:
                self.change_mode("recherche")


# endregion

# region Ghost


#########################################################################
#   Ghost : Définit les fantôme, héritant de perso
#########################################################################
class Ghost(Perso):
    def __init__(self, x, y, color):
        Perso.__init__(self, x, y)
        self.color = color


# endregion

# endregion


# region Initialisation

#########################################################################
#   Initialisation
#########################################################################


# region PacGum

#########################################################################
#   Initialisation et placement des PacGum
#########################################################################


def PlacementsGUM():
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                random_number = random.randint(1, 10)
                if random_number == 1:
                    GUM[x][y] = 1
    return GUM


GUM = PlacementsGUM()

# endregion


# region PacMan

#########################################################################
#   Initialisation et placement des PacMan
#########################################################################
pacman = PacMan(5, 5)

# endregion


# region Fantômes

#########################################################################
#   Initialisation et placement des fantômes
#########################################################################

Ghosts = []
Ghosts.append(Ghost(LARGEUR // 2, HAUTEUR // 2, "pink"))
Ghosts.append(Ghost(LARGEUR // 2, HAUTEUR // 2, "orange"))
Ghosts.append(Ghost(LARGEUR // 2, HAUTEUR // 2, "cyan"))
Ghosts.append(Ghost(LARGEUR // 2, HAUTEUR // 2, "red"))


def PlacementGHOSTS():
    GHOSTS = np.zeros(TBL.shape, dtype=np.int32)
    for g in Ghosts:
        GHOSTS[g.x][g.y] = 1
    return GHOSTS


def UpdatePosGhosts(g, old_x, old_y):
    global GHOSTS
    GHOSTS[old_x][old_y] = 0
    GHOSTS[g.x][g.y] = 1


GHOSTS = PlacementGHOSTS()


# endregion


# endregion


##############################################################################
#
#  Debug : Affichage des valeurs autours dans les cases
#
##############################################################################


# region Debug : DNT

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# Info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0:
        return
    if y < 0:
        return
    if x >= LTBL:
        return
    if y >= LTBL:
        return
    TBL2[x][y] = info


def DisplayDistInfos():
    # Utilisation SetInfo
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                # Information PacGum
                SetInfo1(x, y, DIST_GUM[x][y])
                # Information Ghosts
                SetInfo2(x, y, DIST_GHOSTS[x][y])


# endregion


##############################################################################
#
#   Partie II :  Affichage
#
##############################################################################


# region Affichage : DNT

ZOOM = 40  # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == " ":
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)  # Previously 333


Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family="Arial", size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background="black")


#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1 and TBL[x + 1][y] == 1:
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if TBL[x][y] == 1 and TBL[x][y + 1] == 1:
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine pacman
    xx = To(pacman.x)
    yy = To(pacman.y)
    e = 20
    anim_bouche = (anim_bouche + 1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=PacmanColor)
    canvas.create_polygon(
        xx, yy, xx + e, yy + ouv_bouche, xx + e, yy - ouv_bouche, fill="black"
    )  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P.x)
        yy = To(P.y)
        e = 16

        coul = P.color
        # corps du fantome
        CreateCircle(dec + xx, dec + yy - e + 6, e, coul)
        canvas.create_rectangle(
            dec + xx - e,
            dec + yy - e,
            dec + xx + e + 1,
            dec + yy + e,
            fill=coul,
            width=0,
        )

        # oeil gauche
        CreateCircle(dec + xx - 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx - 7, dec + yy - 8, 3, "black")

        # oeil droit
        CreateCircle(dec + xx + 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx + 7, dec + yy - 8, 3, "black")

        dec += 3

    # texte

    canvas.create_text(
        screeenWidth // 2,
        screenHeight - 50,
        text="PAUSE : PRESS SPACE",
        fill="yellow",
        font=PoliceTexte,
    )
    canvas.create_text(
        screeenWidth // 2,
        screenHeight - 20,
        text=message,
        fill="yellow",
        font=PoliceTexte,
    )
    if GAME_OVER:
        canvas.create_text(
            screeenWidth // 2,
            screenHeight // 2,
            text="GAME OVER",
            fill="yellow",
            font=PoliceTexte,
        )


AfficherPage(0)

# endregion


##############################################################################
#
#  Partie III :   Gestion de partie
#
##############################################################################


# region Variables globales

GAME_OVER = False

score = 0

# endregion


# region Intelligence Artificielle


def IAPacman():
    # Utilisation PacMan gloable
    global pacman

    # Déplacement Pacman
    if pacman.currentMode == "recherche":
        move = PacManMinimalMoveToPacgum(PacManPossibleMove())
    elif pacman.currentMode == "fuite":
        move = PacManFleeMove(PacManPossibleMove())
    elif pacman.currentMode == "chasse":
        move = PacManMinimalMoveToGhost(PacManPossibleMove())
    pacman.x += move[0]
    pacman.y += move[1]
    pacman.refreshDirection()
    timer = pacman.checkPacGum()
    pacman.checkForModeChange()
    DisplayDistInfos()
    return timer


def IAGhosts():
    # Déplacement Fantome
    for F in Ghosts:
        L = GhostsPossibleMove(F)
        choix = random.randrange(len(L))
        old_x, old_y = F.x, F.y
        F.x += L[choix][0]
        F.y += L[choix][1]
        F.refreshDirection()
        UpdatePosGhosts(F, old_x, old_y)
        DisplayDistInfos()


# endregion


# region Possible Moves


def PacManPossibleMove():
    global pacman
    L = []
    if pacman.directions["up"] == 0:
        L.append((0, -1))
    if pacman.directions["down"] == 0:
        L.append((0, 1))
    if pacman.directions["right"] == 0:
        L.append((1, 0))
    if pacman.directions["left"] == 0:
        L.append((-1, 0))
    return L


def PacManMinimalMoveToPacgum(possibleMoves):
    global pacman
    moveValues = {
        move: DIST_GUM[pacman.x + move[0]][pacman.y + move[1]] for move in possibleMoves
    }
    minimalMove = min(moveValues, key=moveValues.get)
    return minimalMove


def PacManFleeMove(possibleMoves):
    global pacman
    moveValues = {
        move: DIST_GHOSTS[pacman.x + move[0]][pacman.y + move[1]]
        for move in possibleMoves
    }
    maximalMove = max(moveValues, key=moveValues.get)
    return maximalMove


def PacManMinimalMoveToGhost(possibleMoves):
    global pacman
    moveValues = {
        move: DIST_GHOSTS[pacman.x + move[0]][pacman.y + move[1]]
        for move in possibleMoves
    }
    minimalMove = min(moveValues, key=moveValues.get)
    return minimalMove


def GhostsPossibleMove(ghost):
    L = []
    if ghost.directions["up"] != 1:
        L.append((0, -1))
    if ghost.directions["down"] != 1:
        L.append((0, 1))
    if ghost.directions["right"] != 1:
        L.append((1, 0))
    if ghost.directions["left"] != 1:
        L.append((-1, 0))
    return L


# endregion


# region Carte distances


def InitializeDistanceMap(inputMap):
    outputMap = np.full(
        TBL.shape, fill_value=100, dtype=np.int32
    )  # On remplie un nouveau tableau, de la forme de TBL avec la valeur 100
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if inputMap[x][y] == 1:
                outputMap[x][y] = 0
            # Dès lors qu'on est sur une case recherchée, on l'initialize à 0
    return outputMap


DIST_GUM = InitializeDistanceMap(GUM)
DIST_GHOSTS = InitializeDistanceMap(GHOSTS)


def UpdateDistanceMap(inputMap, outputMap):
    rows, cols = len(inputMap) - 1, len(inputMap[0]) - 1
    hasBeenModified = True
    while hasBeenModified:
        # On garde une copie pour la comparer après
        oldOutputMap = outputMap

        # On parcours le tableau pour mettre à jours les valeurs
        for row in range(rows):
            for col in range(cols):
                # Remet la position des fantômes à 0 sur la carte, s'il ne sont pas dans la maison
                if inputMap[row][col] == 1 and TBL[row][col] != 2:
                    outputMap[row][col] = 0
                # Vérifie si : On n'est pas sur une pacgum, un mur ou une maison
                elif (
                    inputMap[row][col] != 1
                    and TBL[row][col] != 1
                    and TBL[row][col] != 2
                ):
                    neighbors = InitializeNeighbors(row, col, outputMap)
                    if len(neighbors) != 0:
                        outputMap[row][col] = min(neighbors) + 1

        # On test si on a modifié la carte (bug possible)
        hasBeenModified = HasBeenModified(outputMap, oldOutputMap)


def InitializeNeighbors(row, col, outputMap):
    neighbors = []
    if TBL[row + 1][col] != 1 and outputMap[row + 1][col] != 100:
        neighbors.append(outputMap[row + 1][col])
    if TBL[row][col + 1] != 1 and outputMap[row][col + 1] != 100:
        neighbors.append(outputMap[row][col + 1])
    if TBL[row - 1][col] != 1 and outputMap[row - 1][col] != 100:
        neighbors.append(outputMap[row - 1][col])
    if TBL[row][col - 1] != 1 and outputMap[row][col - 1] != 100:
        neighbors.append(outputMap[row][col - 1])
    return neighbors


def HasBeenModified(firstMap, secondMap):
    rows, cols = len(firstMap) - 1, len(secondMap[0]) - 1
    for row in range(rows):
        for col in range(cols):
            if firstMap[row][col] != secondMap[row][col]:
                return True
    return False


# endregion


# region Checkers


def checkCollisionPacmanGhost(pacman, ghosts):
    global GAME_OVER, LARGEUR, HAUTEUR, score
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            if pacman.currentMode == "chasse":
                score += 2000
                GHOSTS[ghost.x][ghost.y] = 0
                ghost.x, ghost.y = LARGEUR // 2, HAUTEUR // 2
            else:
                GAME_OVER = True


# endregion


# region Worker

#########################################################################
#  Worker : Boucle principale de votre jeu appelée toutes les 500ms
#########################################################################

iteration = 0
tour_mode_chasseur = 0


def PlayOneTurn():
    global iteration,tour_mode_chasseur, score, pacman

    if pacman.currentMode == "chasse":
        PacmanColor = "white"
    else:
        PacmanColor = "yellow"

    if not PAUSE_FLAG and not GAME_OVER:
        iteration += 1

        if pacman.currentMode == "chasse":
            tour_mode_chasseur += 1
            if(tour_mode_chasseur == 15):
                pacman.change_mode("recherche")
                tour_mode_chasseur = 0

        if iteration % 2 == 0:
            IAPacman()
            UpdateDistanceMap(GUM, DIST_GUM)
        else:
            IAGhosts()
        checkCollisionPacmanGhost(pacman, Ghosts)
        UpdateDistanceMap(GHOSTS, DIST_GHOSTS)

    Affiche(PacmanColor, message=f"Score : {score}")


# endregion


#########################################################################
#  Demarrage de la fenetre : DNT
#########################################################################

Window.mainloop()
