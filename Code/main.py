from test import * 
from Processing_Class import *
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import sys


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    timeTracker = TimeTracker(manager)
    block_apps = Block_Apps()

    # Print a word char by char
    def printString(item, string,_time=0.07):
        if item:
            for char in string:
                idx = canvas.index(item, tk.END)
                canvas.insert(item, idx, char)
                canvas.update()
                time.sleep(_time)

    # Populate the canvas with all the block apps
    def Block_apps_window(_canvas):
        _canvas.delete('all')
        block_apps_title = _canvas.create_text(105, 45, font=("Inconsolata SemiExpanded Medium",16), fill="#b2cfca")
        block_apps_text = "Block Apps"
        printString(block_apps_title,block_apps_text)
        block_app_label1 = _canvas.create_text(115, 95,font=("Inconsolata SemiExpanded",14), fill="#b2cfca")
        text = "Program"
        printString(block_app_label1,text,.02)
        block_app_label2 = _canvas.create_text(335, 95,font=("Inconsolata SemiExpanded",14), fill="#b2cfca")
        text = "Time Block"
        printString(block_app_label2,text,.02)
        applications = len(block_apps.programs_block)+1
        corY = 65+(245/applications)
        for app in block_apps.programs_block.keys():
            _canvas.create_text(115, corY ,text=app ,font=("Inconsolata",13), fill="#fee9d1")
            corY += (245/applications)
        global directions 
        directions= _canvas.create_text(140, corY+50 ,text="(1) Reload Function\n(2) Usage Time\n(3) Enter A Program to Block" ,font=("Inconsolata",13), fill="#b2cfca")
        _canvas.create_text(50, corY+115 ,text="× " ,font=("Inconsolata",25), fill="#fee9d1")
        _canvas.create_window(142,corY+115,window=e1)
        e1.focus()
        root.bind('<Return>',press_enter2)


    # Populate the canvas with all usage time information
    def open_time_track(_root,_canvas):
        _canvas.delete('all')
        time_track_title = _canvas.create_text(105, 45, font=("Inconsolata SemiExpanded Medium",16), fill="#b2cfca")
        track_time = "Usage Time"
        printString(time_track_title,track_time)
        time_track_label1 = _canvas.create_text(115, 95,font=("Inconsolata SemiExpanded",14), fill="#b2cfca")
        text="Program"
        printString(time_track_label1,text,.02)
        time_track_label2 = _canvas.create_text(335, 95 ,font=("Inconsolata SemiExpanded",14), fill="#b2cfca")
        text="Active Time"
        printString(time_track_label2,text,.02)
        time_track_label3 = _canvas.create_text(585, 95 ,font=("Inconsolata SemiExpanded",14), fill="#b2cfca")
        text="Usage Time"
        printString(time_track_label3,text,.02)
        applications = len(timeTracker.active_applications)+1
        corY = 65+(245/applications)
        text_labels = []
        apps_used = []
        for app in timeTracker.active_applications.values():
            apps_used.append(app)
            _canvas.create_text(115, corY ,text=app ,font=("Inconsolata",13), fill="#fee9d1")
            label1 = _canvas.create_text(335, corY ,text=timeTracker.active_time[app] ,font=("Inconsolata",13), fill="#fee9d1")
            threading.Thread(target=update_text,args=(_canvas,app,label1),daemon=True).start()
            text_labels.append(label1)
            label2 =_canvas.create_text(585, corY ,text=timeTracker.active_usage_time[app] ,font=("Inconsolata",13), fill="#fee9d1")
            threading.Thread(target=update_text,args=(_canvas,app,label2,1),daemon=True).start()
            text_labels.append(label2)
            corY += (245/applications)
        _canvas.create_text(115, corY ,text="Computer Active\nTime Today: ",font=("Inconsolata",13), fill="#b2cfca")
        label3 =_canvas.create_text(223, corY+15 ,text=timeTracker.computer_active_time,font=("Inconsolata",13), fill="#fee9d1")
        threading.Thread(target=update_text,args=(_canvas,app,label3,2),daemon=True).start()
        _canvas.create_text(115, corY+65 ,text="(1) Reload Function\n(2) Block Apps" ,font=("Inconsolata",13), fill="#b2cfca")
        _canvas.create_text(50, corY+115 ,text="× " ,font=("Inconsolata",25), fill="#fee9d1")
        _canvas.create_window(142,corY+115,window=e1)
        e1.focus()
        _root.bind('<Return>',press_enter)

    # check if the user type enter
    def press_enter(event):
        user_input=e1.get()
        e1.delete(0, 'end')
        if user_input=='1':
            open_time_track(root,canvas)
        elif user_input=='2':
            Block_apps_window(canvas)

    def press_enter2(event):
        global directions
        user_input=e1.get()
        e1.delete(0, 'end')
        if user_input=='1':
            Block_apps_window(canvas)
        elif user_input=='2':
            open_time_track(root,canvas)
        elif user_input=='3':
            canvas.delete(directions)
            directions= canvas.create_text(220,370,text="(1) Go Back\nEnter the name of the program to Lock" ,font=("Inconsolata",14), fill="#b2cfca")
            root.bind('<Return>',press_enterdata)
    
    def press_enterdata(event):
        global directions
        user_input=e1.get()
        e1.delete(0, 'end')
        data = user_input.split(" ")
        if user_input == '1':
            canvas.delete(directions)
            directions= canvas.create_text(140, 360 ,text="(1) Reload Function\n(2) Usage Time\n(3) Enter A Program to Block" ,font=("Inconsolata",13), fill="#b2cfca")
            root.bind('<Return>',press_enter2)
            e1.focus()
        elif user_input.replace(" ", "") == "":
            e1.insert(0,"Enter a Program")
            e1.selection_range(0, END)
        else:
            if len(data)>1:
                program_name = user_input.split(" ")[0]
                time_to_block = user_input.split(" ")[1]
                time_to_block = time_to_block.split(":")
                time_to_block = timedelta(hours=time_to_block[0],minutes=time_to_block[1],seconds=[2])
                block_apps.block_program(program_name,time_to_block)
            else:
                program_name = user_input.split(" ")[0]
                block_apps.block_program(program_name)
            Block_apps_window(canvas)

    def press_enter_unblock(event):
        user_input=e1.get()
        e1.delete(0, 'end')
        program_name = user_input.split(" ")[0]
        block_apps.unblock_program(program_name)


    def update_text(_canvas,_app=None,_text_object=None,mode=0):
        while True:
            try:
                if mode == 0:
                    _canvas.itemconfig(_text_object ,text=timeTracker.active_time[_app])
                elif mode==1:
                    _canvas.itemconfig(_text_object ,text=timeTracker.active_usage_time[_app])
                elif mode==2:
                    _canvas.itemconfig(_text_object ,text=timeTracker.computer_active_time)
                _canvas.update()
                time.sleep(.5)
            except:
                sys.exit()

    root = tk.Tk()
    root.overrideredirect(True) 
    w = 750  # width for the Tk root
    h = 450  # height for the Tk root

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Define Image
    splash_img = Image.open("Pictures/SplashScreen.PNG")
    splash_img_resize = splash_img.resize((500, 300), Image.ANTIALIAS)
    new_pic = ImageTk.PhotoImage(splash_img_resize)
    canvas = Canvas(root, width=w, height=h, bd=-2, bg="#01080e")
    canvas.pack(fill="both", expand=False)
    splash_image = canvas.create_image(120, 89, image=new_pic, anchor="nw")  # put an image inside the canvas
    splash_title = canvas.create_text(115, 50, font=("Rockwell",32), fill="#bbd5d0")
    text = "Kairós"
    printString(splash_title,text)
    splash_version = canvas.create_text(648, 422, font=("Inconsolata",15), fill="#bbd5d0")
    beta_text = "Beta Version 1.0"
    printString(splash_version,beta_text)
    canvas.update()
    time.sleep(1)
    directions = None
    canvas.configure(bg='#171717',bd=0, highlightthickness=0)
    e1 = Entry(root,bg='#171717',bd=0, highlightthickness=0,font=("Inconsolata",13),fg="#BBBBBB",insertbackground="#BBBBBB")
    open_time_track(root,canvas)
    root.mainloop()

    