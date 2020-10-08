import pygame
import time
import random
import os

class SpeedRacer:

    def main(self):

        pygame.init()
        pygame.mixer.init()

        self.gameWindow = pygame.display.set_mode((1000,700))
        pygame.display.set_caption("Speed Racer")

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.font1 = pygame.font.SysFont("Franklin Gothic Demi Cond",50)

        self.car = pygame.image.load("data/images/Car.png")
        self.car = pygame.transform.scale(self.car,(150,150)).convert_alpha()

        self.road = pygame.image.load("data/images/Road.png")
        self.road = pygame.transform.scale(self.road,(400,700)).convert_alpha()

        self.sand = pygame.image.load("data/images/Sand.jpg")
        self.sand = pygame.transform.scale(self.sand,(150,700)).convert_alpha()

        self.leftDisp = pygame.image.load("data/images/LeftDisplay.png")
        self.leftDisp = pygame.transform.scale(self.leftDisp,(250,700)).convert_alpha()

        self.rightDisp = pygame.image.load("data/images/RightDisplay.png")
        self.rightDisp = pygame.transform.scale(self.rightDisp,(250,700)).convert_alpha()

        self.tree = pygame.image.load("data/images/Tree.png")
        self.tree = pygame.transform.scale(self.tree,(185,168)).convert_alpha()
        self.treeLXY = [[290,0],[290,152.5],[290,305],[290,457.5],[290,610]]
        self.treeRXY = [[760,0],[760,152.5],[760,305],[760,457.5],[760,610]]

        self.strip = pygame.image.load("data/images/Strip.png")
        self.strip = pygame.transform.scale(self.strip,(25,90)).convert_alpha()
        self.stripXY = [[593,0],[593,152.5],[593,305],[593,457.5],[593,610]]

        self.explosion = pygame.image.load("data/images/Explosion.png")
        self.explosion = pygame.transform.scale(self.explosion,(290,164)).convert_alpha()

        self.fuel = pygame.image.load("data/images/Fuel.png")
        self.fuel = pygame.transform.scale(self.fuel,(98,104)).convert_alpha()

        self.comingCars,self.goingCars = [],[]
        self.speedCC = [8,10,10,10,10,10,10,10,10]
        self.speedGC = [8,6,7,5,8,7,8,6,8]

        for i in range(1,10):
            self.CCi = pygame.image.load("data/images/Coming Cars/"+"CC"+str(i)+".png")
            self.CCi = pygame.transform.scale(self.CCi, (75, 158)).convert_alpha()
            self.comingCars.append([self.CCi,self.speedCC[i-3]])
            self.GCi = pygame.image.load("data/images/Going Cars/"+"GC"+str(i)+".png").convert_alpha()
            self.GCi = pygame.transform.scale(self.GCi,(75,158)).convert_alpha()
            self.goingCars.append([self.GCi,self.speedGC[i-1]])
        self.homeScreen()


    def distance(self,carX,obstX,carY,obstY,isFuel = False):

        if not isFuel:
            carX += 75 # 75,75,37,79,55,130
            carY += 75
            obstX += 37
            obstY += 79

            return abs(carX - obstX) < 55 and abs(carY - obstY) < 130
        else:
            carX += 75
            carY += 75
            obstX += 98
            obstY += 104

            return abs(carX - obstX) < 70 and abs(carY - obstY) < 80

    def textOnScreen(self, text,color,x,y,font):
        screenText = font.render(text,True,color)
        self.gameWindow.blit(screenText,[x,y])

    def slowDown(self, carX,carY,dist,highscore):

        self.stripXY_ = [[593, 0], [593, 152.5], [593, 305], [593, 457.5], [593, 610]]
        exitScreen = False

        self.stripSpeed = 2

        start = time.time()
        while not exitScreen:
            if time.time() - start > 3:
                self.stripSpeed = 1
            if time.time() - start > 6:
                exitScreen = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitScreen = True

            self.gameWindow.fill((0,0,0))
            self.gameWindow.blit(self.leftDisp, (0, 0))
            self.textOnScreen("DISTANCE", (255, 255, 0), 27, 388, self.font1)
            self.textOnScreen(str(dist) + " Kms", (255, 0, 0), 56, 480, self.font1)
            self.textOnScreen("FUEL", (255, 255, 0), 73, 90, self.font1)
            self.textOnScreen(str(0.00) + ' %', (255, 0, 0), 75, 184, self.font1)
            self.gameWindow.blit(self.rightDisp, (950, 0))
            self.textOnScreen("HIGHSCORE", (255, 255, 0), 958, 236, self.font1)
            if(highscore < 10):
                disp = str(0) + str(highscore)
            else:
                disp = str(highscore)
            self.textOnScreen(disp + " Kms", (255, 0, 0), 1005, 342, self.font1)
            self.gameWindow.blit(self.road, (400, 0))
            self.gameWindow.blit(self.sand,(250,0))
            self.gameWindow.blit(self.sand,(800,0))

            for i in range(len(self.stripXY_)):
                self.stripXY_[i][1] += self.stripSpeed
                if self.stripXY_[i][1] > 700:
                    self.stripXY_[i] = [593, -60]
            for i in range(len(self.treeLXY)):
                self.treeLXY[i][1] += self.stripSpeed
                if self.treeLXY[i][1] > 700:
                    self.treeLXY[i] = [290,-60]
            for i in range(len(self.treeRXY)):
                self.treeRXY[i][1] += self.stripSpeed
                if self.treeRXY[i][1] > 700:
                    self.treeRXY[i] = [760,-60]

            for X,Y in self.stripXY_:
                self.gameWindow.blit(self.strip,(X,Y))
            for self.treeX,self.treeY in self.treeLXY:
                self.gameWindow.blit(self.tree,(self.treeX,self.treeY))
            for self.treeX,self.treeY in self.treeRXY:
                self.gameWindow.blit(self.tree,(self.treeX,self.treeY))

            self.gameWindow.blit(self.car,(carX,carY))
            pygame.display.update()


    def gameLoop(self):


        time.sleep(1)

        carX,carY = 625,540
        drift = 1
        self.carSpeedX = 0

        obstacleXY = [[460,-10],[710,-300]]
        c1,c2 = random.randint(0,8),random.randint(0,8)
        if(c1 == c2):
            c1 = random.randint(0,8)

        obstacleSpeed = [self.comingCars[c1][1],self.goingCars[c2][1]]
        obstacles = [self.comingCars[c1][0],self.goingCars[c2][0]]

        self.stripSpeed = 5

        exitGame = False
        gameOver = False
        explode = False

        self.fuelCount = 50
        fuelX,fuelY = random.randint(420,620),-1000
        self.fuelSpeed = 8
        dist = 0

        with open("data/Highscore.txt","r") as f:
            highscore = int(f.read())

        slow = False
        plotFuel = True

        start1 = time.time()
        start = [start1,start1]
        start2 = start1
        start3 = start1
        start4 = start1
        arrival = [2,3.5]

        while not exitGame:
            if gameOver:

                if slow:
                    self.slowDown(carX,carY,dist,highscore)
                time.sleep(2)

                # pygame.mixer.music.stop()
                # pygame.mixer.music.load("data/audios/rtn.mp3")
                # pygame.mixer.music.play()

                exitScreen = False
                go = pygame.image.load("data/images/GameOver.png")
                go = pygame.transform.scale(go,(1239,752)).convert_alpha()

                with open("data/Highscore.txt","w") as f:
                    f.write(str(highscore))

                while not exitScreen:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exitScreen = True
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                # pygame.mixer.music.stop()
                                self.homeScreen()
                    self.gameWindow.fill((0,0,0))
                    self.gameWindow.blit(go,(0,0))
                    if(dist < 10):
                        disp = str(0) + str(dist)
                    else:
                        disp = str(dist)
                    self.textOnScreen(disp,(255,0,0),540,429,self.font1)
                    pygame.display.update()
                    self.clock.tick(self.fps)

                pygame.quit()
                quit()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exitGame = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.carSpeedX = drift
                        elif event.key == pygame.K_LEFT:
                            self.carSpeedX = -drift
                        elif event.key == pygame.K_a:
                            obstacleXY[0][0] -= 20
                        elif event.key == pygame.K_d:
                            obstacleXY[1][0] += 20

                carX += self.carSpeedX
                fuelY += self.fuelSpeed

                if time.time() - start4 >= 2:
                    dist += 1
                    if dist > highscore:
                        highscore = dist
                    start4 = time.time()

                if time.time() - start2 >= 3:
                    self.fuelCount -= 5
                    start2 = time.time()

                if self.distance(carX,fuelX,carY,fuelY,True) and plotFuel:
                    plotFuel = False
                    self.fuelCount += 20

                for i in range(len(obstacleXY)):
                    obstacleXY[i][1] += obstacleSpeed[i]

                self.fuelper = self.fuelCount/50
                if self.fuelper >= 1:
                    self.fuelper = 1

                self.gameWindow.fill((0,0,0))
                self.gameWindow.blit(self.leftDisp,(0,0))
                self.textOnScreen("DISTANCE", (255, 255, 0),27,388,self.font1)
                if(dist < 10):
                    disp = str(0) + str(dist)
                else:
                    disp = str(dist)
                self.textOnScreen(disp + " Kms",(255,0,0),56,480,self.font1)
                self.textOnScreen("FUEL",(255,255,0),73,90,self.font1)
                self.textOnScreen(str(self.fuelper*100) + ' %',(255,0,0),60,184,self.font1)
                self.gameWindow.blit(self.rightDisp, (950, 0))
                self.textOnScreen("HIGHSCORE",(255,255,0),958,236,self.font1)
                if(highscore < 10):
                    disp = str(0) + str(highscore)
                else:
                    disp = str(highscore)            
                self.textOnScreen(disp + " Kms",(255,0,0),1005,342,self.font1)
                self.gameWindow.blit(self.road,(400,0))
                self.gameWindow.blit(self.sand, (250, 0))
                self.gameWindow.blit(self.sand, (800, 0))

                if self.fuelCount == 0:
                    gameOver = True
                    slow = True

                if carX > 720 or carX < 330:
                    gameOver = True
                    explode = True

                for i in range(len(obstacleXY)):
                    if self.distance(carX,obstacleXY[i][0],carY,obstacleXY[i][1]):
                        gameOver = True
                        explode = True
                        break
                for i in range(len(self.stripXY)):
                    self.stripXY[i][1] += self.stripSpeed
                    if self.stripXY[i][1] > 700:
                        self.stripXY[i] = [593,-60]
                for i in range(len(self.treeLXY)):
                    self.treeLXY[i][1] += self.stripSpeed
                    if self.treeLXY[i][1] > 700:
                        self.treeLXY[i] = [290, -60]
                for i in range(len(self.treeRXY)):
                    self.treeRXY[i][1] += self.stripSpeed
                    if self.treeRXY[i][1] > 700:
                        self.treeRXY[i] = [760, -60]

                for self.stripX,self.stripY in self.stripXY:
                    self.gameWindow.blit(self.strip,(self.stripX,self.stripY))

                if fuelY < 750:
                    if plotFuel:
                        self.gameWindow.blit(self.fuel,(fuelX,fuelY))

                self.gameWindow.blit(self.car,(carX,carY))

                for i in range(len(obstacleXY)):
                    if obstacleXY[i][1] < 750:
                        self.gameWindow.blit(obstacles[i],(obstacleXY[i][0], obstacleXY[i][1]))

                for self.treeX, self.treeY in self.treeLXY:
                    self.gameWindow.blit(self.tree, (self.treeX, self.treeY))
                for self.treeX, self.treeY in self.treeRXY:
                    self.gameWindow.blit(self.tree, (self.treeX, self.treeY))

                if time.time() - start[0] >= arrival[0]:
                    x = random.randint(430,530)
                    x+=3
                    obstacleXY[0] = [x,-10]
                    c1 = random.randint(0,8)
                    obstacles[0] = self.comingCars[c1][0]
                    obstacleSpeed[0] = self.comingCars[c1][1]
                    start[0] = time.time()
                if time.time() - start[1] >= arrival[1]:
                    x = random.randint(620,710)
                    x-=3
                    obstacleXY[1] = [x,-10]
                    c2 = random.randint(0,8)
                    obstacles[1] = self.goingCars[c2][0]
                    obstacleSpeed[1] = self.goingCars[c2][1]
                    start[1] = time.time()
                if time.time() - start3 >= 15:
                    fuelX, fuelY = random.randint(420,710),-500
                    plotFuel = True
                    start3 = time.time()
                if explode:
                    self.gameWindow.blit(self.explosion,(carX - 63,carY))

                pygame.display.update()
                self.clock.tick(self.fps)


        pygame.quit()
        quit()



    def homeScreen(self):

        if not os.path.exists("data/Highscore.txt"):
            with open("data/Highscore.txt","w") as f:
                f.write("0")
                highscore = 0
        else:
            with open("data/Highscore.txt","r") as f:
                highscore = int(f.read())


        background = pygame.image.load("data/images/Background.png")
        background = pygame.transform.scale(background,(1213,760)).convert_alpha()

        exitScreen = False
        while not exitScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitScreen = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        self.gameLoop()

            self.gameWindow.blit(background,(-6,-32))
            if(highscore < 10):
                disp = str(0) + str(highscore)
            else:
                disp = str(highscore)
            self.textOnScreen(disp,(255,0,0),980,9,self.font1)
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()
        quit()

if __name__ == '__main__':
    game = SpeedRacer()
    game.main()