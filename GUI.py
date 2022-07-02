# Import tkinter
import tkinter as tk
import time

# ttk is basically the css for tkinter
from tkinter import ttk

# OS to get the relative path of the project folder
import os

# date time for datetime functions
from datetime import datetime

# Used to get the screen size
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


XLARGE_FONT  = ("Verdana",30, 'bold')
LARGE_FONT = ("Verdana",20, 'bold')
NORM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)

dirname = os.path.dirname(__file__)
#Database = os.path.join(dirname, 'data/project.db')

# Add inheritants to the parentheses
class ProjectTrackerApp(tk.Tk):
    # Initialize funtion will always run when the class is called
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self, "Self Improvment Project")

        container = tk.Frame(self,bg='purple')
        container.grid(row=0,column=0,sticky='nsew')

        # Adding different options to the menu bar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)

        # Adding top indicators (which will be adjusted for my application)
        tk.Tk.config(self, menu=menubar)

    # Eventually we will have a bunch of frames, they will all exist but one will be on top and can change
        self.frames = {}

        for F in (HomePage, ProjectsPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class ProjectsPage(tk.Frame):
    def __init__(self,parent,controller):
        today = datetime.today().date()
        now = datetime.now()
        tk.Frame.__init__(self,parent)
        self.grid_propagate(1)

class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        today = datetime.today().date()
        now = datetime.now()
        tk.Frame.__init__(self,parent)
        self.grid_propagate(1)

app = ProjectTrackerApp()
app.geometry("{}x{}".format(int(screensize[0]/1.5),int(screensize[1]/1.5)))
#ani = animation.FuncAnimation(f, animate, interval=1000)
app.update()
app.mainloop()