#!/usr/bin/env python3
#
# Main Code For ceaserSalad
#

import tkinter as tk
from tkinter import scrolledtext, N, E, S, W
from tkinter import filedialog, simpledialog
from pathlib import Path


class engine:

    soup = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~0123456789 \n\t'''
    def __init__(self):
        self.map = {}
        for char in self.soup:
            self.map[char] = self.soup.index(char)
    def encrypt(self, plainText, secret):
        ind, cypher, l, s = 0, str(), len(secret), len(self.soup)
        for char in plainText:
            cypher += self.shift(char, secret, ind, l, s)
            ind += 1
        return cypher
    def decrypt(self, cipher, secret):
        ind, plain, l, s = 0, str(), len(secret), len(self.soup)
        for letter in cipher:
            plain += self.shift(letter, secret, ind, l, s, -1)
            ind += 1
        return plain
    def shift(self, letter, secret, ind, l, s, sign=1):
        try:
            return self.soup[(self.map[letter] + sign * self.map[secret[ind % l]]) % s]
        except:
            raise ValueError(f'String includes invalid characters, allowed are \n{self.soup}')


class editor (tk.Tk):

    def __init__ (self):

        tk.Tk.__init__(self)

        self.title("ceaserSalad")
        self.engine = engine()
        
        # window geometry
        self.size = (500, 600)
        self.geometry("{}x{}".format(*self.size))
        self.navHeight = 20
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1) 

        # types for explorer
        self.fileTypes = (("Text files", "*.txt"), ("Data files", "*.dat"), ("all files", "*.*"))
        self.savePath = None

        # build UI
        self.build()

        self.mainloop()

    def about (self):

        pass 

    def build (self):

        self.navBar = tk.Frame(self, height=self.navHeight, bg="#ddd")
        self.navBar.grid(row=0, columnspan=20, rowspan=1, sticky=N+S+E+W)
        self.navBar.grid_propagate(0)

        self.fileDropDown = tk.Menubutton(self.navBar, text="File")
        self.fileDropDown.menu =  tk.Menu( self.fileDropDown, tearoff = 0 )
        self.fileDropDown["menu"] = self.fileDropDown.menu  
        self.fileDropDown.menu.add_command(label='Open', command=self.open)
        self.fileDropDown.menu.add_command(label='Save', command=self.save)
        self.fileDropDown.menu.add_command(label='Save as', command=self.save_as)
        self.fileDropDown.menu.add_command(label='About', command=self.save_as)
        self.fileDropDown.grid(row=0, column=0)

        self.encryptButton = tk.Button(self.navBar, text="Encrypt", command=self.encryptAction)
        self.encryptButton.grid(row=0, column=1)

        self.decryptButton = tk.Button(self.navBar, text="Decrypt", command=self.decryptAction)
        self.decryptButton.grid(row=0, column=2)

        self.textField = scrolledtext.ScrolledText(self)
        self.textField.grid_propagate(0)
        self.textField.grid(row=1, column=0, rowspan=19, columnspan=20, sticky=N+S+E+W)
    
    def decryptAction (self):

        password = simpledialog.askstring("Decrypt", "Enter password:")
        cipher = self.get()
        plaintext = self.engine.decrypt(cipher, password)
        self.textField.delete(1.0, tk.END)
        self.textField.insert(1.0, plaintext)
    
    def encryptAction (self):

        password = simpledialog.askstring("Encrypt", "Enter password:")
        plaintext = self.get()
        print(plaintext)
        cipher = self.engine.encrypt(plaintext, password)
        self.textField.delete(1.0, tk.END)
        self.textField.insert(1.0, cipher)
    
    def get(self):

        '''
        Get text from text field.
        '''

        return self.textField.get(1.0, tk.END)[:-1]

    def open (self):

        '''
        Open file path routine.
        '''
        
        # override path
        self.savePath = Path(filedialog.askopenfilename(initialdir="~", filetypes=self.fileTypes))

        # drop file content into text field
        with open(self.savePath) as f:
            self.textField.insert(tk.INSERT, f.read())
    
    def save (self):

        '''
        Quick save routine.
        '''

        if not self.savePath:
           self.save_as()
           return

        # drop file content into text field
        with open(self.savePath, 'w+') as f:
            f.write(self.get())
    
    def save_as (self):

        '''
        Save as routine.
        '''

        # override the savepath
        f = filedialog.asksaveasfile(initialdir="~", defaultextension=self.fileTypes[0][1])
        self.savePath = Path(f.name)
        f.write('*')
        f.close()

        # quick save
        self.save()