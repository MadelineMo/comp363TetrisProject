import pygame
import tkinter as tk
import start

song1 = "resources/general.mp3"
icon = "resources/icon.gif"

class Resources():

    def __init__(self):
        pygame.init()

    def startmusic(self):
        global song1
        pygame.mixer.music.load(song1)
        pygame.mixer.music.play(-1)
