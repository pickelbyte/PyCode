import tkinter as tk
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
from tkinter import scrolledtext as sct
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import random
from tkinter import ttk
from tkinter import font
import os
import subprocess

currentfile = None
issaved = True
crfont = ("Arial", 16)

root = tk.Tk()
root.title("PyCode")
root.geometry("720x480")

maintxtfield = sct.ScrolledText(root,
        wrap = tk.WORD,
        width=720,
        height=480,
        font=crfont
)
maintxtfield.pack(expand=True, fill=tk.BOTH)

def openfile(x=None):
    global maintxtfield, root, currentfile
    try:
        try:
            fork = open(fd.askopenfilename(initialdir="~/Documents"), 'r')
            maintxtfield.delete(1.0, tk.END)
            maintxtfield.insert(tk.END, fork.read())
            root.title(f"PyCode - {fork.name}")
            currentfile = fork.name
        except FileNotFoundError:
            pass
    except AttributeError:
        pass
    return x

def new(x=None):
    global root, maintxtfield, currentfile, issaved
    if issaved is True:
        pass
    else:
        response = msg.askokcancel(title="Unsaved Changes", message="All unsaved changes will be lost")
        if response is True:
            root.title("PyCode - New File")
            maintxtfield.delete(1.0, tk.END)
            currentfile = None
        else:
            pass
    return x

def save(x=None):
    global maintxtfield, root, currentfile, issaved
    try:
        txt = maintxtfield.get(1.0, tk.END)
        name = fd.asksaveasfile(parent=root, title="Save as...", defaultextension=".txt", initialdir="~/Documents")
        with open(name.name, 'w') as f:
            f.write(txt)
        root.title(f"PyCode - {name.name}")
        currentfile = name.name
        issaved = True
    except AttributeError:
        print("AttributeError")

    return x

def checksaved(x=None):
    global maintxtfield, root, currentfile, issaved
    entrytxt = maintxtfield.get(1.0, tk.END)
    try:
        with open(currentfile, 'r') as f:
            filetxt = f.read()

        if entrytxt == filetxt:
            issaved = True
            root.title(f"PyCode - {currentfile}")
        else:
            issaved = False
            root.title(f"*PyCode - {currentfile}*")
    except TypeError:
        pass
    return x

def getsfont():
    global fontsbox, fsize
    size = 12
    try:
        size = int(fsize.get())
    except ValueError:
        pass
    for x in fontsbox.curselection():
        return (fontsbox.get(x), size)

def changefont():
    global maintxtfield, root, fonts, fontsbox, fsize
    fontwin = tk.Toplevel(root)
    fontsbox = tk.Listbox(fontwin)
    fontsbox.pack(pady=20, expand=True, fill=tk.BOTH)
    for f in fonts:
        fontsbox.insert(tk.END, f)
    applybtn = ttk.Button(fontwin, text="Apply", command=lambda: maintxtfield.config(font=(getsfont())))
    fsize = tk.Entry(fontwin)
    fsize.pack()
    applybtn.pack()

def run(x):
    global currentfile
    process = subprocess.Popen(['python', currentfile],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr

""" def opencout(x=None):
    global console, closebtn
    console = sct.ScrolledText(root, 
                            height=240, 
                            width=720, 
                            wrap=tk.WORD, 
                            font=("Consolas", 12)
                            )
    console.place(x=0, y=240)
    closebtn = tk.Button(root, text="X", command=closecout)
    closebtn.place(x=700, y=220)
    return x

def closecout():
    global console, closebtn
    console.destroy()
    closebtn.destroy() """

fonts = list(font.families())
fonts.sort()
crfont = (random.choice(fonts), 12)

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New (Ctrl-N)", command=new)
filemenu.add_command(label="Open (Ctrl-O)", command=openfile)
filemenu.add_command(label="Save (Ctrl-S)", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

formatmenu = tk.Menu(menubar, tearoff=0)
formatmenu.add_command(label="Change Font", command=changefont)
menubar.add_cascade(label="Format", menu=formatmenu)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)

# cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}

ip.Percolator(maintxtfield).insertfilter(cdg)

root.bind('<Control-s>', save)
root.bind('<Control-o>', openfile)
root.bind('<Control-n>', new)
root.bind('<Control-r>', run)
root.bind("<KeyRelease>", checksaved)
root.config(menu=menubar)
root.mainloop()
