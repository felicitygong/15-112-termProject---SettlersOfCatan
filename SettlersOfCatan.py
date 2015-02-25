#Felicity Gong, Section Q, felicitg
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
from random import randint
from math import *
import copy

class Player(object):
    def __init__(self, color):
        self.color = color
        self.roadsLeft = 15
        self.settlementsLeft = 5
        self.citiesLeft = 4
        self.resourceCards = []
        self.devCards = []
        self.knightsPlayed = 0
        self.VP = 0

    def reduceCards(self):
        self.resourceCards = self.resourceCards[:len(self.resourceCards)/2]

    def __str__(self):
        return "Player(%s)" % (self.color)

    def __eq__(self, other):
        if (type(other) != int):
            return self.color == other.color

    def __ne__(self, other):
        if (type(other) != int):
            return not(self.color == other.color)
        else: return True
            
class SettlersOfCatan(EventBasedAnimationClass):
    def __init__(self, width=1350, height=700):
        super(SettlersOfCatan, self).__init__(width, height)
        self.width = width
        self.height = height

    def boards(self):
        self.makeResourcesBoard()
        self.makeSettlementsAndCitiesBoard()
        self.makeRoadsBoard()

    def makeResourcesBoard(self):
        #index of associated vertices
        resources = ['brick', 'brick', 'brick', 'ore', 'ore', 'ore', 'wheat',
                     'wheat', 'wheat', 'wheat', 'wood', 'wood', 'wood', 'wood',
                     'sheep', 'sheep', 'sheep', 'sheep', 'desert']
        tokens = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
        tiles = [[(0, 1, 2, 8, 9, 10)], [(2, 3, 4, 10, 11, 12)],
                 [(4, 5, 6, 12, 13, 14)], [(7, 8, 9, 17, 18, 19)],
                 [(9, 10, 11, 19, 20, 21)], [(11, 12, 13, 21, 22, 23)],
                 [(13, 14, 15, 23, 24, 25)], [(16, 17, 18, 27, 28, 29)],
                 [(18, 19, 20, 29, 30, 31)], [(20, 21, 22, 31, 32, 33)],
                 [(22, 23, 24, 33, 34, 35)], [(24, 25, 26, 35, 36, 37)],
                 [(28, 29, 30, 38, 39, 40)], [(30, 31, 32, 40, 41, 42)],
                 [(32, 33, 34, 42, 43, 44)], [(34, 35, 36, 44, 45, 46)],
                 [(39, 40, 41, 47, 48, 49)], [(41, 42, 43, 49, 50, 51)],
                 [(43, 44, 45, 51, 52, 53)]]
        for tile in xrange(0, len(resources)):
            tiles[tile].insert(0, (resources.pop(randint(0, len(resources)-1))))
        for tile in xrange(0, len(tiles)):
            if (tiles[tile][0] == 'desert'):
                tiles[tile].insert(0, [True, 0])
                self.robberPlace = tile
            else: tiles[tile].insert(0, [False,
                                         tokens.pop(randint(0, len(tokens)-1))])
        self.resourcesBoard = tiles

    def makeSettlementsAndCitiesBoard(self):
        #list of indexes to indicate the player and settlement or city
        vertices = [[0, 0] for i in xrange(54)]
        self.settlements = vertices

    def makeRoadsBoard(self):
        settlements = self.settlements
        #number of possible roads
        roads = []
        for point in xrange(0, len(settlements)-1):
            if (point not in [6, 15, 26, 37, 46]):
                roads += [[(point, point+1), 0]]
        for point in xrange(0, 7, 2):
            roads += [[(point, point+8), 0]]
        for point in xrange(7, 16, 2):
            roads += [[(point, point+10), 0]]
        for point in xrange(39, 46, 2):
            roads += [[(point, point+8), 0]]
        for point in xrange(28, 37, 2):
            roads += [[(point, point+10), 0]]
        for point in xrange(16, 27, 2):
            roads += [[(point, point+11), 0]]
        self.roadsBoard = roads

    def rollDice(self):
        self.rollDisplay = True
        self.dice1 = randint(1, 6)
        self.dice2 = randint(1, 6)
        self.roll = self.dice1 + self.dice2
        if (self.roll != 7):
            self.distributeResources()
        else:
            self.activateRobber = True
            self.text = "Move the robber"
            self.max7()

    def distributeResources(self):
        for resource in self.resourcesBoard:
            if ((resource[0][1] == self.roll) and (resource[0][0] == False)):
                for corner in resource[2]:
                    if (self.settlements[corner][1] != 0):
                        if (self.settlements[corner][1] == 'settlement'):
                            self.players[self.players.index(self.settlements[corner][0])].resourceCards.append(resource[1])
                        else:
                            self.players[self.players.index(self.settlements[corner][0])].resourceCards += [resource[1]]*2

    def moveRobber(self, tile):
        if (self.resourcesBoard[tile][0][0] == False):
            for corner in self.resourcesBoard[tile][2]:
                if (self.settlements[corner][0] == self.players[(self.players.index(self.playerTurn)+1)%len(self.players)]):
                    self.resourcesBoard[tile][0][0] = True
                    self.resourcesBoard[self.robberPlace][0][0] = False
                    self.robberPlace = tile
                    self.activateRobber = False
                    self.stealing = True
                    self.text = "Steal from a player on this tile"
                    break

    def steal(self, player):
        legalPlayers = []
        for corner in self.resourcesBoard[self.robberPlace][2]:
            if ((self.settlements[corner][0] != 0) and
                (self.settlements[corner][0] not in legalPlayers)):
                legalPlayers += [self.settlements[corner][0]]
        for person in legalPlayers:
            if person == player:
                thief = self.playerTurn
                card = randint(0, len(player.resourceCards)-1)
                thief.resourceCards += [player.resourceCards.pop(card)]
                self.stealing = False
                self.text = ""

    def max7(self):
        for player in self.players:
            if (len(player.resourceCards) > 7):
                player.reduceCards()

    def initAnimation(self):
        self.images()
        self.bonuses = ['longest road', 'largest army']
        self.boards()
        self.colors = ["blue", "red", "orange", "white"]
        self.text = ""
        self.turn = 0
        self.players = []
        self.devCards = ['knight', 'knight', 'knight', 'knight', 'knight',
                         'knight', 'knight', 'knight', 'knight', 'knight',
                         'knight', 'knight', 'knight', 'knight', 'VP', 'VP',
                         'VP', 'VP', 'VP', 'monopoly', 'monopoly',
                         'roadBuilding', 'roadBuilding', 'yearOfPlenty',
                         'yearOfPlenty']
        self.inPlayGameStates()
        (cx, cy) = (250, 225)
        self.centers = self.findHexCenters(cx, cy)
        self.hexPoints = self.findHexPoints(self.centers)
        self.intersections = self.findIntersectionPoints(self.hexPoints)
        self.roadsPoints = self.findRoads(self.intersections)

    def inPlayGameStates(self):
        self.displayStartScreen = True
        self.displayHelpScreen = False
        self.displayPlayerSelection = False
        self.gameInPlay = False
        self.isGameOver = False
        self.buildRoad = False
        self.buildSettlement = False
        self.buildCity = False
        self.activateRobber = False
        self.stealing = False
        self.rollDisplay = False
        self.monopoly = False
        self.dcroadbuilding = False
        self.yearOfPlenty1 = False
        self.yearOfPlenty2 = False
        
    def images(self):
        self.start = PhotoImage(file="startScreen.gif")
        self.help1 = PhotoImage(file="helpScreen1.gif")
        self.help2 = PhotoImage(file="helpScreen2.gif")
        
    def onMousePressed(self, event):
        (x, y) = (event.x, event.y)
        if (self.displayStartScreen == True):
            if ((x > 3*self.width/8) and (x < 5*self.width/8) and
                (y > 19*self.height/22) and (y < 21*self.height/22)):
                self.displayStartScreen = False
                self.displayHelpScreen = True

        elif (self.displayHelpScreen == True):
            if ((x > 3*self.width/8) and (x < 5*self.width/8) and
                (y > 19*self.height/22) and (y < 21*self.height/22)):
                if (self.help1 != self.help2): self.help1 = self.help2
                else:
                    self.displayHelpScreen = False
                    self.displayPlayerSelection = True

        elif (self.displayPlayerSelection == True):
            self.playerSelection(x, y)
                    
        elif (self.gameInPlay == True):
            self.gamePlayActions(x, y)

    def gamePlayActions(self, x, y):
        #if click in bank box
        if ((x > 7*self.width/12) and (y > self.height/8) and
              (x < 7*self.width/12 + self.width/3) and
              (y < self.height/8+self.height/2)):
            self.bankPressed(x, y)
        elif (self.buildSettlement == True): self.buildingSettlement(x, y)
        elif (self.buildRoad == True): self.buildingRoad(x, y)
        elif (self.buildCity == True): self.buildingCity(x, y)
        elif (self.activateRobber == True):
            tokenRadius = 20
            for center in xrange(len(self.centers)):
                if (((self.centers[center][0]-x)**2+(self.centers[center][1]-y)**2) <= tokenRadius**2):
                    self.moveRobber(center)
        elif (self.stealing == True):
            if ((x > 25) and (x < 25+len(self.players)*75) and
                (y > 2*self.height/3) and (y < 2*self.height/3+25)):
                if (self.players[(x-25)/75] != self.playerTurn):
                    self.steal(self.players[(x-25)/75])
        elif ((x > self.width/2) and (x < self.width) and (y > 3*self.height/4)
              and (y < self.height)):
            position = ((x-self.width/2-5)/50) + ((y-3*self.height/4)/140)
            try:
                card = self.playerTurn.devCards.pop(position)
                self.playDevCard(card)
            except: None
        elif (self.inResourceBank(x, y) == True):            
            resources = ["brick", "wood", "sheep", "wheat", "ore"]
            resource = resources[(x-(self.left+125))/50]
            for r in resources:
                if (r != resource) and (self.playerTurn.resourceCards.count(r) >= 4):
                    count = 0
                    while count < 4:
                        self.playerTurn.resourceCards.pop(self.playerTurn.resourceCards.index(r))
                        count += 1
                    self.playerTurn.resourceCards.append(resource)
            else: self.devCardActions(x)

    def devCardActions(self, x):
        if (self.monopoly == True):
            resources = ["brick", "wood", "sheep", "wheat", "ore"]
            resource = resources[(x-(self.left+125))/50]
            self.takeMonopoly(resource)
        elif (self.yearOfPlenty1 == True):
            resources = ["brick", "wood", "sheep", "wheat", "ore"]
            resource = resources[(x-(self.left+125))/50]
            self.playerTurn.resourceCards.append(resource)
            self.yearOfPlenty1 = False
            self.text = "Select another resource to take from the bank"
            self.yearOfPlenty2 = True
        elif (self.yearOfPlenty2 == True):
            resources = ["brick", "wood", "sheep", "wheat", "ore"]
            resource = resources[(x-(self.left+125))/50]
            self.playerTurn.resourceCards.append(resource)
            self.yearOfPlenty2 = False
            self.text = ""

    def inResourceBank(self, x, y):
        if ((x > self.left+self.length/5) and (x < self.left + 4*self.length/5)
            and (y > self.top+self.tall) and (y < self.top + 19*self.tall/16)):
            return True

    def onKeyPressed(self, event):
        if (event.char == "a"): self.playerTurn.VP += 7
        elif (self.isGameOver == True) and (event.char == "r"):
            self.initAnimation()

    def playDevCard(self, card):
        if (card == "knight"): self.playKnight()
        elif (card == "VP"): self.playVP()
        elif (card == "monopoly"): self.playMonopoly()
        elif (card == "roadBuilding"): self.playRoadBuilding()
        elif (card == "yearOfPlenty"): self.playYearOfPlenty()

    def playKnight(self):
        self.text="Place the robber and steal 1 card from another player"
        self.activateRobber = True
        self.text = "Move the robber"
        self.playerTurn.knightsPlayed += 1

    def playVP(self):
        self.text="You just gained a victory point"
        self.players[self.players.index(self.playerTurn)].VP += 1
        self.checkWinner()

    def playMonopoly(self):
        self.text="Select a resource to take from all the other players"
        self.monopoly = True

    def takeMonopoly(self, resource):
        for player in self.players:
            if player != self.playerTurn:
                while resource in player.resourceCards:
                    card = player.resourceCards.pop(player.resourceCards.index(resource))
                    self.playerTurn.resourceCards.append(card)
                    self.monopoly = False
                    self.text = ""

    def playRoadBuilding(self):
        self.text="Place 2 roads"
        self.buildRoad = True
        self.dcroadbuilding = True

    def playYearOfPlenty(self):
        self.text="Select two resources to take from the bank"
        self.yearOfPlenty1 = True

    def bankPressed(self, x, y):
        left = self.left
        top = self.top
        width = self.length
        height = self.tall
        if ((x > left+width/12) and (x < left + 11*width/12) and
            (y > top+height/8+2) and (y < top+2*height/8-2)):
            self.buyRoad()
        elif ((x > left+width/12) and (x < left + 11*width/12) and
              (y > top+2*height/8+2) and (y < top+3*height/8-2)):
            self.buySettlement()
        elif ((x > left+width/12) and (x < left + 11*width/12) and
              (y > top+3*height/8+2) and (y < top+4*height/8-2)):
            self.buyCity()
        elif ((x > left+width/12) and (x < left + 11*width/12) and
              (y > top+4*height/8+2) and (y < top+5*height/8-2)):
            self.buyDevCard()
            
        elif ((x > left+3*width/8) and (x < left+11*width/8) and
              (y > top+6*height/8+2) and (y < top+7*height/8-2)):
            if ((self.turn < len(self.players)) and
                (self.playerTurn.roadsLeft == 14) and
                (self.playerTurn.settlementsLeft == 4)):
                 self.nextTurn()
            elif ((self.turn < 2*len(self.players)) and
                (self.playerTurn.roadsLeft == 13) and
                (self.playerTurn.settlementsLeft == 3)):
                  self.nextTurn()
            elif (self.activateRobber == False) and (self.stealing == False):
                  self.nextTurn()

    def buyRoad(self):
        if (("brick" in self.playerTurn.resourceCards) and
            ("wood" in self.playerTurn.resourceCards) and
            (self.playerTurn.roadsLeft > 0)):
            self.buildRoad = True
            self.text = "Place a road"
            self.playerTurn.resourceCards.remove("brick")
            self.playerTurn.resourceCards.remove("wood")

    def buySettlement(self):
        if (("brick" in self.playerTurn.resourceCards) and
            ("wood" in self.playerTurn.resourceCards) and
            ("wheat" in self.playerTurn.resourceCards) and
            ("sheep" in self.playerTurn.resourceCards) and
            (self.playerTurn.settlementsLeft > 0)):
            self.buildSettlement = True
            self.text = "Place a settlement"
            self.playerTurn.resourceCards.remove("brick")
            self.playerTurn.resourceCards.remove("wood")
            self.playerTurn.resourceCards.remove("wheat")
            self.playerTurn.resourceCards.remove("sheep")

    def buyCity(self):
        if ((self.playerTurn.resourceCards.count("wheat") >= 2) and
            (self.playerTurn.resourceCards.count("ore") >= 3) and
            (self.playerTurn.citiesLeft > 0)):
            self.buildCity = True
            self.text = "Place a city"
            self.playerTurn.resourceCards.remove("wheat")
            self.playerTurn.resourceCards.remove("wheat")
            self.playerTurn.resourceCards.remove("ore")
            self.playerTurn.resourceCards.remove("ore")
            self.playerTurn.resourceCards.remove("ore")

    def buyDevCard(self):
        if (("sheep" in self.playerTurn.resourceCards) and
            ("wheat" in self.playerTurn.resourceCards) and
            ("ore" in self.playerTurn.resourceCards) and (len(self.devCards) > 0)):
            card = randint(0, len(self.devCards)-1)
            self.playerTurn.devCards.append(self.devCards.pop(card))
            self.playerTurn.resourceCards.remove("sheep")
            self.playerTurn.resourceCards.remove("wheat")
            self.playerTurn.resourceCards.remove("ore")
        
    def buildingRoad(self, x, y):
        for road in xrange(len(self.roads)):
            if (self.onLine(x, y, road) == True):
                if (self.isLegalRoad(self.roadsBoard[road][0]) == True):
                    self.roadsBoard[road][1] = self.playerTurn
                    self.playerTurn.roadsLeft -= 1
                    self.text = ""
                    self.buildRoad = False
                    if self.dcroadbuilding == True:
                        self.buildroad = True
                        self.dcroadbuilding = False
                    
    def onLine(self, x, y, road):
        (Xa, Ya) = self.roads[road][0]
        (Xb, Yb) = self.roads[road][1]
        m = (Xa-Xb)/(Ya-Yb)
        b = Xa-m*Ya
        if ((abs(Xa-Xb) <= 10**-2) and (abs(x-Xa) <= 1) and (y < max(Ya, Yb))
            and (y > min(Ya, Yb))): return True
        elif ((y < max(Ya, Yb)) and (y > min(Ya, Yb)) and (x < max(Xa, Xb)) and
             (x > min(Xa, Xb)) and (abs(x - (m*y + b)) <= 10)):
            return True
        else: return False

    def buildingSettlement(self, x, y):
        points = self.intersections
        for pt in xrange(len(points)):
            if (((points[pt][0]-x)**2+(points[pt][1]-y)**2) <= 10**2):
                if (self.isLegalSettlement(pt) == True):
                    self.settlements[pt][0] = self.playerTurn
                    self.settlements[pt][1] = 'settlement'
                    self.players[self.players.index(self.playerTurn)].VP += 1
                    self.checkWinner()
                    self.playerTurn.settlementsLeft -= 1
                    self.text = ""
                    self.buildSettlement = False
                    if (self.turn <= len(self.players)-1):
                        self.distributeSetup(pt)
                    
    def checkWinner(self):
        if (self.playerTurn.VP == 10):
            self.gameInPlay = False
            self.isGameOver = True

    def distributeSetup(self, pt):
        for resource in self.resourcesBoard:
            if pt in resource[2]:
                if resource[0][0] == False:
                    self.playerTurn.resourceCards += [resource[1]]

    def buildingCity(self, x, y):
        points = self.intersections
        for pt in xrange(len(points)):
            if (((points[pt][0]-x)**2+(points[pt][1]-y)**2) <= 10**2):
                if (self.isLegalCity(pt) == True):
                    self.settlements[pt][0] = self.playerTurn
                    self.settlements[pt][1] = 'city'
                    self.players[self.players.index(self.playerTurn)].VP += 1
                    self.checkWinner()
                    self.playerTurn.citiesLeft -= 1
                    self.playerTurn.settlementsLeft += 1
                    self.text = ""
                    self.buildCity = False

    def isLegalRoad(self, point):
        (x, y) = point
        for road in self.roadsBoard:
            if (self.turn < 2*len(self.players)):
                if (self.settlements[x][0] == self.playerTurn): return True
                elif (self.settlements[y][0] == self.playerTurn): return True
            elif (x in road[0]) and (road[1] == self.playerTurn): return True
            elif (y in road[0]) and (road[1] == self.playerTurn): return True
        return False

    def isLegalSettlement(self, point):
        connectedSettlements = []
        for road in self.roadsBoard:
            if ((road[0][0] == point) and
                (self.settlements[road[0][0]][0] == 0)):
                connectedSettlements += [(self.settlements[road[0][1]][0], road)]
            elif ((road[0][1] == point) and
                  (self.settlements[road[0][1]][0] == 0)):
                connectedSettlements += [(self.settlements[road[0][0]][0], road)]
        for settlement in connectedSettlements:
            if settlement[0] != 0:
                return False
        if (self.turn < 9): return True
        else:
            for settlement in connectedSettlements:
                if (settlement[1][1] == self.playerTurn):
                    return True
        return False

    def isLegalCity(self, point):
        if (self.settlements[point] == [self.playerTurn, 'settlement']):
            return True

    def redrawAll(self):
        if (self.displayStartScreen == True): self.displayScreen()
        elif (self.displayHelpScreen == True): self.drawHelpScreen()
        elif (self.displayPlayerSelection == True): self.drawPlayerSelection()
        elif (self.gameInPlay == True):
            self.canvas.create_rectangle(0, 0, self.width, self.height,
                                         fill="seashell")
            self.drawCatanBoard()
            self.drawSettlementsAndCities()
            self.drawRoads()
            self.drawInfoText()
            self.drawBonuses()
            self.drawBank()
            self.drawPlayerTabs()
            if (self.rollDisplay == True):
                self.drawDice()
        elif (self.isGameOver == True): self.drawGameOver(self.playerTurn)

    @staticmethod
    def findHexCenters(cx, cy):
        sideLength = 50*sqrt(3)
        hexCenter = [[cx, cy]]
        closeCenters = []
        farCenters = []
        for angle in xrange(0, 360, 60):
            closeCenters += [[cx+sideLength*cos(radians(angle)),
                              cy+sideLength*
                              sin(radians(angle))]]
            farCenters += [[cx+2*sideLength*cos(radians(angle)),
                            cy+2*sideLength*sin(radians(angle))]]
        otherFarCenters = []
        for point in xrange(0, len(farCenters)):
            if (point == len(farCenters)-1):
                midpointX = (farCenters[point][0] + farCenters[0][0])/2
                midpointY = (farCenters[point][1] + farCenters[0][1])/2
            else:
                midpointX = (farCenters[point][0] + farCenters[point+1][0])/2
                midpointY = (farCenters[point][1] + farCenters[point+1][1])/2
            otherFarCenters += [[midpointX, midpointY]]
        #want them to be organized by lowest y value, then lowest x value
        centers = hexCenter + closeCenters + farCenters + otherFarCenters
        for center in centers:
            (center[0], center[1]) = (center[1], center[0])
        hexCenters = sorted(centers)
        for center in hexCenters:
            (center[0], center[1]) = (center[1], center[0])
        return (sorted(hexCenters[:3]) + sorted(hexCenters[3:7])+
                sorted(hexCenters[7:12]) + sorted(hexCenters[12:16]) +
                sorted(hexCenters[16:]))

    @staticmethod
    def findHexPoints(centers):
        sideLength = 50
        allHexPoints = []
        for center in centers:
            [cx, cy] =  center
            hexPoints = []
            for angle in xrange(30, 360, 60):
                hexPoints += [(round(cx+sideLength*cos(radians(angle)), 8),
                               round(cy+sideLength*sin(radians(angle)), 8))]
            allHexPoints += [hexPoints]
        return allHexPoints

    def drawCatanBoard(self):
        tiles = self.resourcesBoard
        tokenRadius = 20
        for tile in xrange(len(tiles)):
            if (tiles[tile][1] == 'brick'): color = 'maroon'
            elif (tiles[tile][1] == 'ore'): color = 'grey'
            elif (tiles[tile][1] == 'wheat'): color = 'yellow'
            elif (tiles[tile][1] == 'wood'): color = 'darkGreen'
            elif (tiles[tile][1] == 'sheep'): color = 'lightGreen'
            else: color = 'khaki'
            self.canvas.create_polygon(tuple(self.hexPoints[tile]), fill=color,
                                       outline="black")
            if (tiles[tile][0][0] == False): tokenColor = 'white'
            else: tokenColor = 'black'
            (x, y) = tuple(self.centers[tile])
            self.canvas.create_oval(x-tokenRadius, y-tokenRadius,
                                    x+tokenRadius, y+tokenRadius,
                                    fill=tokenColor)
            self.canvas.create_text(x, y, text=str(tiles[tile][0][1]))

    @staticmethod
    def findIntersectionPoints(hexagons):
        points = []
        for i in xrange(0, len(hexagons)/2+3):
            for j in xrange(len(hexagons[i])/2, len(hexagons[i])):
                if hexagons[i][j] not in points:
                    points += [hexagons[i][j]]
        for i in xrange(len(hexagons)/2-2, len(hexagons)):
            for j in xrange(len(hexagons[i])/2-1, -1, -1):
                if hexagons[i][j] not in points:
                    points += [hexagons[i][j]]
        return points
    
    def drawStar(self, x, y, r, color):
        points = []
        for angle in xrange(270, 630, 360/10):
            if ((angle-270)%(360/5) == 0):
                points += [(x+2*r*cos(radians(angle)), y+2*r*sin(radians(angle)))]
            else:
                points += [(x+r*cos(radians(angle)), y+r*sin(radians(angle)))]
        self.canvas.create_polygon(points, fill=color, outline="black")

    def drawSettlementsAndCities(self):
        r = 10
        intersections = self.intersections
        board = self.settlements
        for point in xrange(len(board)):
            if (isinstance(board[point][0], Player) == True):
                color = board[point][0].color
                if (board[point][1] == 'settlement'):
                    self.canvas.create_oval(intersections[point][0]-r,
                                            intersections[point][1]-r,
                                            intersections[point][0]+r,
                                            intersections[point][1]+r,
                                            fill=color, outline="black")
                else:
                    self.drawStar(intersections[point][0], intersections[point][1],
                                  r, color)

    @staticmethod
    def findRoads(settlements):
        roads = []*72
        for point in xrange(0, len(settlements)-1):
            if (point not in [6, 15, 26, 37, 46]):
                roads += [(settlements[point], settlements[point+1])]
        for point in xrange(0, 7, 2):
            roads += [(settlements[point], settlements[point+8])]
        for point in xrange(7, 16, 2):
            roads += [(settlements[point], settlements[point+10])]
        for point in xrange(39, 46, 2):
            roads += [(settlements[point], settlements[point+8])]
        for point in xrange(28, 37, 2):
            roads += [(settlements[point], settlements[point+10])]
        for point in xrange(16, 27, 2):
            roads += [(settlements[point], settlements[point+11])]
        return roads
    
    def drawRoads(self):
        width = 5
        roads = self.roadsPoints
        board = self.roadsBoard
        for point in xrange(len(board)):
            if (isinstance(board[point][1], Player) == True):
                color = board[point][1].color
                self.canvas.create_line(roads[point][0], roads[point][1],
                                        fill=color, width=width)
        self.roads = roads

    def drawInfoText(self):
        self.canvas.create_text(7*self.width/16, self.height/2,
                                text=self.text)
        

    def drawBonuses(self):
        r = 20
        center = [7*self.width/8, self.height/16]
        if (len(self.bonuses) != 0):
            for bonus in self.bonuses:
                if (bonus == 'longest road'):
                    text="LR"
                    color = "green"
                else:
                    text="LA"
                    color = "red"
                self.canvas.create_oval(center[0] - r, center[1] - r,
                                        center[0] + r, center[1] + r,
                                        fill=color, outline='black')
                self.canvas.create_text(tuple(center), text=text)
                center[0] += self.width/32

    def drawBank(self):
        self.left = left = 7*self.width/12
        self.top = top = self.height/8
        self.length = width = self.width/3
        self.tall = height = self.height/2
        self.canvas.create_rectangle(left, top, left+width, top+height,
                                     fill="khaki", outline="black", width=5)
        self.canvas.create_text(left+width/2, top+height/16,
                                text="Building Costs")
        
        self.canvas.create_rectangle(left+width/12, top+height/8+2,
                                     left+11*width/12, top+2*height/8-2)
        self.canvas.create_text(left+width/2, top+3*height/16,
                                text="Road| Cost: 1 brick, 1 wood")
        
        self.canvas.create_rectangle(left+width/12, top+2*height/8+2,
                                     left+11*width/12, top+3*height/8-2)
        self.canvas.create_text(left+width/2, top+5*height/16,
                                text="Settlement| Cost: 1 brick, 1 wood, 1 sheep, 1 wheat")

        self.canvas.create_rectangle(left+width/12, top+3*height/8+2,
                                     left+11*width/12, top+4*height/8-2)
        self.canvas.create_text(left+width/2, top+7*height/16,
                                text="City| Cost: 2 wheat, 3 ore")
        
        self.canvas.create_rectangle(left+width/12, top+4*height/8+2,
                                     left+11*width/12, top+5*height/8-2)
        self.canvas.create_text(left+width/2, top+9*height/16,
                                text="DevCard| Cost: 1 sheep, 1 wheat, 1 ore")
        
        self.canvas.create_rectangle(left+3*width/8, top+6*height/8+2,
                                     left+5*width/8, top+7*height/8-2)
        self.canvas.create_text(left+width/2, top+13*height/16,
                                text="Next Turn")
        self.drawResourcesBank()

    def drawResourcesBank(self):
        resources = ["brick", "wood", "sheep", "wheat", "ore"]
        position = self.left + 125
        width = self.length
        height = self.tall
        top = self.top
        self.canvas.create_rectangle(self.left+width/5, top+height,
                                     self.left+4*width/5,
                                     top+19*height/16, fill="black")
        for resource in resources:
            if resource == "brick": color = "maroon"
            elif resource == "wood": color = "green"
            elif resource == "sheep": color = "lightGreen"
            elif resource == "wheat": color = "goldenrod"
            elif resource == "ore": color = "lightGrey"
            self.canvas.create_text(position, top + 17*height/16, text=resource,
                                    anchor=W, fill=color, font="Arial 12")
            position += 50

    def nextTurn(self):
        reverseTurn = copy.deepcopy(self.players)
        reverseTurn.reverse()
        self.turn += 1
        self.text = ""
        if ((self.turn > len(self.players)-1) and
            (self.turn < 2*len(self.players))):
            self.playerTurn = reverseTurn[(self.reverseTurn)%(len(self.players))]
            self.text = "Place a settlement, and then a road"
            self.buildRoad = True
            self.buildSettlement = True
            self.reverseTurn += 1
        else:
            self.playerTurn = self.players[(self.turn)%(len(self.players))]
            if (self.turn >= 2*len(self.players)-1):
                self.rollDice()
            else:
                self.text = "Place a settlement, and then a road"
                self.buildRoad = True
                self.buildSettlement = True
    
    def drawDice(self):
        self.canvas.create_rectangle(self.width/2-20,
                                     self.height/12-40,
                                     self.width/2+20,
                                     self.height/12, fill="red")
        self.canvas.create_text(self.width/2, self.height/12-20,
                                text=str(self.dice1), fill="yellow")
        self.canvas.create_rectangle(9*self.width/16-20,
                                     self.height/12-40,
                                     9*self.width/16+20,
                                     self.height/12, fill="yellow")
        self.canvas.create_text(9*self.width/16, self.height/12-20,
                                text=str(self.dice2), fill="red")

    def drawPlayerTabs(self):
        m = 25
        t = 0
        tL = 75
        w = self.width
        h = self.height
        for player in self.players:
            if (player == self.playerTurn):
                self.canvas.create_rectangle(m+t*tL, 2*h/3+m, m+(t+1)*tL, 2*h/3,
                                             fill=self.playerTurn.color,
                                             outline="black")
                self.canvas.create_rectangle(m, 2*h/3+m, w-m, h-m,
                                             fill=self.playerTurn.color,
                                             outline="black")
            else:
                self.canvas.create_rectangle(m+t*tL, 2*h/3+m, m+(t+1)*tL, 2*h/3,
                                             fill=player.color,
                                             outline="black")
            self.canvas.create_text(m+t*tL+tL/2, 2*h/3+m/2,
                                    text=player.color)
            t += 1
        self.drawPlayerStuff()

    def drawPlayerStuff(self):
        m1 = 25
        m2 = 25
        self.canvas.create_text(m1+m2, 2*self.height/3+40, anchor=W,
                                text="Resources")
        self.canvas.create_text(self.width/2, 2*self.height/3+40, anchor=W,
                                text="Dev Cards")
        self.canvas.create_text(7*self.width/8, 2*self.height/3+40,
                                text="VP: " + str(self.playerTurn.VP))
        self.canvas.create_rectangle(m1+m2, 2*self.height/3+m1+m2,
                                     self.width/2-m2, self.height-m1-m2,
                                     fill="black")
        self.canvas.create_rectangle(self.width/2, 2*self.height/3+m1+m2,
                                     self.width-m1-m2, self.height-m1-m2,
                                     fill="black")
        text='Roads Left: %d,' %(self.playerTurn.roadsLeft)
        text += 'Settlements Left: %d,' % (self.playerTurn.settlementsLeft)
        text+= 'Cities Left: %d' % (self.playerTurn.citiesLeft)
        self.canvas.create_text(m1+m2/2, self.height-m1, anchor=SW, text=text)
        self.drawResources()
        self.drawDevCards()

    def drawResources(self):
        rPosy = 3*self.height/4
        rPosx = 60
        counter = 0
        for resource in self.playerTurn.resourceCards:
            if (resource == 'sheep'): color = "lightGreen"
            elif (resource == 'wood'): color = "green"
            elif (resource == 'ore'): color = "grey"
            elif (resource == 'brick'): color = "maroon"
            elif (resource == 'wheat'): color = "goldenrod"
            self.canvas.create_text(rPosx, rPosy, anchor=W,
                                    text=resource, fill=color)
            if counter == 6:
                counter = 0
                rPosx += 50
                rPosy = 3*self.height/4-20
            else: counter += 1
            rPosy += 20

    def drawDevCards(self):
        self.devCard = 0
        dcPy = 3*self.height/4
        dcPx = self.width/2+5
        counter = 0
        for devCard in self.playerTurn.devCards:
            if (devCard == 'knight'): color = "maroon"
            elif (devCard == 'monopoly'): color = "green"
            elif (devCard == 'yearOfPlenty'): color = "green"
            elif (devCard == 'roadBuilding'): color = "green"
            elif (devCard == 'VP'): color = "blue"
            self.canvas.create_text(dcPx, dcPy, anchor=W,
                                    text=devCard, fill=color)
            if counter == 6:
                counter = 0
                dcPx += 50
                dcPy = 3*self.height/4-20
            else: counter += 1
            dcPy += 20

    def displayScreen(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="red")
        self.canvas.create_image(self.width/2, self.height/2-50,
                                 image=self.start)
        self.canvas.create_rectangle(3*self.width/8, 19*self.height/22,
                                     5*self.width/8, 21*self.height/22,
                                     outline="yellow")
        self.canvas.create_text(self.width/2, 10*self.height/11,
                                text="Start", fill="yellow")
       
    def drawHelpScreen(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="red")
        self.canvas.create_image(self.width/2, self.height/2-50,
                                 image=self.help1)
        self.canvas.create_rectangle(3*self.width/8, 19*self.height/22,
                                     5*self.width/8, 21*self.height/22,
                                     outline="yellow")
        self.canvas.create_text(self.width/2, 10*self.height/11,
                                text="Next", fill="yellow")

    def drawPlayerSelection(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="red")
        self.canvas.create_text(self.width/2, self.height/3,
                                text="Select number of players and the colors",
                                fill="yellow", font="Arial 20 bold")

        self.canvas.create_text(self.width/8, 7*self.height/16, text="Player 1")
        self.canvas.create_text(3*self.width/8, 7*self.height/16,
                                text="Player 2")
        self.canvas.create_text(5*self.width/8, 7*self.height/16,
                                text="Player 3")
        self.canvas.create_text(7*self.width/8, 7*self.height/16,
                                text="Player 4")

        if (len(self.players) == 0):
            self.drawSelectPlayer1()

        elif (len(self.players) == 1):
            self.drawSelection()
            self.drawSelectPlayer2()

        elif (len(self.players) == 2):
            self.drawSelection()
            self.drawSelectPlayer3()
            
        elif (len(self.players) == 3):
            self.drawSelection()
            self.drawSelectPlayer4()

        elif (len(self.players) == 4):
            self.drawSelection()
        
        if (len(self.players) >= 2):
            self.canvas.create_rectangle(3*self.width/8, 19*self.height/22,
                                         5*self.width/8, 21*self.height/22,
                                         outline="yellow")
            self.canvas.create_text(self.width/2, 10*self.height/11,
                                    text="Next", fill="yellow")

    def drawSelection(self):
        width = self.width/16
        textWidth = self.width/8
        for player in xrange(len(self.players)):
            self.canvas.create_rectangle(width, 11*self.height/22,
                                         width+self.width/8, 13*self.height/22,
                                         fill=self.players[player].color,
                                         outline="green", width=5)
            if self.players[player].color == "white": color = "black"
            else: color = "white"
            self.canvas.create_text(textWidth, 6*self.height/11,
                                    text=self.players[player].color, fill=color)
            width += self.width/4
            textWidth += self.width/4

    def drawSelectPlayer1(self):
        self.canvas.create_rectangle(self.width/16, 11*self.height/22,
                                     3*self.width/16, 13*self.height/22,
                                     fill="blue")
        self.canvas.create_text(self.width/8, 6*self.height/11, text="blue",
                                fill="white")
        self.canvas.create_rectangle(self.width/16, 13*self.height/22,
                                     3*self.width/16, 15*self.height/22,
                                     fill="red")
        self.canvas.create_text(self.width/8, 7*self.height/11, text="red",
                                fill="white")
        self.canvas.create_rectangle(self.width/16, 15*self.height/22,
                                     3*self.width/16, 17*self.height/22,
                                     fill="orange")
        self.canvas.create_text(self.width/8, 8*self.height/11,
                                text="orange", fill="white")
        self.canvas.create_rectangle(self.width/16, 17*self.height/22,
                                     3*self.width/16, 19*self.height/22,
                                     fill="white")
        self.canvas.create_text(self.width/8, 9*self.height/11,
                                text="white")

    def drawSelectPlayer2(self):   
        if "blue" in self.colors:
            self.canvas.create_rectangle(5*self.width/16, 11*self.height/22,
                                         7*self.width/16, 13*self.height/22,
                                         fill="blue")
            self.canvas.create_text(3*self.width/8, 6*self.height/11,
                                    text="blue", fill="white")
        if "red" in self.colors:
            self.canvas.create_rectangle(5*self.width/16, 13*self.height/22,
                                         7*self.width/16, 15*self.height/22,
                                         fill="red")
            self.canvas.create_text(3*self.width/8, 7*self.height/11,
                                    text="red", fill="white")
        if "orange" in self.colors:
            self.canvas.create_rectangle(5*self.width/16, 15*self.height/22,
                                         7*self.width/16, 17*self.height/22,
                                         fill="orange")
            self.canvas.create_text(3*self.width/8, 8*self.height/11,
                                text="orange", fill="white")
        if "white" in self.colors:
            self.canvas.create_rectangle(5*self.width/16, 17*self.height/22,
                                         7*self.width/16, 19*self.height/22,
                                         fill="white")
            self.canvas.create_text(3*self.width/8, 9*self.height/11,
                                    text="white")

    def drawSelectPlayer3(self):
        if "blue" in self.colors:
            self.canvas.create_rectangle(9*self.width/16, 11*self.height/22,
                                         11*self.width/16, 13*self.height/22,
                                         fill="blue")
            self.canvas.create_text(5*self.width/8, 6*self.height/11,
                                    text="blue", fill="white")
        if "red" in self.colors:
            self.canvas.create_rectangle(9*self.width/16, 13*self.height/22,
                                         11*self.width/16, 15*self.height/22,
                                         fill="red")
            self.canvas.create_text(5*self.width/8, 7*self.height/11,
                                    text="red", fill="white")
        if "orange" in self.colors:
            self.canvas.create_rectangle(9*self.width/16, 15*self.height/22,
                                         11*self.width/16, 17*self.height/22,
                                         fill="orange")
            self.canvas.create_text(5*self.width/8, 8*self.height/11,
                                text="orange", fill="white")
        if "white" in self.colors:
            self.canvas.create_rectangle(9*self.width/16, 17*self.height/22,
                                         11*self.width/16, 19*self.height/22,
                                         fill="white")
            self.canvas.create_text(5*self.width/8, 9*self.height/11,
                                    text="white")

    def drawSelectPlayer4(self):
        if "blue" in self.colors:
            self.canvas.create_rectangle(13*self.width/16, 11*self.height/22,
                                         15*self.width/16, 13*self.height/22,
                                         fill="blue")    
            self.canvas.create_text(7*self.width/8, 6*self.height/11,
                                    text="blue", fill="white")
        if "red" in self.colors:
            self.canvas.create_rectangle(13*self.width/16, 13*self.height/22,
                                         15*self.width/16, 15*self.height/22,
                                         fill="red")
            self.canvas.create_text(7*self.width/8, 7*self.height/11,
                                    text="red", fill="white")
        if "orange" in self.colors:
            self.canvas.create_rectangle(13*self.width/16, 15*self.height/22,
                                         15*self.width/16, 17*self.height/22,
                                         fill="orange")
            self.canvas.create_text(7*self.width/8, 8*self.height/11,
                                    text="orange", fill="white")
        if "white" in self.colors:
            self.canvas.create_rectangle(13*self.width/16, 17*self.height/22,
                                         15*self.width/16, 19*self.height/22,
                                         fill="white")
            self.canvas.create_text(7*self.width/8, 9*self.height/11,
                                    text="white")

    def playerSelection(self, x, y):
        if (len(self.players) == 0):
            self.addPlayer1(x, y)                    
        elif (len(self.players) == 1):
            self.addPlayer2(x, y)
        elif (len(self.players) == 2):
            if ((x > 3*self.width/8) and (x < 5*self.width/8) and
                (y > 19*self.height/22) and (21*self.height/22)):
                self.startCatan()
            else: self.addPlayer3(x, y)
        elif (len(self.players) == 3):
            if ((x > 3*self.width/8) and (x < 5*self.width/8) and
                (y > 19*self.height/22) and (21*self.height/22)):
                self.startCatan()
            else: self.addPlayer4(x, y)
        elif (len(self.players) == 4):
            if ((x > 3*self.width/8) and (x < 5*self.width/8) and
                (y > 19*self.height/22) and (21*self.height/22)):
                self.startCatan()

    def addPlayer1(self, x, y):
        if ((x > self.width/16) and (x < 3*self.width/16) and
            (y > 11*self.height/22) and (y < 13*self.height/22)):
            self.player1 = Player(self.colors.pop(self.colors.index("blue")))
        elif ((x > self.width/16) and (x < 3*self.width/16) and
              (y > 13*self.height/22) and (y < 15*self.height/22)):
            self.player1 = Player(self.colors.pop(self.colors.index("red")))
        elif ((x > self.width/16) and (x < 3*self.width/16) and
              (y > 15*self.height/22) and (y < 17*self.height/22)):
            self.player1 = Player(self.colors.pop(self.colors.index("orange")))
        elif ((x > self.width/16) and (x < 3*self.width/16) and
              (y > 17*self.height/22) and (y < 19*self.height/22)):
            self.player1 = Player(self.colors.pop(self.colors.index("white")))
        self.players += [self.player1]

    def addPlayer2(self, x, y):
        if ((x > 5*self.width/16) and (x < 7*self.width/16) and
            (y > 11*self.height/22) and (y < 13*self.height/22) and
            ("blue" in self.colors)):
            self.player2 = Player(self.colors.pop(self.colors.index("blue")))
        elif ((x > 5*self.width/16) and (x < 7*self.width/16) and
              (y > 13*self.height/22) and (y < 15*self.height/22) and
              ("red" in self.colors)):
            self.player2 = Player(self.colors.pop(self.colors.index("red")))
        elif ((x > 5*self.width/16) and (x < 7*self.width/16) and
              (y > 15*self.height/22) and (y < 17*self.height/22) and
              ("orange" in self.colors)):
            self.player2 = Player(self.colors.pop(self.colors.index("orange")))
        elif ((x > 5*self.width/16) and (x < 7*self.width/16) and
              (y > 17*self.height/22) and (y < 19*self.height/22) and
              ("white" in self.colors)):
            self.player2 = Player(self.colors.pop(self.colors.index("white")))
        self.players += [self.player2]

    def addPlayer3(self, x, y):
        if ((x > 9*self.width/16) and (x < 11*self.width/16) and
            (y > 11*self.height/22) and (y < 13*self.height/22) and
            ("blue" in self.colors)):
            self.player3 = Player(self.colors.pop(self.colors.index("blue")))
        elif ((x > 9*self.width/16) and (x < 11*self.width/16) and
              (y > 13*self.height/22) and (y < 15*self.height/22) and
              ("red" in self.colors)):
            self.player3 = Player(self.colors.pop(self.colors.index("red")))
        elif ((x > 9*self.width/16) and (x < 11*self.width/16) and
              (y > 15*self.height/22) and (y < 17*self.height/22) and
              ("orange" in self.colors)):
            self.player3 = Player(self.colors.pop(self.colors.index("orange")))
        elif ((x > 9*self.width/16) and (x < 11*self.width/16) and
              (y > 17*self.height/22) and (y < 19*self.height/22) and
              ("white" in self.colors)):
            self.player3 = Player(self.colors.pop(self.colors.index("white")))
        self.players += [self.player3]
                
    def addPlayer4(self, x, y):
        if ((x > 13*self.width/16) and (x < 15*self.width/16) and
            (y > 11*self.height/22) and (y < 13*self.height/22) and
            ("blue" in self.colors)):
            self.player4 = Player(self.colors.pop(self.colors.index("blue")))
        elif ((x > 13*self.width/16) and (x < 15*self.width/16) and
              (y > 13*self.height/22) and (y < 15*self.height/22) and
              ("red" in self.colors)):
            self.player4 = Player(self.colors.pop(self.colors.index("red")))
        elif ((x > 13*self.width/16) and (x < 15*self.width/16) and
              (y > 15*self.height/22) and (y < 17*self.height/22) and
              ("orange" in self.colors)):
            self.player4 = Player(self.colors.pop(self.colors.index("orange")))
        elif ((x > 13*self.width/16) and (x < 15*self.width/16) and
              (y > 17*self.height/22) and (y < 19*self.height/22) and
              ("white" in self.colors)):
            self.player4 = Player(self.colors.pop(self.colors.index("white")))
        self.players += [self.player4]
    

    def startCatan(self):
        self.displayPlayerSelection = False
        self.reverseTurn = 0
        self.gameInPlay = True
        self.playerTurn = self.players[0]
        self.buildSettlement = True
        self.buildRoad = True
        self.text="Place a settlement, then a road"
        
    def drawGameOver(self, player):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="red")
        self.canvas.create_text(self.width/2, self.height/2, text="Game Over!",
                                fill="yellow", font="Arial 36 bold")
        self.canvas.create_text(self.width/2, self.height/4,
                                text=player.color + " is the winner!",
                                fill="yellow")
        self.canvas.create_text(self.width/2, 3*self.height/4,
                                text="Press 'r' to play again!", fill="yellow")

    def run(self):
        # create the root and the canvas
        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.initAnimation()
        # set up events
        # DK: You can use a local function with a closure
        # to store the canvas binding, like this:
        def f(event): self.onMousePressedWrapper(event)    
        self.root.bind("<Button-1>", f)
        # DK: Or you can just use an anonymous lamdba function, like this:
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()
        # and launch the app (This call BLOCKS, so your program waits
        # until you close the window!)
        self.root.mainloop()

catan = SettlersOfCatan()
catan.run()
