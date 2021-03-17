import pygame
import tkinter as tk
import resources


class Start(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.screen()

    def screen(self):
        s = tk.StringVar(value="\n Start\n")
        self.label = tk.Label(self, textvariable = s)
        self.label.pack(side="top")

        self.one = tk.Button(self, bg = "blue", fg = "white", command=self.destroy)
        self.one["text"] = "START"
        self.one.pack(side="bottom")

    def destroy(self):
        self.label.destroy()
        self.one.destroy()
