from asyncio.windows_events import NULL
from calendar import c
from faulthandler import disable
from operator import truediv
from optparse import Option
from tkinter import messagebox
import tkinter as tk
from turtle import color, width
from pystray import MenuItem as item
import pystray
import PIL.Image
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from functools import partial
import os
import subprocess

#隱藏黑窗
CREATE_NO_WINDOW = 0x08000000

class MonitorFrame:
    def __init__(self,MonitorIndex,MonitorList):
        #呼叫生成MonitorString
        self.MonitorIndex=MonitorIndex
        self.MonitorList=MonitorList
        os.system("API\ControlMyMonitor.exe /scomma Cache\monitor"+ str(MonitorIndex) +".txt "+MonitorList[0+6*MonitorIndex][21:])
        file = open('Cache\monitor'+str(MonitorIndex)+'.txt', 'r',encoding="utf-8")
        self.Option=file.readlines()
        file.close()

        #初始化Lists
        self.OptionList={}
        self.inputButton=[]
        self.inputOptions=[]

        #產生OptionList Dict
        for j in range(len(self.Option)):
            self.OptionList[self.Option[j][:2]]=self.Option[j].split(",",5)
        lf=ttk.LabelFrame(controlPanel, text=MonitorList[1+6*MonitorIndex][15:-2])
        lf.pack(fill='x',padx=10,pady=10,ipadx=10,ipady=2)

        #產生inputButton
        if(self.OptionList["60"][5][1:-2]!=""):
            self.inputOptions=self.OptionList["60"][5][1:-2].split(',')
            for j in range(len(self.inputOptions)):
                if(int(self.inputOptions[j])<3):
                    action_with_arg = partial(self.selectInput, self.inputOptions[j])
                    self.inputButton.append(ttk.Button(lf, text="   VGA  ", image = VGAImg, compound=LEFT, width=6, bootstyle="secondary",command=action_with_arg))
                
                elif(int(self.inputOptions[j])<15):
                    action_with_arg = partial(self.selectInput, self.inputOptions[j])
                    self.inputButton.append(ttk.Button(lf, text="   DVI  ", image = DVIImg, compound=LEFT, width=6, bootstyle="secondary",command=action_with_arg))

                elif(int(self.inputOptions[j])<17):
                    action_with_arg = partial(self.selectInput, self.inputOptions[j])
                    self.inputButton.append(ttk.Button(lf, text="   DP   ", image = DPImg, compound=LEFT, width=6, bootstyle="secondary",command=action_with_arg))

                else:
                    action_with_arg = partial(self.selectInput, self.inputOptions[j])
                    self.inputButton.append(ttk.Button(lf, text="  HDMI  ", image = HDMIImg, compound=LEFT, width=6, bootstyle="secondary",command=action_with_arg))
                    
                self.inputButton[j].grid(row=j, column=0, padx=5, pady=3,sticky="w")
        
        ##產生色準調整面板
        if(self.OptionList["16"]!=NULL):
            colorFrame=ttk.LabelFrame(lf, text="RGB色準調整")
            colorFrame.grid(row=0, column=1, padx=5, pady=3,rowspan=2,columnspan=2,sticky=NSEW)
            
            self.scaleR=ttk.Scale(colorFrame, bootstyle="danger", to=100,variable=IntVar,command=self.updateColorLabel)
            self.scaleR.grid(row=0, column=0, padx=5, pady=5)
            self.scaleR.set(int(self.OptionList["16"][3]))

            self.scaleG=ttk.Scale(colorFrame, bootstyle="success", to=100,variable=IntVar,command=self.updateColorLabel)
            self.scaleG.grid(row=0, column=1, padx=5, pady=5)
            self.scaleG.set(int(self.OptionList["18"][3]))

            self.scaleB=ttk.Scale(colorFrame, bootstyle="default", to=100,variable=IntVar,command=self.updateColorLabel)
            self.scaleB.grid(row=1, column=0, padx=5, pady=5)
            self.scaleB.set(int(self.OptionList["1A"][3]))

            setColorBtn=ttk.Button(colorFrame,text="設定顏色",bootstyle="secondary", command=self.setColorGain)
            setColorBtn.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

            self.ColorLabel=ttk.Label(colorFrame, text="R: "+str(int(self.scaleR.get()))+"    G: "+str(int(self.scaleG.get()))+"   B: "+str(int(self.scaleB.get())))
            self.ColorLabel.grid(row=2,column=0,columnspan=2)

        ##產生螢幕亮度調整面板
        if(self.OptionList['10']!=NULL):
            brightnessFrame=ttk.LabelFrame(lf,text="螢幕亮度調整")
            brightnessFrame.grid(row=2, column=1, padx=5, pady=3,columnspan=2,sticky=NSEW)
            self.brightnessScale=ttk.Scale(brightnessFrame, bootstyle="light",to=100,variable=IntVar,command=self.setBrightness, length=200)
            self.brightnessScale.grid(row=0, column=0, padx=5,columnspan=2, pady=5,sticky=N)
            self.brightnessScale.set(int(self.OptionList["10"][3]))



    
    #更新色彩標籤
    def updateColorLabel(self,value):
        self.ColorLabel['text']="R: "+str(int(self.scaleR.get()))+"    G: "+str(int(self.scaleG.get()))+"   B: "+str(int(self.scaleB.get()))

    #調整螢幕色準
    def setColorGain(self):
        subprocess.call("API\ControlMyMonitor.exe /SetValue " + self.MonitorList[0+6*self.MonitorIndex][21:-1] + " 16 "+str(int(self.scaleR.get())), creationflags=CREATE_NO_WINDOW)
        subprocess.call("API\ControlMyMonitor.exe /SetValue " + self.MonitorList[0+6*self.MonitorIndex][21:-1] + " 18 "+str(int(self.scaleG.get())), creationflags=CREATE_NO_WINDOW)
        subprocess.call("API\ControlMyMonitor.exe /SetValue " + self.MonitorList[0+6*self.MonitorIndex][21:-1] + " 1A "+str(int(self.scaleB.get())), creationflags=CREATE_NO_WINDOW)

    def setBrightness(self,brightness):
        subprocess.call("API\ControlMyMonitor.exe /SetValue " + self.MonitorList[0+6*self.MonitorIndex][21:-1] + " 10 "+str(brightness), creationflags=CREATE_NO_WINDOW)

    #切換輸入

    def selectInput(self , inputValue):
        subprocess.call("API\ControlMyMonitor.exe /SetValue " + self.MonitorList[0+6*self.MonitorIndex][21:-1] + " 60 "+inputValue, creationflags=CREATE_NO_WINDOW)




#套用樣式及視窗大小
controlPanel = ttk.Window(themename="cyborg")
controlPanel.resizable(False,False)
controlPanel.minsize(300, 200)

#設定視窗參數
controlPanel.title('OpenMonitorControlPanel v0.4-alpha')
controlPanel.attributes("-alpha", 0.8)
controlPanel.attributes("-topmost", 1)
controlPanel.geometry('-0-35')

#導入圖片
VGAImg = PhotoImage(file = r"img\VGA.png")
HDMIImg = PhotoImage(file = r"img\HDMI.png")
DPImg = PhotoImage(file = r"img\DP.png")
DVIImg = PhotoImage(file = r"img\DVI.png")

#System Tray Code

def quit_window(icon, item):
    icon.stop()
    controlPanel.destroy()

def show_window(icon, item):
    icon.stop()
    controlPanel.after(0,controlPanel.deiconify)

def withdraw_window():  
    controlPanel.withdraw()
    image = PIL.Image.open("img\image.ico")
    menu = (item('退出', quit_window), item('顯示', show_window ,default=True))
    icon = pystray.Icon("name", image, "Open Monitor Control Panel", menu)
    icon.run()

controlPanel.protocol("WM_DELETE_WINDOW", withdraw_window)



    




#掃描螢幕

def scanMonitor():
    subprocess.call("API\ControlMyMonitor.exe /smonitors Cache\smonitors.txt", creationflags=CREATE_NO_WINDOW)
    file = open('Cache\smonitors.txt', 'r',encoding="utf-16 le")

    MonitorList = file.readlines()
    MonitorList[0]=MonitorList[0][1:]
    messagebox.showinfo("掃描完成" , "找到 " + str(len(MonitorList)//6) + " 個螢幕" )
    file.close()
    
    #初始化lists
    Monitors=[]
    

    
    for i in range(len(MonitorList)//6):
        if(len(MonitorList[1+6*i][15:-2])==0):
            Monitors.append('')
            messagebox.showinfo("警告","發現了不支援DDC/CI的螢幕,請檢查您的OSD設定\n"+MonitorList[4+6*i])
        else:
            Monitors.append(MonitorFrame(i,MonitorList))
            print(len(Monitors))
            

#Setup
#refreshButton = ttk.Button(controlPanel, text="更新螢幕清單", bootstyle="default",command=scanMonitor,state='disabled')
#refreshButton.pack(anchor=tk.NE,padx=10,pady=10)

scanMonitor()
controlPanel.mainloop()

