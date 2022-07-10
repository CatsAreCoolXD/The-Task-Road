# The Task Road
#
# Voor de metis Game Jam, 2022
# Datum: 8-7-2022
# Gemaakt in 7 uur, daarna had ik meer toegevoegd

project_info = {
    "version": "v0.131"
}

import random
import pygame
import string as s
import math

pygame.init()
pygame.font.init()
pygame.mixer.init()

keyToPygame = {
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,
}

objectivesList = [
    "Collect 3 scrap",
    "Jump 10 times",
    "Click on amogus",
    "Press K",
    "Click on the time",
    "Play the click sound",
    "Touch the border of the window",
    "Complete all other task(s) and wait 5 seconds",
    "Click 20 times",
]

r = True

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption(f"The Task Road {project_info['version']}")
car = pygame.image.load("car.png").convert()
car = pygame.transform.scale(car, (car.get_width() * 2, car.get_height() * 2))
player2 = pygame.image.load("player.png").convert()
explosion = pygame.image.load("explosion.png").convert()
explosion = pygame.transform.scale(explosion, (explosion.get_width()*1.25, explosion.get_height()*1.25))
bed = pygame.image.load("bed.png").convert()
bed = pygame.transform.scale(bed, (1280, 720))
playerTRight = pygame.image.load("playerTransparentRight.png").convert_alpha()
playerTLeft = pygame.image.load("playerTransparentLeft.png").convert_alpha()
playerInBed = pygame.transform.rotate(playerTRight, 57)
grass = pygame.image.load("grass.png").convert()
dirt = pygame.image.load("dirt.png").convert()
scrap = pygame.image.load("scrap.png").convert_alpha()
scrap = pygame.transform.scale(scrap, (scrap.get_width()/15, scrap.get_height()/15))
amogus = pygame.image.load("amogus.png").convert_alpha()
amogus = pygame.transform.scale(amogus, (amogus.get_width()/10, amogus.get_height()/10))
playerLeft = pygame.image.load("playerLeft.png").convert()
playerDead = pygame.image.load("playerDead.png").convert()
carT = pygame.image.load("carTransparent.png").convert_alpha()
carT = pygame.transform.scale(carT, (carT.get_width() * 2, carT.get_height() * 2))
explosionS = pygame.mixer.Sound("explosion.wav")
jumpS = pygame.mixer.Sound("jump.wav")
susS = pygame.mixer.Sound("sus.wav")
clickS = pygame.mixer.Sound("click.wav")
cheerS = pygame.mixer.Sound("kids_cheering.wav")
gameOverS = pygame.mixer.Sound("game_over.wav")

carAddX = 0
waitTime = 0
secondTime = 31
moveCar = False
stopCar = False
startCutscene = True
oneFrame = True
renderExplosion = True
wakeUp = False
endCutscene = False
game = False
clickedOnAmogus = False
end = False
endDead = False
hitPlayer = False
clickOnTime = False
playGOSound = True
playWSound = True
playedCSound = False
canNewFast = True
clicked = False
waitSeconds = 0
endPlayerAddX = 0
secondWait = 0
waitAgain = 0
pressTimer = 2
reasonOfDeath = ""
soMuchWait = 0
eachSecond = 0
seconds = 0
clickTotal = 0

# Elke seconde increasen die wait dingen bij 500

# Gamerules
doTesting = True
doRandomKeyPresses = False
includeObjective = ""
amountObjective = 0
disableSound = True

if includeObjective not in objectivesList and includeObjective != "":
    raise ValueError("Objective not in list of objectives. See variable objectivesList to see all objectives")

if doTesting:
    game = True
    startCutscene = False

if disableSound:
    cheerS.set_volume(0)
    jumpS.set_volume(0)
    explosionS.set_volume(0)
    gameOverS.set_volume(0)
    susS.set_volume(0)
    clickS.set_volume(0)

font = pygame.font.SysFont("Arial", 30, False)
qFont = pygame.font.SysFont("Arial", 55, False)

activeObjectives = []
objectivesOrder = {}
progressObjectives = ["", "", "", ""]
if includeObjective == "":
    xi = -1
    totalDoTasks = 4
else:
    xi = 0
    totalDoTasks = 3

if includeObjective != "":
    activeObjectives.append(includeObjective)
    objectivesOrder[includeObjective] = 0
    progressObjectives[0] = "0/" + str(amountObjective)

for xii in range(totalDoTasks):
    appendObjective = random.choice(objectivesList)
    if appendObjective not in activeObjectives:
        xi += 1
        activeObjectives.append(appendObjective)
        objectivesOrder[appendObjective] = xi
        x = objectivesOrder[appendObjective]
        if appendObjective == "Collect 3 scrap":
            progressObjectives[x] = "0/3"
        elif appendObjective == "Jump 10 times":
            progressObjectives[x] = "0/10"
        elif appendObjective == "Click on amogus":
            progressObjectives[x] = "0/1"
        elif appendObjective == "Press K":
            progressObjectives[x] = "0/1"
        elif appendObjective == "Click on the time":
            progressObjectives[x] = "0/1"
        elif appendObjective == "Play the click sound":
            progressObjectives[x] = "0/1"
        elif appendObjective == "Touch the border of the window":
            progressObjectives[x] = "0/1"
        elif appendObjective == "Complete all other task(s) and wait 5 seconds":
            progressObjectives[x] = "0/5"
        elif appendObjective == "Click 20 times":
            progressObjectives[x] = "0/20"

clock = pygame.time.Clock()
startCutsceneEvent = pygame.USEREVENT
waitTillGame = pygame.USEREVENT
pygame.time.set_timer(startCutsceneEvent, 2500, 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = -1
        self.grounded = True
        self.is_jumping = False
        self.go_down = False
        self.left = 0
        self.right = 1
        self.direction = self.right
        self.playerLeft = playerTLeft
        self.playerRight = playerTRight
        self.jumped = 0
        self.down_thing = True

    def drawPlayer(self, *dead: bool):
        if self.direction == self.right:
            if not dead:
                screen.blit(self.playerRight, (self.x, self.y))
            else:
                screen.blit(self.playerRight, (self.x, self.y - 30))
        else:
            if not dead:
                screen.blit(self.playerLeft, (self.x, self.y))
            else:
                screen.blit(self.playerLeft, (self.x, self.y - 30))
        if self.y >= 720 / 2:
            self.grounded = True

    def movePlayer(self):
        keys = pygame.key.get_pressed()
        if self.is_jumping and not self.go_down:
            self.y -= (self.vel_y / 75) * clock.get_time()
            self.vel_y -= (self.vel_y / 75) * clock.get_time()
            if self.vel_y < 4:
                self.go_down = True
        if self.go_down:
            self.y -= self.gravity * clock.get_time()

        if not self.go_down and self.down_thing and not self.grounded:
            self.jumped += 1
            jumpS.play()
            self.down_thing = False
        if keys[pygame.K_a]:
            if (self.x + 100) - 1 > 0:
                self.x -= 1 * clock.get_time()
            self.direction = self.left
        if keys[pygame.K_d]:
            self.direction = self.right
            if self.x + 100 < 1280:
                self.x += 1 * clock.get_time()
        if keys[pygame.K_SPACE] and self.grounded:
            self.vel_y = 150
            self.is_jumping = True
            self.grounded = False
            self.go_down = False
            self.y -= 1
        if not keys[pygame.K_SPACE] and self.grounded:
            self.vel_y = 0
        if self.grounded:
            self.is_jumping = False
            self.go_down = False
            self.down_thing = True


player = Player(500, 720 / 2)


def renderGrass():
    for x in range(0, 41):
        screen.blit(grass, (x * 32, 600))
        for y in range(7):
            screen.blit(dirt, (x * 32, y * 18 + 618))


objectivesPreset = font.render("", False, (0, 0, 0))
objectivesText = font.render(activeObjectives[0] + ": " + progressObjectives[0], False, (0, 0, 0))
objectivesText2 = objectivesPreset
objectivesText3 = objectivesPreset
objectivesText4 = objectivesPreset
if len(activeObjectives) > 1:
    objectivesText2 = font.render(activeObjectives[1] + ": " + progressObjectives[1], False, (0, 0, 0))
    if len(activeObjectives) > 2:
        objectivesText3 = font.render(activeObjectives[2] + ": " + progressObjectives[2], False, (0, 0, 0))
        if len(activeObjectives) > 3:
            objectivesText4 = font.render(activeObjectives[3] + ": " + progressObjectives[3], False, (0, 0, 0))

scrapPositions = []
for x in range(3):
    scrapPositions.append((random.randint(100, 1180), random.randint(250, 550)))

amogusPos = (random.randint(100, 1180), random.randint(10, 550))


def updateObjectives(*seconds: int):
    global objectivesText, objectivesText2, objectivesText3, objectivesText4, clicked, clickTotal
    for x in range(len(activeObjectives)):
        objectivesOrder[activeObjectives[x]] = x

    if len(activeObjectives) != 0:
        objectivesText = font.render(activeObjectives[0] + ": " + progressObjectives[0], False, (0, 0, 0))
        objectivesText2 = objectivesPreset
        objectivesText3 = objectivesPreset
        objectivesText4 = objectivesPreset
        if len(activeObjectives) > 1:
            objectivesText2 = font.render(activeObjectives[1] + ": " + progressObjectives[1], False, (0, 0, 0))
            if len(activeObjectives) > 2:
                objectivesText3 = font.render(activeObjectives[2] + ": " + progressObjectives[2], False, (0, 0, 0))
                if len(activeObjectives) > 3:
                    objectivesText4 = font.render(activeObjectives[3] + ": " + progressObjectives[3], False, (0, 0, 0))

    if "Collect 3 scrap" in activeObjectives:
        progressObjectives[objectivesOrder["Collect 3 scrap"]] = str(len(scrapPositions) * -1 + 3) + "/3"

    if "Jump 10 times" in activeObjectives:
        progressObjectives[objectivesOrder["Jump 10 times"]] = str(player.jumped) + "/10"

    if "Complete all other task(s) and wait 5 seconds" in activeObjectives:
        # Dit duurde een half uur
        if len(seconds) != 0:
            noTuplePls = str(seconds[0])
        else:
            noTuplePls = "0"
        progressObjectives[objectivesOrder["Complete all other task(s) and wait 5 seconds"]] = noTuplePls + "/5"

    if "Click 20 times" in activeObjectives:
        if clicked:
            clicked = False
            clickTotal += 1
            progressObjectives[objectivesOrder["Click 20 times"]] = str(clickTotal) + "/20"



wonText = font.render("You won!", False, (0, 255, 0))
deadText = font.render("Game Over", False, (255, 0, 0))
reasonDeathText = font.render(f"Reason of death: {reasonOfDeath}", False, (255, 0, 0))
copyrightText = font.render("©Cat Games 2022", False, (0,0,0))

while r:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        elif event.type == startCutsceneEvent:
            moveCar = True
        elif event.type == waitTillGame:
            game = True
            wakeUp = False
        if event.type == pygame.MOUSEBUTTONDOWN and game and "Click on amogus" in activeObjectives:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > amogusPos[0] and mouse[0] < amogusPos[0] + 25.6:
                if mouse[1] > amogusPos[1] and mouse[1] < amogusPos[1] + 25.6:
                    clickedOnAmogus = True
                    susS.play()

        if event.type == pygame.MOUSEBUTTONDOWN and game and "Click on the time" in activeObjectives:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > 10 and mouse[0] < 150:
                if mouse[1] > 0 and mouse[1] < 40:
                    clickOnTime = True

        if event.type == pygame.MOUSEBUTTONDOWN and game:
            clickS.play()
            playedCSound = True
            clicked = True
            updateObjectives()
    if startCutscene:

        if stopCar:
            screen.fill((255, 255, 255))
            wakeUp = True
            startCutscene = False
        else:
            screen.fill((47, 116, 102))
        if not stopCar:
            screen.blit(player2, (1280 / 2, 720 / 2))
            screen.blit(car, (-525 + carAddX, 280))
        if moveCar:
            carAddX += 1 * (clock.get_time() * 1.1)
        if carAddX > 800:
            moveCar = False
            stopCar = True
            explosionS.play()
        if stopCar and renderExplosion:
            pass
        if stopCar and oneFrame:
            oneFrame = False

        renderGrass()

    elif wakeUp:
        screen.blit(bed, (0, 0))
        screen.blit(playerInBed, (450, 250))
        waitTime += (1 * (clock.get_time() / 2))
        if waitTime > 2000:
            game = True
            wakeUp = False

    elif game:
        updateObjectives()
        secondTime -= 0.1 * (clock.get_time() / 100)
        if secondTime < 10:
            secondText = font.render("Time: " + str(secondTime)[0], True, (255, 0, 0))
        else:
            secondText = font.render("Time: " + str(secondTime)[0] + str(secondTime)[1], True, (0, 0, 0))
        screen.fill((0, 50, 255))
        renderGrass()
        player.movePlayer()
        player.drawPlayer()
        screen.blit(secondText, (10, 0))
        screen.blit(objectivesText, (10, 50))
        screen.blit(objectivesText2, (10, 100))
        screen.blit(objectivesText3, (10, 150))
        screen.blit(objectivesText4, (10, 200))

        if "Collect 3 scrap" in activeObjectives:
            for x in range(len(scrapPositions)):
                screen.blit(scrap, scrapPositions[x])

            fastBoi = True
            popped = False
            for y in range(len(scrapPositions)):
                if not popped:
                    if player.x + 256 > scrapPositions[y][0] and player.x < scrapPositions[y][0]:
                        if player.y + 256 > scrapPositions[y][1] and player.y < scrapPositions[y][1]:
                            if fastBoi:
                                scrapPositions.pop(y)
                                updateObjectives()
                                fastBoi = False
                                popped = True

            if len(scrapPositions) == 0 and "Collect 3 scrap" in activeObjectives:
                activeObjectives.pop(objectivesOrder["Collect 3 scrap"])
                updateObjectives()

        if "Press K" in activeObjectives:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k] and "Press K" in activeObjectives:
                activeObjectives.pop(objectivesOrder["Press K"])
                updateObjectives()

        if "Jump 10 times" in activeObjectives:
            if player.jumped == 10:
                activeObjectives.pop(objectivesOrder["Jump 10 times"])
                updateObjectives()

        if "Click on amogus" in activeObjectives:
            mouse = pygame.mouse.get_pos()
            screen.blit(amogus, amogusPos)
            if clickedOnAmogus:
                activeObjectives.pop(objectivesOrder["Click on amogus"])
                updateObjectives()

        if "Click on the time" in activeObjectives:
            if clickOnTime:
                activeObjectives.pop(objectivesOrder["Click on the time"])
                updateObjectives()

        if "Play the click sound" in activeObjectives:
            if playedCSound:
                activeObjectives.pop(objectivesOrder["Play the click sound"])
                updateObjectives()

        if "Touch the border of the window" in activeObjectives:
            if player.x < 10 or player.x > 1150:
                activeObjectives.pop(objectivesOrder["Touch the border of the window"])
                updateObjectives()

        if "Complete all other task(s) and wait 5 seconds" in activeObjectives:
            if len(activeObjectives) == 1:
                soMuchWait += (1 * (clock.get_time() / 2))
                if soMuchWait > 2500:
                    activeObjectives.pop(objectivesOrder["Complete all other task(s) and wait 5 seconds"])
                    updateObjectives()
                for seconds in range(math.floor(soMuchWait / 500)):
                    seconds = math.floor(soMuchWait // 500)
                    updateObjectives(seconds)

        if "Click 20 times" in activeObjectives:
            if clickTotal >= 20:
                activeObjectives.pop(objectivesOrder["Click 20 times"])
                updateObjectives()

        if len(activeObjectives) == 0:
            game = False
            end = True

        if secondTime <= 0:
            game = False
            endDead = True
            carAddX = 0
            reasonOfDeath = "Didnt complete objectives in time."

        if random.randint(0, 2500) == 1 and canNewFast and doRandomKeyPresses:
            canNewFast = False
            rKey = random.choice(s.ascii_lowercase)
            pressText = qFont.render(f"Quick, press '{rKey}'! Remaining time: {pressTimer}", False, (200, 0, 100))
            pressTimer = 2

        if not canNewFast:
            pressTimer -= 0.1 * (clock.get_time() / 100)
            pressText = qFont.render(f"Quick, press '{rKey}'! Remaining time: {str(pressTimer)[0]}", False,
                                     (200, 0, 100))
            screen.blit(pressText, (300, 100))
            keys = pygame.key.get_pressed()
            if keys[keyToPygame[rKey]]:
                canNewFast = True

            if pressTimer < 0:
                carAddX = 0
                game = False
                endDead = True
                reasonOfDeath = f"Didnt press '{rKey}' in time."

    elif end:
        screen.fill((47, 116, 102))
        if waitSeconds > 2000:
            screen.blit(wonText, (500, 720 / 2))
            endPlayerAddX += (1 * (clock.get_time() / 2))
            secondText = font.render("Time is up!", False, (250, 0, 0))
            if playWSound:
                cheerS.play()
                playWSound = False
        screen.blit(playerLeft, (500 - endPlayerAddX, 720 / 2))
        renderGrass()
        waitSeconds += (1 * (clock.get_time() / 2))

    elif endDead:

        reasonDeathText = font.render(f"Reason of death: {reasonOfDeath}", False, (255, 0, 0))
        secondText = font.render("Time is up!", False, (250, 0, 0))
        if not hitPlayer:
            screen.fill((0, 50, 255))
        else:
            screen.fill((255, 255, 255))
            waitAgain += (1 * (clock.get_time() / 2))

        if not hitPlayer:
            renderGrass()
        if waitAgain == 0:
            if "Click on amogus" in activeObjectives:
                mouse = pygame.mouse.get_pos()
                screen.blit(amogus, amogusPos)

            if "Collect 3 scrap" in activeObjectives:
                for x in range(len(scrapPositions)):
                    screen.blit(scrap, scrapPositions[x])

        if not hitPlayer and waitAgain == 0:
            screen.blit(secondText, (10, 0))
            screen.blit(objectivesText, (10, 50))
            screen.blit(objectivesText2, (10, 100))
            screen.blit(objectivesText3, (10, 150))
            screen.blit(objectivesText4, (10, 200))
            player.y = 720 / 2

        if not hitPlayer and waitAgain == 0:
            player.drawPlayer()
        if waitAgain == 0:
            player.playerRight = playerTLeft
        secondWait += (1 * (clock.get_time() / 2))
        if secondWait > 2000 and waitAgain == 0:
            screen.blit(carT, (-525 + carAddX, 280))
            if (-525 + carAddX) < player.x - 400:
                carAddX += 1 * (clock.get_time() * 1.1)
            else:
                hitPlayer = True
                explosionS.play()

        if waitAgain > 1500:
            hitPlayer = False
            player.playerRight = playerDead
            player.playerLeft = playerDead
            screen.blit(deadText, (500, 300))
            player.drawPlayer(True)
            screen.blit(reasonDeathText, (100, 100))
            if playGOSound:
                gameOverS.play()
                playGOSound = False

    copyrightText.set_alpha(50)
    screen.blit(copyrightText, (1065, 0))
    pygame.display.flip()

pygame.quit()
pygame.mixer.quit()
# Dit is mijn beste game ooit