from tkinter import messagebox
import tkinter as tk
from pystray import MenuItem as item
import pystray
import PIL.Image
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from functools import partial

#套用樣式
controlPanel = ttk.Window(themename="cyborg")
controlPanel.resizable(False,False)


#設定視窗參數
controlPanel.title('OpenMonitorControlPanel Alpha 0.1')
controlPanel.attributes("-alpha", 0.8)
controlPanel.attributes("-topmost", 1)
controlPanel.geometry('400x600-0-35')

#導入圖片
VGAImg = PhotoImage(file = r"VGA.png")
HDMIImg = PhotoImage(file = r"HDMI.png")
DPImg = PhotoImage(file = r"DP.png")

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
    menu = (item('退出', quit_window), item('顯示', show_window ,default=True))
    icon = pystray.Icon("name", image, "Open Monitor Control Panel", menu)
    icon.run()

controlPanel.protocol("WM_DELETE_WINDOW", withdraw_window)

#切換輸入

def selectInput(monitorString , inputValue):
    os.system("ControlMyMonitor.exe /SetValue " + monitorString + " 60 "+inputValue)
    print("ControlMyMonitor.exe /SetValue " + monitorString + " 60 "+inputValue)




#掃描螢幕

def scanMonitor():
    os.system("ControlMyMonitor.exe /smonitors smonitors.txt")
    file = open('smonitors.txt', 'r',encoding="utf-16 le")

    MonitorList = file.readlines()
    MonitorList[0]=MonitorList[0][1:]
    
    messagebox.showinfo("掃描完成" , "找到 " + str(len(MonitorList)//6) + " 個螢幕" )
    file.close()
    Monitors=[]
    OptionList=[]
    lf=[]
    inputButton=[]
    inputOptions=[]
    for i in range(len(MonitorList)//6):
        os.system("ControlMyMonitor.exe /scomma monitor"+ str(i) +".txt "+MonitorList[0+6*i][21:])
        print("ControlMyMonitor.exe /scomma monitor"+ str(i) +".txt "+MonitorList[0+6*i][21:])
        file = open('monitor'+str(i)+'.txt', 'r',encoding="utf-8")
        Monitors.append(file.readlines())
        file.close()
        OptionList.append({})
        for j in range(len(Monitors[i])):
            OptionList[i][Monitors[i][j][:2]]=Monitors[i][j].split(",",5)
        
        print(OptionList[i]["60"][5])

        #生成螢幕控制區塊
        lf.append(ttk.LabelFrame(controlPanel, text=MonitorList[1+6*i][15:-2]))
        lf[i].pack(fill='x',padx=10,pady=5)
        inputButton.append([])
        
        inputOptions.append(OptionList[i]["60"][5][1:-2].split(','))
        for j in range(len(inputOptions[i])):
            if(int(inputOptions[i][j])<15):
                action_with_arg = partial(selectInput, MonitorList[0+6*i][21:-1], inputOptions[i][j])
                inputButton[i].append(ttk.Button(lf[i], text="VGA", image = VGAImg, compound=TOP, bootstyle="secondary",command=action_with_arg))
                
            elif(int(inputOptions[i][j])<17):
                action_with_arg = partial(selectInput, MonitorList[0+6*i][21:-1], inputOptions[i][j])
                inputButton[i].append( ttk.Button(lf[i], text="DP", image = DPImg, compound=TOP,bootstyle="secondary",command=action_with_arg))
                
            else:
                action_with_arg = partial(selectInput, MonitorList[0+6*i][21:-1], inputOptions[i][j])
                inputButton[i].append(ttk.Button(lf[i], text="HDMI", image = HDMIImg, compound=TOP,bootstyle="secondary",command=action_with_arg))
                
            inputButton[i][j].grid(row=0, column=j, padx=5, pady=5)
    
    
    

#Setup
refreshButton = ttk.Button(controlPanel, text="更新螢幕清單", bootstyle="default",command=scanMonitor)
refreshButton.pack(anchor=tk.NE,padx=10,pady=10)




scanMonitor()
controlPanel.mainloop()

