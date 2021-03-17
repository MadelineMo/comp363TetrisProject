import pygame
import tkinter as tk
import start
import resources

res = resources.Resources()
res.startmusic() #loads music // we dont need to keep the music if u hate it

'''initalize gui'''
root = tk.Tk() #initializes the gui class
root.geometry("850x900") #sets window length width
root.title("Tetris") #sets title for program
photo = tk.PhotoImage(file = resources.icon) #grabs photo
root.iconphoto(False, photo) #sets icon photo
app = start.Start(master=root) #initializes the window
app.mainloop() #loops app until the user quits
