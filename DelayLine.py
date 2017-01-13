#DelayLine: Ein Programm, zur Berechnung des Delay beim Aufbau mehrer Lautsprecherreihen
#Malte Worat, Benjamin Carp

import random, pygame, sys, tkFont, math, time	#mport benoetigter Module
from pygame.locals import *


SCHALLGESCHWINDIGKEIT=343   #Konstante fuer die Schallgeschwindigkeit
TEMPERATUR=20	#Temperatur in Grad Celsius

#RGB-Farben
WEISS=(255,255,255)
ROT=(255,0,0)
SCHWARZ=(0,0,0)
GRUEN=(0,255,0)
BLAU=(0,0,255)



laenge=int(0)
breite=int(0)

def start():
#Eingabe der Raumgroesse
	print"Bitte gib die Laenge des Raums in Metern ein!"
	global laenge
	laenge=float(raw_input())

	print"Bitte gib die Breite des Raums in Metern ein!"
	global breite
	breite=float(raw_input())
start()


#Berechnung der Raumgroesse in Quadratmetern
raumgroesse=laenge * breite
print "Die Raumgroesse betraegt", raumgroesse, "Quadratmeter."


#Laengen- und Breitenfloat in int wandeln
laenge=int(math.ceil(laenge))
breite=int(math.ceil(breite))

#Pygame initialisieren, Bildschirmgroesse auslesen
pygame.init()

bildschirmbreite = pygame.display.list_modes()[0][0]
bildschirmhoehe = pygame.display.list_modes()[0][1]

#if-schleife, um einheitliches Format zu erhalten
if laenge < breite:
	print'FEHLER! Breite muss kleiner gleich Laenge sein!'
	print' ---RESTART---'
	start()
	
print "Bitte gib hier die Anzahl der verwendeten Boxenpaare ein (Ganzzahl)"		#Eingabe der verwendeten Anzahl der Boxenpaare
boxenanzahl=int(raw_input())
	

#Berechnung der Fenstergroesse
verhaeltnis=(float(laenge) / float(breite))
startstrecke=laenge
laenge=bildschirmhoehe
breite=bildschirmhoehe / verhaeltnis


def main():
	global MAINSURF, BASICFONT
	
	MAINSURF=pygame.display.set_mode((int(breite), int(laenge)))	#Fenster anlegen
	BASICFONT=pygame.font.Font('freesansbold.ttf', 18)		#Definieren einer Font
	pygame.display.set_caption('DelayLine')		#Name, der in der Leiste angezeigt wird
	
	programLoop()
	showEndScreen()

def terminate():
    pygame.quit()
    sys.exit()
    
boxlinks=pygame.image.load("speakerbox_links.jpg")	#laden des JPEG der linken Box
boxrechts=pygame.image.load("speakerbox_rechts.jpg")	#laden des JPEG der rechten Box


#Startposition der Boxenpaare
startXlinks=10
startYlinks=10
startXrechts=(breite -80)
startYrechts=(10)

def programLoop():
	MAINSURF.fill(SCHWARZ)
	pygame.display.update()
	
	UP=1
	DOWN=2
	LEFT=3
	RIGHT=4
	ENTER=13
	direction="UP"
	MAINSURF.blit(boxlinks, (startXlinks, startYlinks))
	MAINSURF.blit(boxrechts, (startXrechts, startYrechts))
	boxenKoordinaten = [(startXlinks, startYlinks), (startXlinks-1, startYlinks)]
	while True:
		direction = ""
		for event in pygame.event.get():
            #Schliessen ueber x-Button
			if event.type == QUIT:
				terminate()
           
            #Boxen bewegen ueber die Pfeiltasten oder wasd
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a):
					direction = "LEFT"
				if (event.key == K_RIGHT or event.key == K_d):
					direction = "RIGHT"
				if (event.key == K_UP or event.key == K_w):
					direction = "UP"
				if (event.key == K_DOWN or event.key == K_s):
					direction = "DOWN"
				if (event.key == ENTER):
					entfernung()
					return
				

		


		

		
		if direction=="UP":
			boxenKoordinaten = [(boxenKoordinaten[0][0], boxenKoordinaten[0][1]-10)]	#(x-Koordinate,y-Koordinate)
		elif direction=="DOWN":
			boxenKoordinaten = [(boxenKoordinaten[0][0],boxenKoordinaten[0][1]+10)]
		elif direction=="LEFT":
			boxenKoordinaten = [(boxenKoordinaten[0][0]-10,boxenKoordinaten[0][1])]

		elif direction=="RIGHT":
			boxenKoordinaten = [(boxenKoordinaten[0][0]+10,boxenKoordinaten[0][1])]
			
			
		zeichneBox(boxenKoordinaten)
		pygame.display.update()
		
def zeichneBox(boxenKoordinaten):
    #Box zeichnen
	global startYlinks
	MAINSURF.fill(SCHWARZ)
	startXlinks=boxenKoordinaten[0][0]*verhaeltnis
	startYlinks=boxenKoordinaten[0][1]*verhaeltnis
	coordRect=pygame.Rect(startXlinks,startYlinks,20,20)
	pygame.draw.rect(MAINSURF,BLAU,(breite /4, 0, breite /2, 150))		#Zeichnen der Buehne
	MAINSURF.blit(boxlinks, (startXlinks, startYlinks))
	MAINSURF.blit(boxrechts, (startXlinks + breite - 80, startYlinks))
	MAINSURF.blit(boxlinks, (10, 10))
	MAINSURF.blit(boxrechts, (breite - 80, 10))

	
def entfernung():	
#Berechnung der Entfernung
	global StreckeAB
	global timems
	StreckeAB=startYlinks-10
	StreckeAB=StreckeAB / 900 *startstrecke
	timems=StreckeAB/SCHALLGESCHWINDIGKEIT *1000
	showEndScreen()


def showEndScreen():
	MAINSURF.fill(SCHWARZ)
	programEndFont=pygame.font.Font('freesansbold.ttf',40)
	valueSurf=programEndFont.render('Ergebnis:',True,ROT)
	streckeSurf=programEndFont.render(str(StreckeAB) + ' Meter', True, ROT)
	timeSurf=programEndFont.render(str(timems) + ' ms', True, GRUEN)
	valueRect=valueSurf.get_rect()
	streckeRect=streckeSurf.get_rect()
	timeRect=timeSurf.get_rect()
	valueRect.midtop=(breite/2,9+100)
	streckeRect.midtop=(breite/2,9+200)
	timeRect.midtop=(breite/2,9+300)

	MAINSURF.blit(valueSurf,valueRect)
	MAINSURF.blit(streckeSurf, streckeRect)
	MAINSURF.blit(timeSurf, timeRect)
	pygame.display.update()
    
	time.sleep(0.5)
	checkForKeyPress()
	while True:
		if checkForKeyPress():
			return
			
def checkForKeyPress():
	for event in pygame.event.get(QUIT):
		terminate()

	for event in pygame.event.get(KEYUP):
		if event.key==K_ESCAPE:
			terminate()
			return event.key

			
	 
	

	
	
if __name__=='__main__':
    main()
