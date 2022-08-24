import pygame
import pygame.camera
import cv2
import numpy as np
from HandTrackingModule import handDetector
from collections import deque
from imutils.video import VideoStream
import math
import random
import time

#add pause and resume function
#create an executable and add to resume/github

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 50)

#create the screen
screen = pygame.display.set_mode((1280, 720))

#webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

pygame.display.set_caption("Fruit Ninja VR")
icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(icon)

#detector
detector = handDetector(detectionCon=0.8, maxHands=1)

#knife
knifeImg = pygame.image.load('assets/knife.png').convert_alpha()
knifeX = 300
knifeY = 300
knifeX_change = 0
knifeImg.set_alpha(255)

#background
imgBackground = pygame.image.load('assets/background.jpg').convert_alpha()
imgBackground = pygame.transform.scale(imgBackground, (1280,720))
imgBackground.set_alpha(225)

imgLogo = pygame.image.load('assets/vrlogo.jpg').convert_alpha()
#imgLogo = pygame.transform.scale(imgLogo, (1280,720))
imgLogo.set_alpha(225)

#trace
pts = deque(maxlen=100)
pts.appendleft((0,0))
pts.appendleft((0,0))
pts.appendleft((0,0))

#fruits
imgBomb = pygame.image.load('assets/bomb.png').convert_alpha()
imgBomb = pygame.transform.scale(imgBomb, (100, 100))
rectBomb = imgBomb.get_rect()
rectBomb.x, rectBomb.y = 500, 500

imgExplosion = pygame.image.load('assets/explosion.png').convert_alpha()
imgExplosion = pygame.transform.scale(imgExplosion, (200, 200))
rectExplosion = imgExplosion.get_rect()
rectExplosion.x, rectExplosion.y = 500, 500

imgWatermelon = pygame.image.load('assets/watermelon.png').convert_alpha()
imgWatermelon = pygame.transform.scale(imgWatermelon, (100, 100))
rectWatermelon = imgWatermelon.get_rect()
rectWatermelon.x, rectWatermelon.y = 500, 500

imgKiwi = pygame.image.load('assets/kiwi.png').convert_alpha()
imgKiwi = pygame.transform.scale(imgKiwi, (100, 100))
rectKiwi = imgKiwi.get_rect()
rectKiwi.x, rectKiwi.y = 500, 500

imgBanana = pygame.image.load('assets/banana.png').convert_alpha()
imgBanana = pygame.transform.scale(imgBanana, (100, 100))
rectBanana = imgBanana.get_rect()
rectBanana.x, rectBanana.y = 500, 500

imgApple = pygame.image.load('assets/apple.png').convert_alpha()
imgApple = pygame.transform.scale(imgApple, (100, 100))
rectApple = imgApple.get_rect()
rectApple.x, rectApple.y = 500, 500

imgCoconut = pygame.image.load('assets/coconut.png').convert_alpha()
imgCoconut = pygame.transform.scale(imgCoconut, (100, 100))
rectCoconut = imgCoconut.get_rect()
rectCoconut.x, rectCoconut.y = 500, 500

imgLemon = pygame.image.load('assets/lemon.png').convert_alpha()
imgLemon = pygame.transform.scale(imgLemon, (100, 100))
rectLemon = imgLemon.get_rect()
rectLemon.x, rectLemon.y = 500, 500

imgWatermelonHalf = pygame.image.load('assets/watermelon-half.png').convert_alpha()
imgWatermelonHalf = pygame.transform.scale(imgWatermelonHalf, (90, 90))
rectWatermelonHalf = imgWatermelonHalf.get_rect()
rectWatermelonHalf.x, rectWatermelonHalf.y = 500, 500

imgKiwiHalf = pygame.image.load('assets/kiwi-half.png').convert_alpha()
imgKiwiHalf = pygame.transform.scale(imgKiwiHalf, (100, 100))
rectKiwiHalf = imgKiwiHalf.get_rect()
rectKiwiHalf.x, rectKiwiHalf.y = 500, 500

imgBananaHalf = pygame.image.load('assets/banana-half.png').convert_alpha()
imgBananaHalf = pygame.transform.scale(imgBananaHalf, (90, 90))
rectBananaHalf = imgBananaHalf.get_rect()
rectBananaHalf.x, rectBananaHalf.y = 500, 500

imgAppleHalf = pygame.image.load('assets/apple-half.png').convert_alpha()
imgAppleHalf = pygame.transform.scale(imgAppleHalf, (100, 100))
rectAppleHalf = imgAppleHalf.get_rect()
rectAppleHalf.x, rectAppleHalf.y = 500, 500

imgCoconutHalf = pygame.image.load('assets/coconut-half.png').convert_alpha()
imgCoconutHalf = pygame.transform.scale(imgCoconutHalf, (100, 100))
rectCoconutHalf = imgCoconutHalf.get_rect()
rectCoconutHalf.x, rectCoconutHalf.y = 500, 500

imgLemonHalf = pygame.image.load('assets/lemon-half.png').convert_alpha()
imgLemonHalf = pygame.transform.scale(imgLemonHalf, (90, 90))
rectLemonHalf = imgLemonHalf.get_rect()
rectLemonHalf.x, rectLemonHalf.y = 500, 500

fruits = ['watermelon', 'apple', 'kiwi', 'coconut', 'lemon', 'banana', 'bomb']

def generate_random_fruits(fruit):
    fruit_path = "assets/" + fruit + ".png"
    imgFruit = pygame.image.load(fruit_path)
    rectFruit = imgFruit.get_rect()
    rectFruit.x = random.randint(100,1060)
    rectFruit.y = 800
    data[fruit] = {
        'img': fruit,
        'rect': rectFruit,
        'x' : rectFruit.x,               
        'y' : rectFruit.y,
        'x-half': 0,
        'rotate' : 0,
        'speed_x': random.randint(-25, 25),    
        'speed_y': random.randint(-40, -30),    
        'throw': False,                       
        't': 0,                               
        'hit': False,
        'fallen': False
    }

    if random.random() >= 0.75:     
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

#start
imgStart = pygame.image.load('assets/start.png').convert_alpha()
x = imgStart.get_width()
x = x - 300
y = imgStart.get_height()
y = y - 300
imgStartHover = pygame.transform.scale(imgStart, (x, y))
rectStart = imgStart.get_rect()
rectStart.x, rectStart.y = 370, 50

imgStartHover = pygame.image.load('assets/start.png').convert_alpha()
x = imgStart.get_width()
x = x + 50
y = imgStart.get_height()
y = y + 50
imgStartHover = pygame.transform.scale(imgStartHover, (x, y))
rectStartHover = imgStartHover.get_rect()
rectStartHover.x, rectStartHover.y = 345, 25

imgPlayAgain = pygame.image.load('assets/playagain.png').convert_alpha()
x = imgPlayAgain.get_width()
y = imgPlayAgain.get_height()
imgPlayAgain = pygame.transform.scale(imgPlayAgain, (x, y))
rectPlayAgain = imgPlayAgain.get_rect()
rectPlayAgain.x, rectPlayAgain.y = 570, 425

imgPlayAgainHover = pygame.image.load('assets/playagain.png').convert_alpha()
x = imgPlayAgainHover.get_width()
x = x + 50
y = imgPlayAgainHover.get_height()
y = y + 50
imgPlayAgainHover = pygame.transform.scale(imgPlayAgainHover, (x, y))
rectPlayAgainHover = imgPlayAgainHover.get_rect()
rectPlayAgainHover.x, rectPlayAgainHover.y = 545, 400

imgPause = pygame.image.load('assets/pause.png').convert_alpha()
x = imgPause.get_width()
y = imgPause.get_height()
imgPause = pygame.transform.scale(imgPause, (x, y))
rectPause = imgPause.get_rect()
rectPause.x, rectPause.y = 600, 50

imgPauseHover = pygame.image.load('assets/pause.png').convert_alpha()
x = imgPauseHover.get_width()
x = x + 30
y = imgPauseHover.get_height()
y = y + 30
imgPauseHover = pygame.transform.scale(imgPauseHover, (x, y))
rectPauseHover = imgPauseHover.get_rect()
rectPauseHover.x, rectPauseHover.y = 585, 35

imgResume = pygame.image.load('assets/resume.png').convert_alpha()
x = imgResume.get_width()
y = imgResume.get_height()
imgResume = pygame.transform.scale(imgResume, (x, y))
rectResume = imgResume.get_rect()
rectResume.x, rectResume.y = 600, 300

imgResumeHover = pygame.image.load('assets/resume.png').convert_alpha()
x = imgResumeHover.get_width()
x = x + 30
y = imgResumeHover.get_height()
y = y + 30
imgResumeHover = pygame.transform.scale(imgResumeHover, (x, y))
rectResumeHover = imgResumeHover.get_rect()
rectResumeHover.x, rectResumeHover.y = 585, 285

imgQuit = pygame.image.load('assets/quit.png').convert_alpha()
x = imgQuit.get_width()
y = imgQuit.get_height()
imgQuit = pygame.transform.scale(imgQuit, (x, y))
rectQuit = imgQuit.get_rect()
rectQuit.x, rectQuit.y = 600, 625

imgQuitHover = pygame.image.load('assets/quit.png').convert_alpha()
x = imgQuitHover.get_width()
x = x + 30
y = imgQuitHover.get_height()
y = y + 30
imgQuitHover = pygame.transform.scale(imgQuitHover, (x, y))
rectQuitHover = imgQuitHover.get_rect()
rectQuitHover.x, rectQuitHover.y = 585, 610

#game over
imgGameOver = pygame.image.load('assets/game-over.png').convert_alpha()
x = imgGameOver.get_width()
#x = x - 100
y = imgGameOver.get_height()
#y = y - 100
imgGameOver = pygame.transform.scale(imgGameOver, (x, y))
rectGameOver = imgGameOver.get_rect()
rectGameOver.x, rectGameOver.y = 420, 100

def knife(x, y, pts, frame):
    screen.blit(frame, (0,0))
    if not x == 0 or not y == 0:
        screen.blit(knifeImg, (x, y))
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(20 / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

#globals
speed = 15
startGameFlag = 0
score = 0
startTime = time.time()
totalTime = 60
gameOverFlag = 0
bombFlag = 0
pausedTime = 0

def resetWatermelon():
    rectWatermelon.x = random.randint(100, img.shape[1]-100)
    rectWatermelon.y = img.shape[0]+50

def throwFruit(key, value, pflag):
    global score
    global gameOverFlag
    global bombFlag
    if value['throw']:
        if pflag == 0:
            if value['x'] > 1200 or value['x'] < 10:
                if not value['hit']:
                    value['speed_x'] = -value['speed_x']
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            if value['hit']:
                value['x-half'] -= value['speed_x']
        currRect = pygame.Rect(value['rect'])
        currRect.x = value['x']
        currRect.y = value['y']
        value['rect'] = currRect
        if pflag == 0:
            value['speed_y'] += (1 * value['t'])
            value['t'] += 0.1
            value['rotate'] += value['speed_x']
        if value['img'] == 'watermelon':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgWatermelon, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgWatermelonHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgWatermelonHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']
        elif value['img'] == 'apple':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgApple, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgAppleHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgAppleHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']
        elif value['img'] == 'banana':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgBanana, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgBananaHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgBananaHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']
        elif value['img'] == 'coconut':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgCoconut, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgCoconutHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgCoconutHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']
        elif value['img'] == 'kiwi':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgKiwi, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgKiwiHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgKiwiHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']
        elif value['img'] == 'bomb':
            if not value['hit']:
                currImage = pygame.transform.rotate(imgBomb, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
        else:
            if not value['hit']:
                currImage = pygame.transform.rotate(imgLemon, 0.5*value['rotate'])
                currRect = currImage.get_rect(center=currRect.center)
            else:
                currImage1 = pygame.transform.rotate(imgLemonHalf, 0.5*value['rotate'])
                degrees = (0.5*value['rotate'])+180
                currImage2 = pygame.transform.rotate(imgLemonHalf, degrees)
                currRect1 = currImage1.get_rect(center=currRect.center)
                currRect2 = currImage2.get_rect(center=currRect.center)
                currRect2.x = value['x-half']

        if value['y'] <= 800:
            if not value['hit']:
                screen.blit(currImage, currRect)
            else:
                screen.blit(currImage1, currRect1)
                screen.blit(currImage2, currRect2)
        else:
            if not key =='bomb' or timeRemaining == 50 or timeRemaining == 40 or timeRemaining == 30 or timeRemaining == 20 or timeRemaining == 10:
                generate_random_fruits(key)
        
        #gameplay
        if pflag == 0:
            if not value['hit'] and currRect.collidepoint(knifeX, knifeY):
                if value['img'] == 'bomb':
                    currImage = pygame.transform.rotate(imgExplosion, 0.5*value['rotate'])
                    currRect = currImage.get_rect(center=currRect.center)
                    screen.blit(currImage, currRect)
                    pygame.display.update()
                    time.sleep(0.5)
                    gameOverFlag = 1
                    score -= 1
                value['hit'] = True
                value['x-half'] = value['x']
                if value['speed_x'] >= 0:
                    value['speed_x'] += 5
                else:
                    value['speed_x'] -= 5
                score += 1

    else:
        generate_random_fruits(key)

#Game loop
running = True
while running:
    if startGameFlag == 0:
        success, img = cap.read()
        img, pointerX, pointerY, thumbX, thumbY = detector.findHands(img)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(frame, (0,0))
        screen.blit(imgBackground, (0,0))
        #screen.blit(imgLogo, (530, 50))

        if rectStart.collidepoint(pointerX, pointerY):
            screen.blit(imgStartHover, rectStartHover)
            if math.dist((pointerX, pointerY), (thumbX, thumbY)) < 50:
                startGameFlag = 1
                startTime = time.time()
        else:
            screen.blit(imgStart, rectStart)

        pinchText = font.render(f'Pinch button to start!', True, (0, 255, 0))
        screen.blit(pinchText, (375,500))

        pygame.display.update()
    else:
        #screen.fill((0,0,0))
        timeRemaining = int(totalTime - (time.time()-startTime) + pausedTime)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if timeRemaining < 0 or gameOverFlag == 1:
            success, img = cap.read()
            img, pointerX, pointerY, thumbX, thumbY = detector.findHands(img)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            
            screen.blit(frame, (0,0))
            screen.blit(imgBackground, (0,0))
            screen.blit(imgGameOver, rectGameOver)

            if rectPlayAgain.collidepoint(pointerX, pointerY):
                screen.blit(imgPlayAgainHover, rectPlayAgainHover)
                if math.dist((pointerX, pointerY), (thumbX, thumbY)) < 50:
                    startGameFlag = 1
                    score = 0
                    startTime = time.time()
                    totalTime = 60
                    gameOverFlag = 0
                    bombFlag = 0
                    pausedTime = 0
                    data = {}
                    for fruit in fruits:
                        generate_random_fruits(fruit)
            else:
                screen.blit(imgPlayAgain, rectPlayAgain)

            screen.blit(imgQuit, rectQuit)
            if rectQuit.collidepoint(pointerX, pointerY):
                screen.blit(imgQuitHover, rectQuitHover)
                if math.dist((pointerX, pointerY), (thumbX, thumbY)) < 50:
                    startGameFlag = 0
                    score = 0
                    startTime = time.time()
                    totalTime = 60
                    gameOverFlag = 0
                    bombFlag = 0
                    pausedTime = 0
                    data = {}
                    for fruit in fruits:
                        generate_random_fruits(fruit)
                    pauseFlag = 0
            else:
                screen.blit(imgQuit, rectQuit)

            textScore = font.render(f'Score:{score}', True, (0, 255, 0))
            screen.blit(textScore, (550,275))
        else:
            success, img = cap.read()
            img, knifeX, knifeY, thumbX, thumbY = detector.findHands(img)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()

            #rectWatermelon.y -= speed  

            #if rectWatermelon.y < 0:
            #    resetWatermelon() 
                
            pts.appendleft((knifeX-30, knifeY+30))
            #knife(knifeX, knifeY, pts, frame)
            if not knifeX == 0 or not knifeY == 0:
                for i in range(1, 3):
                    if pts[i - 1] is None or pts[i] is None or pts[i-1] == (0,0) or pts[i] == (0,0):
                        continue
                    pygame.draw.line(frame, (255, 0, 0), pts[i-1], pts[i], 5)
            
            screen.blit(frame, (0,0))
            screen.blit(imgBackground, (0,0))
            #screen.blit(imgWatermelon, rectWatermelon)

            if rectPause.collidepoint(knifeX, knifeY):
                screen.blit(imgPauseHover, rectPauseHover)
                if math.dist((knifeX, knifeY), (thumbX, thumbY)) < 50:
                    pauseFlag = 1
                    waitStart = time.time()
                    while pauseFlag == 1:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pauseFlag = 0
                                running = False

                        success, img = cap.read()
                        img, knifeX, knifeY, thumbX, thumbY = detector.findHands(img)
                        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        imgRGB = np.rot90(imgRGB)
                        frame = pygame.surfarray.make_surface(imgRGB).convert()

                        screen.blit(frame, (0,0))
                        screen.blit(imgBackground, (0,0))

                        screen.blit(imgResume, rectResume)
                        if rectResume.collidepoint(knifeX, knifeY):
                            screen.blit(imgResumeHover, rectResumeHover)
                            if math.dist((knifeX, knifeY), (thumbX, thumbY)) < 50:
                                pausedTime += time.time() - waitStart
                                pauseFlag = 0
                        else:
                            screen.blit(imgResume, rectResume)

                        screen.blit(imgQuit, rectQuit)
                        if rectQuit.collidepoint(knifeX, knifeY):
                            screen.blit(imgQuitHover, rectQuitHover)
                            if math.dist((knifeX, knifeY), (thumbX, thumbY)) < 50:
                                startGameFlag = 0
                                score = 0
                                startTime = time.time()
                                totalTime = 60
                                gameOverFlag = 0
                                bombFlag = 0
                                pausedTime = 0
                                data = {}
                                for fruit in fruits:
                                    generate_random_fruits(fruit)
                                pauseFlag = 0
                        else:
                            screen.blit(imgQuit, rectQuit)

                        for key, value in data.items():
                            if timeRemaining > 50:
                                if key == 'watermelon':
                                    throwFruit(key, value, pauseFlag)
                            elif timeRemaining > 40:
                                if key == 'watermelon' or key == 'apple':
                                    throwFruit(key, value, pauseFlag)
                            elif timeRemaining > 30:
                                if key == 'watermelon' or key == 'apple' or key == 'banana':
                                    throwFruit(key, value, pauseFlag)
                            elif timeRemaining > 20:
                                if key == 'watermelon' or key == 'apple' or key == 'banana' or key == 'kiwi':
                                    throwFruit(key, value, pauseFlag)
                            elif timeRemaining > 10:
                                if key == 'watermelon' or key == 'apple' or key == 'banana' or key == 'kiwi'or key == 'coconut':
                                    throwFruit(key, value, pauseFlag)
                            elif timeRemaining > 0:
                                throwFruit(key, value, pauseFlag)
                            if key == 'bomb':
                                throwFruit(key, value, pauseFlag)

                        textScore = font.render(f'Score:{score}', True, (0, 255, 0))
                        textTime = font.render(f'Time Remaining:{timeRemaining}', True, (0, 255, 0))
                        screen.blit(textScore, (35,35))
                        screen.blit(textTime, (820,35))
                        
                        pygame.display.update()
            else:
                screen.blit(imgPause, rectPause)

            for key, value in data.items():
                if timeRemaining > 50:
                    if key == 'watermelon':
                        throwFruit(key, value, 0)
                elif timeRemaining > 40:
                    if key == 'watermelon' or key == 'apple':
                        throwFruit(key, value, 0)
                elif timeRemaining > 30:
                    if key == 'watermelon' or key == 'apple' or key == 'banana':
                        throwFruit(key, value, 0)
                elif timeRemaining > 20:
                    if key == 'watermelon' or key == 'apple' or key == 'banana' or key == 'kiwi':
                        throwFruit(key, value, 0)
                elif timeRemaining > 10:
                    if key == 'watermelon' or key == 'apple' or key == 'banana' or key == 'kiwi'or key == 'coconut':
                        throwFruit(key, value, 0)
                elif timeRemaining > 0:
                    throwFruit(key, value, 0)
                if key == 'bomb':
                    throwFruit(key, value, 0)
                
                    
            #if rectWatermelon.collidepoint(knifeX, knifeY):
            #    resetWatermelon()
            #    score += 1

            if not knifeX == 0 or not knifeY == 0:
                screen.blit(knifeImg, (knifeX-30, knifeY))
            #screen.blit(frame, (0,0))

            textScore = font.render(f'Score:{score}', True, (0, 255, 0))
            textTime = font.render(f'Time Remaining:{timeRemaining}', True, (0, 255, 0))
            screen.blit(textScore, (35,35))
            screen.blit(textTime, (820,35))

        pygame.display.update()
