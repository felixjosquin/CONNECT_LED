# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 16:20:53 2020

@author: Félix
"""

import serial
from tkinter import *
import numpy as np
from PIL import ImageGrab
import time

s=serial.Serial('COM11',9600)
s.timeout= 1

dx=12
n_led=10
L=[[50, 960, 644, 1078],[2, 550, 120, 1030],[2, 50, 120, 530],[50, 2, 644, 120],[663, 2, 1257, 120],[1278, 5, 1872, 120],[1800, 50, 1918, 530],[1800, 550, 1918, 1030],[1278, 960, 1872, 1078],[663, 960, 1257, 1078]]

couleur='#000000'

def take_m(a,b,T):
    Y=T[a[1]:b[1],a[0]:b[0],:]
    txt=''
    for i in range(3):
        txt=txt+moyenne(Y[:,:,i])
    return txt

     
def moyenne(Y):
    h=len(Y)//dx
    l=len(Y[0])//dx
    S=0
    k=0
    if h<l:
        for i in range(h):
            for j in range(l):
                if l/4<j<3*l/4:
                    S+=Y[i*dx,j*dx]*2
                    k+=2
                else:
                    S+=Y[i*dx,j*dx]
                    k+=1
    if l<h:
        for i in range(h):
            for j in range(l):
                if h/4<i<3*h/4:
                    S+=Y[i*dx,j*dx]*2
                    k+=2
                else:
                    S+=Y[i*dx,j*dx]
                    k+=1
    x=hex(int(S/k))[2:]
    while len(x)<2:
        x='0'+x
    return x



class afficher:
    
    def __init__(self):
        self.etat=True
        self.open=False

        self.root = Tk()
        self.root.title("")
        self.root.geometry('200x150+1888+1020')
        self.root.config(background=couleur)

        frame=Frame(self.root,bg=couleur)
        framei=Frame(frame,bg=couleur)
        frameii=Frame(framei,bg=couleur)
        framex=Frame(self.root,bg=couleur)
        framex.pack(side=TOP)
        frame.pack(expand=YES,pady=20)
        framei.grid(row=0,column=1,sticky=W)

        label = Label(framex, text='       ', font=("courrier",9),bg=couleur,fg='white',relief='flat')
        label.grid(row=0,column=1,sticky=W,padx=50)
        but_x = Button(framex, text=' x ', font=("courrier",9,'bold'),bg=couleur,fg='white',command = self.x,activebackground=couleur,activeforeground='white',relief='flat')
        but_x.grid(row=0,column=0,sticky=W,padx=2)
        but_quit = Button(framex, text='Quitter', font=("courrier",8),bg=couleur,fg='white',command = self.leave,activebackground=couleur,activeforeground='white',relief='flat')
        but_quit.grid(row=0,column=3,sticky=W,padx=2)
        but_run = Button(frame, text=' run ! ',font=("courrier",16),bg=couleur,fg='white',command = self.click,activebackground=couleur,activeforeground='white',relief='flat')
        but_run.grid(row=0,column=0,sticky=W,padx=20)
        butplus = Button(frame, text='  +  ',font=("courrier", 11,'bold'),bg=couleur,fg='white',command = self.plus,activebackground=couleur,activeforeground='white',relief='flat')
        butplus.grid(row=0,column=1,sticky=W,padx=2)
        butmoins = Button(frame, text='  -  ',font=("courrier", 12 , 'bold'),bg=couleur,fg='white',command = self.moins,activebackground=couleur,activeforeground='white',relief='flat')
        butmoins.grid(row=0,column=2,sticky=W,padx=5)

        self.root.bind('<Return>',lambda i: self.click())
        self.root.bind('<KeyPress-plus>',lambda i: self.plus())
        self.root.bind('<KeyPress-minus>',lambda i: self.moins())
        self.root.overrideredirect(1)

        self.run()
        self.root.mainloop()

    def x(self) :
        self.open=not self.open
        if self.open:
            self.root.geometry('200x150+1717+888')
        else:
            self.root.geometry('200x150+1888+1020')  

    def plus(self) :
        s.write('i+'.encode('utf-8'))

    def moins(self) :
        s.write('i-'.encode('utf-8'))

    def click(self):
        self.etat=not self.etat
        self.run()

    def run(self):
        if self.etat:
            im = ImageGrab.grab()
            T = np.array(im) 
            s.write('c'.encode('utf-8'))
            for i in range(n_led):
                s.write((take_m(L[i][:2],L[i][2:], T)).encode())
            self.root.after(2, self.run)
        else:
            s.write('c'.encode('utf-8'))
            for i in range(n_led):
                s.write(('000000').encode())

    def leave(self):
        self.root.destroy()
        s.write('c'.encode('utf-8'))
        for i in range(n_led):
            s.write(('000000').encode())
        s.close()

afficher()
s.close()