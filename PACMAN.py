# region Imports

import random
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
        [4, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 4],
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

    def RefreshDirection(self):
        self.directions = {
            "up": TBL[self.x][self.y - 1],
            "down": TBL[self.x][self.y + 1],
            "right": TBL[self.x + 1][self.y],
            "left": TBL[self.x - 1][self.y],
        }

    def GetPossibleMoves(self):
        L = []
        if self.directions["down"] == 0:
            L.append((0, 1))
        if self.directions["right"] == 0 or self.directions["right"] == 4:
            L.append((1, 0))
        if self.directions["left"] == 0 or self.directions["left"] == 4:
            L.append((-1, 0))
        if self.directions["up"] == 0:
            L.append((0, -1))
        return L
    
    def CheckTunnel(self):
        if(TBL[self.x][self.y] == 4):
            if(self.x == 0):
                self.x = len(TBL)-2
            else:
                self.x = 1


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
        self.tempo = False
        self.moveToSuperPacGum = (0,0)

    def change_mode(self, newMode):
        if newMode in self.modes:
            self.currentMode = newMode

    def CheckPacGum(self):
        global SCORE, NB_PACGUM
        if GUM[self.x][self.y] == 1:
            SCORE += 100
            GUM[self.x][self.y] = 0
            NB_PACGUM -= 1
        if GUM[self.x][self.y] == 2:
            self.change_mode("chasse")
            GUM[self.x][self.y] = 0
            NB_PACGUM -= 1

    def CheckForModeChange(self):
        if self.currentMode != "chasse":
            if DIST_GHOSTS[self.x][self.y] < 4:
                self.change_mode("fuite")
            else:
                self.change_mode("recherche")

    def CheckForEndTempo(self):
        if(self.tempo):
            if (DIST_GHOSTS[self.x][self.y] < 3):
                self.tempo = False
                return True
        return False
    
    def CheckForEnterTempo(self, move):
        if(GUM[self.x + move[0]][self.y + move[1]] == 2):
            self.tempo = True
            self.moveToSuperPacGum = move
            return True
        return False


# endregion

# region Ghost


#########################################################################
#   Ghost : Définit les fantôme, héritant de perso
#########################################################################
class Ghost(Perso):
    def __init__(self, x, y, color):
        Perso.__init__(self, x, y)
        self.color = color
        self.lastDirection = "up"


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


NB_PACGUM = 0

def PlacementsGUM():
    global NB_PACGUM
    GUM = np.zeros(TBL.shape, dtype=np.int32)

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 0:
                GUM[x][y] = 1
                NB_PACGUM += 1

    # Positionnement des super pac gommes dans les 4 coins
    GUM[1][1] = 2
    GUM[1][HAUTEUR - 2] = 2
    GUM[LARGEUR - 2][1] = 2
    GUM[LARGEUR - 2][HAUTEUR - 2] = 2
    NB_PACGUM += 4

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
            if TBL[x][y] == 0 or TBL[x][y] == 4:
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
    Window.after(333, WindowAnim)


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

    # pacgum et super pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1:
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")
            elif GUM[x][y] == 2:
                xx = To(x)
                yy = To(y)
                e = 7
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="white")

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
    if WIN:
        canvas.create_text(
            screeenWidth // 2,
            screenHeight // 2,
            text="YOU WIN",
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
WIN = False

SCORE = 0

# endregion


# region Intelligences Artificielles


def IAPacman():
    # Utilisation PacMan globale
    global pacman

    endtempo = pacman.CheckForEndTempo()
    if(not pacman.tempo):
        pacman.RefreshDirection()

        # Déplacement Pacman
        if pacman.currentMode == "recherche":
            move = PacManMinimalMoveToPacGum(pacman.GetPossibleMoves())
        elif pacman.currentMode == "fuite":
            move = PacManFleeMove(pacman.GetPossibleMoves())
        elif pacman.currentMode == "chasse":
            move = PacManMinimalMoveToGhost(pacman.GetPossibleMoves())

        if(endtempo):
                pacman.x += pacman.moveToSuperPacGum[0]
                pacman.y += pacman.moveToSuperPacGum[1]
        elif(not pacman.CheckForEnterTempo(move)):
                pacman.x += move[0]
                pacman.y += move[1]

        pacman.CheckTunnel()
        pacman.CheckPacGum()
        pacman.CheckForModeChange()

    DisplayDistInfos()


def IAGhosts():
    # Utilisation PacMan globale
    global pacman

    # Déplacement Fantome
    for F in Ghosts:
        F.RefreshDirection()
        old_x, old_y = F.x, F.y

        if TBL[F.x][F.y] == 2:
            p_sortir = random.randint(1,10)
            if(p_sortir == 1):
                F.y -= 2
            else :
                continue

        elif IsInCorridor(F):
            if F.lastDirection == "up":
                F.y -= 1
            elif F.lastDirection == "down":
                F.y += 1
            elif F.lastDirection == "left":
                F.x -= 1
            elif F.lastDirection == "right":
                F.x += 1

        else:
            L = F.GetPossibleMoves()
            move = L[random.randint(0, len(L) - 1)]
            F.x += move[0]
            F.y += move[1]
            F.lastDirection = GetLastDirection(move)

        F.CheckTunnel()
        UpdatePosGhosts(F, old_x, old_y)
        UpdateDistanceMap(GHOSTS, DIST_GHOSTS)
        DisplayDistInfos()


# endregion


# region Gestions Mouvement


# region PacMan Moves


def PacManMinimalMoveToPacGum(possibleMoves):
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


# endregion


# region Ghosts Moves


def IsInCorridor(ghost):
    if TBL[ghost.x + 1][ghost.y] == 1 and TBL[ghost.x - 1][ghost.y] == 1:
        return True
    elif TBL[ghost.x][ghost.y + 1] == 1 and TBL[ghost.x][ghost.y - 1] == 1:
        return True
    return False


def GetLastDirection(move): 
    if move == (1, 0):
        return "right"
    elif move == (0, 1):
        return "down"
    elif move == (-1, 0):
        return "left"
    return "up"


# endregion


# endregion


# region Carte distances


def InitializeDistanceMap(inputMap):
    outputMap = np.full(
        TBL.shape, fill_value=100, dtype=np.int32
    )  # On remplie un nouveau tableau, de la forme de TBL avec la valeur 100
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if inputMap[x][y] != 0:
                outputMap[x][y] = 0
            # Dès lors qu'on est sur une case recherchée, on l'initialize à 0
    return outputMap


DIST_GUM = InitializeDistanceMap(GUM)
DIST_GHOSTS = InitializeDistanceMap(GHOSTS)
# DIST_HOUSE = Initialize


def UpdateDistanceMap(inputMap, outputMap):
    rows, cols = len(inputMap) - 1, len(inputMap[0]) - 1
    hasBeenModified = True
    while hasBeenModified:
        # On garde une copie pour la comparer après
        oldOutputMap = outputMap.copy()

        # On parcours le tableau pour mettre à jours les valeurs
        for row in range(rows):
            for col in range(cols):
                # Remet la position des fantômes à 0 sur la carte, s'il ne sont pas dans la maison
                if inputMap[row][col] != 0 and TBL[row][col] != 2:
                    outputMap[row][col] = 0

                # Vérifie si : On n'est pas sur une pacgum, un mur ou une maison
                elif inputMap[row][col] != 1 and TBL[row][col] != 1 and TBL[row][col] != 4:
                    neighbors = InitializeNeighbors(row, col, outputMap)
                    if len(neighbors) != 0:
                        outputMap[row][col] = min(neighbors) + 1

                # Modification des distances en prenant en compte le tunnel
                if row == 0:
                    if(TBL[row][col] == 4):
                        outputMap[row+1][col] = min(outputMap[row+1][col],outputMap[rows-1][col])
                        outputMap[row][col] = outputMap[row+1][col]
                        outputMap[rows-1][col] = outputMap[row][col]
                if row+1 == rows:
                    if(TBL[row+1][col] == 4):
                        outputMap[row][col] = min(outputMap[1][col]+1,outputMap[row][col])
                        outputMap[row+1][col] = outputMap[row][col]
                        outputMap[0][col] = outputMap[row][col]

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
    global GAME_OVER, LARGEUR, HAUTEUR, SCORE
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            if pacman.currentMode == "chasse":
                SCORE += 2000
                GHOSTS[ghost.x][ghost.y] = 0
                ghost.x, ghost.y = LARGEUR // 2, HAUTEUR // 2
            else:
                GAME_OVER = True

def checkWin():
    global WIN, NB_PACGUM
    if(NB_PACGUM == 0):
        WIN = True   


# endregion


# region Worker

#########################################################################
#  Worker : Boucle principale de votre jeu appelée toutes les 500ms
#########################################################################

iteration = 0
tour_mode_chasseur = 0


def PlayOneTurn():
    global iteration, tour_mode_chasseur, SCORE, pacman

    if pacman.currentMode == "chasse":
        PacmanColor = "white"
    else:
        PacmanColor = "yellow"

    if not PAUSE_FLAG and not GAME_OVER and not WIN:
        iteration += 1

        if pacman.currentMode == "chasse":
            tour_mode_chasseur += 1
            if tour_mode_chasseur == 25:
                pacman.change_mode("recherche")
                tour_mode_chasseur = 0

        if iteration % 2 == 0:
            IAPacman()
            UpdateDistanceMap(GUM, DIST_GUM)
            checkWin()
        else:
            IAGhosts()
        checkCollisionPacmanGhost(pacman, Ghosts)

    Affiche(PacmanColor, message=f"SCORE : {SCORE}")


# endregion


#########################################################################
#  Demarrage de la fenetre : DNT
#########################################################################

Window.mainloop()
