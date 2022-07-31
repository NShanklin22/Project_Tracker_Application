# Import tkinter
import tkinter as tk
import time

# ttk is basically the css for tkinter
from tkinter import ttk

# OS to get the relative path of the project folder
import os

# date time for datetime functions
from datetime import datetime

# Sql for task dataframes
import sqlite3
import pandas as pd
import sqlalchemy

# Used to get the screen size
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Create a standard app width and height to be used later
app_width = int(screensize[0]/1.5)
app_height = int(screensize[1]/1.5)

XLARGE_FONT  = ("Verdana",30, 'bold','underline')
LARGE_FONT = ("Verdana",20, 'bold')
NORM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)

TABLE_FONT = ("Verdana",30)

dirname = os.path.dirname(__file__)
Database = os.path.join(dirname, 'data/tasks.db')
connection = sqlite3.connect(Database)
cursor = connection.cursor()
engine = sqlalchemy.create_engine(r'sqlite:///{}'.format(Database)).connect()
df = pd.read_sql_table('tasks', engine, index_col=1)

# Add inheritants to the parentheses
class ProjectTrackerApp(tk.Tk):
    # Initialize funtion will always run when the class is called
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self, "Project Tracker Application")

        # Configure columns for 1:5 ratio for side menu
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=10)
        # self.grid_rowconfigure(0, weight=1)

        # Main canvas that all frames/widgets will sit on
        mainCanvas = tk.Frame(self,bg='blue',width=int(app_width*4/5),height=app_height)
        mainCanvas.grid(row=0,column=1,sticky='nsew')
        mainCanvas.grid_propagate(1)

        # Adding different options to the menu bar
        menubar = tk.Menu(mainCanvas)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)
        sortmenu = tk.Menu(menubar,tearoff=0)
        sortmenu.add_separator()
        sortmenu.add_command(label="By Number",command=quit)
        menubar.add_cascade(label="Sort",menu=sortmenu)

        # Adding top menu options
        tk.Tk.config(self, menu=menubar)

        sideMenu = SideMenu(self,self)
        sideMenu.grid(row=0,column=0,sticky="nsew")

    # Eventually we will have a bunch of frames, they will all exist but one will be on top and can change
        self.frames = {}

        for F in (HomePage,TasksPage, ProjectsPage):
            frame = F(mainCanvas,self)
            self.frames[F] = frame
            #frame.grid_propagate(0)
            frame.grid(column=1,row=0,stick="nsew")

        self.show_frame(HomePage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class SideMenu(tk.Frame):
    def __init__(self,parent,controller):
        today = datetime.today().date()
        now = datetime.now()
        tk.Frame.__init__(self,parent,width = int(app_width/5), height = app_height)
        self.pack_propagate(0)

        # Add the side menu buttons
        # Home button to return to main page
        homeButton = tk.Button(self,text="Home", font=LARGE_FONT, command=lambda: controller.show_frame(HomePage))
        homeButton.pack(fill="both")
        # Projects will list all current projects
        tasksPage = tk.Button(self,text="Tasks", font=LARGE_FONT, command=lambda: controller.show_frame(TasksPage))
        tasksPage.pack(fill="both")
        # Projects will list all current projects
        projectsButton = tk.Button(self,text="Projects", font=LARGE_FONT, command=lambda: controller.show_frame(ProjectsPage))
        projectsButton.pack(fill="both")
        # Exit the application
        exitButton = tk.Button(self,text="Exit", font=LARGE_FONT,command=exit)
        exitButton.pack(fill="both")

    def expandButton(self):
        return

class HomePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,width=app_width*4/5, height=app_height)
        self.grid_propagate(0)
        self.columnconfigure(0,weight=1)
        Label01 = tk.Label(self,text="Project Tracker Tool", font=XLARGE_FONT,wraplength=400)
        Label01.grid(column=0,row=0, sticky="nsew")
        Label02 = tk.Label(self,text="How the heck do these managers work", font=LARGE_FONT,wraplength=400)
        Label02.grid(column=0,row=1, sticky="nsew")

class TasksPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.columnconfigure(0,weight=1)
        Label01 = tk.Label(self,text="Tasks Page", font=XLARGE_FONT)
        Label01.grid(column=0,row=0,sticky="nsew")
        print(self.displayTasks())

    def displayTasks(self):
        tasksFrame = tk.Frame(self,bg='blue',width=int(app_width*4/5),height=app_height)
        tasksFrame.grid(column=0,row=1)
        df_dict = df.to_dict(orient='records')
        print(int((app_width*4/5)))
        r = 0
        # Create a zero image to be used for the labels
        img = tk.PhotoImage()
        #headerFrame = tk.Frame(tasksFrame,width=int(app_width*4/5)).grid()
        for i in range(len(df_dict)):
            r = r + 1
            taskFrame = tk.Frame(tasksFrame,bg='red',width=int(app_width*4/5),relief="sunken",borderwidth=10)
            taskFrame.grid_propagate(0)
            taskFrame.grid(column=1,row=r,sticky='nsew')
            for key in df_dict[i]:
                cellFrame = tk.Frame(taskFrame, width=int(app_width*4/5/8), height= int(app_height/4) ,relief="sunken",borderwidth=10)
                #cellFrame.pack_propagate(0)
                cellFrame.pack(side='left')
                label = tk.Label(cellFrame,text=df_dict[i][key], font=TABLE_FONT,wraplength=int(app_width*4/5/8))
                label.pack(side='left')


class ProjectsPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.columnconfigure(0,weight=1)
        Label01 = tk.Label(self,text="Projects Page", font=XLARGE_FONT)
        Label01.grid(column=0,row=0,sticky="nsew")


app = ProjectTrackerApp()
app.geometry("{}x{}".format(app_width,app_height))
app.resizable(False,False)
#ani = animation.FuncAnimation(f, animate, interval=1000)
app.update()
app.mainloop()