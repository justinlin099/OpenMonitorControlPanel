from tkinter import messagebox
import tkinter as tk
from pystray import MenuItem as item
import pystray
import PIL.Image
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os

#套用樣式
controlPanel = ttk.Window(themename="cyborg")
controlPanel.resizable(False,False)


#設定視窗參數
controlPanel.title('OpenMonitorControlPanel')
controlPanel.attributes("-alpha", 0.8)
controlPanel.attributes("-topmost", 1)
controlPanel.geometry('400x600-0-35')


#System Tray Code

def quit_window(icon, item):
    icon.stop()
    controlPanel.destroy()

def show_window(icon, item):
    icon.stop()
    controlPanel.after(0,controlPanel.deiconify)

def withdraw_window():  
    controlPanel.withdraw()
    image = PIL.Image.open("image.ico")
    menu = (item('離開', quit_window), item('顯示', show_window ,default=True))
    icon = pystray.Icon("name", image, "Open Monitor Control Panel", menu)
    icon.run()

controlPanel.protocol("WM_DELETE_WINDOW", withdraw_window)

#掃描螢幕

def scanMonitor():
    os.system("ControlMyMonitor.exe /smonitors smonitors.txt")
    file = open('smonitors.txt', 'r',encoding="utf-16 le")

    MonitorList = file.readlines()
    messagebox.showinfo("掃描完成" , "找到 " + str(len(MonitorList)//6) + " 個螢幕" )
    file.close()
    Monitors=[]
    for i in range(len(MonitorList)//6):
        os.system("ControlMyMonitor.exe /scomma monitor"+ str(i) +".txt "+MonitorList[0+6*i][22:])
        file = open('monitor'+str(i)+'.txt', 'r',encoding="utf-8")

        Monitors.append(file.readlines())
        file.close()
        print(Monitors[i][10])
    
    

#Setup
refreshButton = ttk.Button(controlPanel, text="更新螢幕清單", bootstyle="default",command=scanMonitor)
refreshButton.place(x=300,y=5)





scanMonitor()
controlPanel.mainloop()

