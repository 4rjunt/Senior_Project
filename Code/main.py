import tkinter
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import ImageTk,Image

#Create Splash Screen
splash_root = Tk()
splash_root.overrideredirect(True) #set the labels in the SplashScreen
w = 700 # width for the Tk root
h = 400 # height for the Tk root

# get screen width and height
ws = splash_root.winfo_screenwidth() # width of the screen
hs = splash_root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen and where it is placed
splash_root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# define Image
splash_img = Image.open("c:/Users/Desktop/Desktop/Weas/Fotos/a.png")
splash_img_resize = splash_img.resize((700,400), Image.ANTIALIAS)
new_pic = ImageTk.PhotoImage(splash_img_resize)

#Create a canvas inside the splash screen root
splash_canvas = Canvas(splash_root,width=w,height=h,cursor="circle",bd=-2,bg="#464646")
splash_canvas.pack(fill="both",expand=True)
splash_image = splash_canvas.create_image(0,0,image=new_pic,anchor="nw") # put an image inside the canvas
splash_title = splash_canvas.create_text(160,110,text="Program\nOf\nEfficiency",font=("Rockwell",38),fill="white")
splash_version = splash_canvas.create_text(590,380,text="Beta Version 0.1",font=("Courier New",15),fill="white")


def main_window():
    splash_root.destroy()
    root = Tk()
    root.title('Program Of Efficiency')
    root.state('zoomed')
    root.geometry("500x500")

    # set a menu bar
    menubar = Menu(root,background="#464646")
    main_menu = Menu(menubar, tearoff=0)
    main_menu.add_command(label="Apps Usage Times")
    main_menu.add_separator()
    main_menu.add_command(label="(Coming Soon) Block Apps",state=tkinter.DISABLED)
    main_menu.add_command(label="(Coming Soon) Calendar",state=tkinter.DISABLED)
    menubar.add_cascade(label="Menu", menu=main_menu)

    appearance_menu = Menu(menubar, tearoff=0)
    appearance_menu.add_command(label="(Coming Soon)",state=tkinter.DISABLED)
    menubar.add_cascade(label="Appearance", menu=appearance_menu)

    root.config(menu=menubar)

#Splash Screen Timer
splash_root.after(1500, main_window)

mainloop()

ApplicationUsage = Usage_time()
ApplicationUsage.active_time()
