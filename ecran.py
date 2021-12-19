# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:58:52 2020

@author: Félix
"""
from tkinter import *
root = Tk()
root.geometry('1080x1920')
root.attributes("-fullscreen", True)
c=Canvas(root, width=1920, height=1080, bg='ivory')
c.pack()


L=[[50, 960, 644, 1078],[2, 550, 120, 1030],[2, 50, 120, 530],[50, 2, 644, 120],[663, 2, 1257, 120],[1278, 5, 1872, 120],[1800, 50, 1918, 530],[1800, 550, 1918, 1030],[1278, 960, 1872, 1078],[663, 960, 1257, 1078]]
for i in range(10):
    a='#0000'+hex((i+2)*255//11)[2:]
    c.create_rectangle(L[i][:2],L[i][2:],fill=a)
# but_quit = Button(c, text='Quitter', command = root.destroy)
# but_quit.pack()
root.mainloop()