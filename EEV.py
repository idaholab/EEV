# Copyright 2026, Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED

############# Modify As Needed
CPEfinderDictPath = "CPEfinder/CPE_Dictionary.csv"
WAVgraphDB = "neo4j"
dbUser = "neo4j"
dbPass = "????"
##############################

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import os
from stix2validator import validate_file, print_results, ValidationOptions
import shutil
import time
from datetime import datetime

programPath = '.' + os.sep
selectedFilename = ''

def enforceButton():
   #Check if checkboxes selected
   if enforceChecker.get() == 0:
        #Rename Checker Folder to _Checker
        try:
            os.rename("./STIXEnforcer/Checkers", "./STIXEnforcer/DISABLED_Checkers")
        except:
            pass
   else:
        #Rename Checker Folder to Checker
        try:
            os.rename("./STIXEnforcer/DISABLED_Checkers", "./STIXEnforcer/Checkers")
        except:
            pass
        
   if enforceFixer.get() == 0:
        #Rename Fixer Folder to _Fixer
        try:
            os.rename("./STIXEnforcer/Fixers", "./STIXEnforcer/DISABLED_Fixers")
        except:
            pass
   else:
        #Rename Fixer Folder to Fixer
        try:
            os.rename("./STIXEnforcer/DISABLED_Fixers", "./STIXEnforcer/Fixers")
        except:
            pass
        
   if enforceHolder.get() == 0:
        #Rename Holder Folder to _Holder
        try:
            os.rename("./STIXEnforcer/Holders", "./STIXEnforcer/DISABLED_Holders")
        except:
            pass
   else:
        #Rename Holder Folder to Holder
        try:
            os.rename("./STIXEnforcer/DISABLED_Holders", "./STIXEnforcer/Holders")
        except:
            pass
        
   ############
   ## Run STIX Enforcer
   statusBox.delete(1.0, END)
   statusBox.insert(END, "Running Enforcer...")
   root.update()
   
   os.system('python3 STIXEnforcer/STIX_Enforcer.py ' + " \"" + selectedFilename + "\" \"" + selectedFilename + "\"")
   
   statusBox.delete(1.0, END)
   statusBox.insert(END, "Enforcer Completed")
   print("Enforcer Completed")
   print("------------------------------------------")
   print()
   #########
        
def validateButton():
   ## Run Validator
   statusBox.delete(1.0, END)
   statusBox.insert(END, "Running Validator...")
   root.update()
   
   options = ValidationOptions(version="2.1")
   results = validate_file(selectedFilename, options)
   if results.is_valid:
        statusBox.delete(1.0, END)
        statusBox.insert(END, "Valid STIX Bundle")
        print_results(results)
        print("Validation Complete - VALID")
        print("------------------------------------------")
        print()
   else:
        statusBox.delete(1.0, END)
        statusBox.insert(END, "Invalid STIX Bundle")
        print_results(results)
        print("Validation Complete - INVALID")
        print("------------------------------------------")
        print()
   
def enrichButton():
   #Clear statusBox
   statusBox.delete(1.0, END)
   statusBox.insert(END, "Enrich")
   
   #Check if checkboxes selected
   if enrichWAVgraph.get() == 1:
        #########
        ## Run WAVgraphEnricher
        statusBox.delete(1.0, END)
        statusBox.insert(END, "Running WAVgraphEnricher...")
        print("Running WAVgraphEnricher...")
        root.update()
        
        os.system('python3 WAVgraphEnricher/WAVgraphEnricher.py ' + WAVgraphDB + " " + dbUser + " " + dbPass + " \"" + selectedFilename + "\" \"" + selectedFilename + "\"")
        
        statusBox.delete(1.0, END)
        statusBox.insert(END, "WAVgraphEnricher Completed")
        print("WAVgraphEnricher Completed")
        print("------------------------------------------")
        print()
        #########
        
   if enrichCPEfinder.get() == 1:
        #########
        ## Run CPE Finder
        statusBox.delete(1.0, END)
        statusBox.insert(END, "Running CPEfinder...")
        root.update()
        
        os.system('python3 CPEfinder/CPE_Finder_EVE.py ' + CPEfinderDictPath + " \"" + selectedFilename + "\" \"" + selectedFilename + "\"")
        
        statusBox.delete(1.0, END)
        statusBox.insert(END, "CPEfinder Completed")
        print("CPEfinder Completed")
        print("------------------------------------------")
        print()
        #########

def CPEfinderDictPathSettingButton():
   statusBox.delete(1.0, END)
   global CPEfinderDictPath
   temp = CPEfinderDictPath
   CPEfinderDictPath = simpledialog.askstring(title = "CPE Dictionary CSV Path", prompt = "Enter CPE Dictionary CSV Path\t\t\t\t\t\t", initialvalue=CPEfinderDictPath)
   if not CPEfinderDictPath:
       CPEfinderDictPath = temp
   statusBox.insert(END, "CPE Dictionary CSV Path: " + CPEfinderDictPath)
      
def WAVgraphDBSettingButton():
   statusBox.delete(1.0, END)
   global WAVgraphDB
   temp = WAVgraphDB
   WAVgraphDB = simpledialog.askstring(title = "DB Name", prompt = "Enter DB Name\t\t\t\t\t\t", initialvalue=WAVgraphDB)
   if not WAVgraphDB:
       WAVgraphDB = temp
   statusBox.insert(END, "DB Name: " + WAVgraphDB)
   
def dbUserSettingButton():
   statusBox.delete(1.0, END)
   global dbUser
   temp = dbUser
   dbUser = simpledialog.askstring(title = "DB Username", prompt = "Enter DB Username\t\t\t\t\t\t", initialvalue=dbUser)
   if not dbUser:
       dbUser = temp
   statusBox.insert(END, "DB Username: " + dbUser)
   
def dbPassSettingButton():
   statusBox.delete(1.0, END)
   global dbPass
   temp = dbPass
   dbPass = simpledialog.askstring(title = "DB Password", prompt = "Enter DB Password\t\t\t\t\t\t", initialvalue=dbPass)
   if not dbPass:
       dbPass = temp
   statusBox.insert(END, "DB Password: " + dbPass)
   
def fileSelectButton():
   statusBox.delete(1.0, END)
   global selectedFilename
   selectedFilename =  filedialog.askopenfilename(initialdir = programPath,title = "Select STIX Bundle")
   fileSelectedLabelText.set(selectedFilename)
   
   #Backup Bundle on Select
   date_time = datetime.fromtimestamp(time.time())
   str_date_time = date_time.strftime("%d-%m-%Y_%H:%M:%S")
   outputFilename = selectedFilename.split('.json')[0] + ".json__Backup_" + str_date_time + ".json"
   shutil.copyfile(selectedFilename, outputFilename)
   
   #Check for Zero size files
   ##############################################
   while os.path.getsize(selectedFilename) <= 0:
       print("Zero-byte file detected. Please select a different file.")
       selectedFilename =  filedialog.askopenfilename(initialdir = programPath,title = "Select STIX Bundle")
    
   statusBox.insert(END, "Loaded " + selectedFilename)
   
   enforceButton["state"] = "normal"
   checkerButton["state"] = "normal"
   fixerButton["state"] = "normal"
   holderButton["state"] = "normal"
   validateButton["state"] = "normal"
   enrichButton["state"] = "normal"
   wavgraphButton["state"] = "normal"
   cpefinderButton["state"] = "normal"
   
#############Initialization###################
root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="WAVgraph: DB Name...", command=WAVgraphDBSettingButton)
filemenu.add_command(label="WAVgraph: DB Username...", command=dbUserSettingButton)
filemenu.add_command(label="WAVgraph: DB Password...", command=dbPassSettingButton)
filemenu.add_command(label="CPEfinder: CPE Dictionary CSV Path...", command=CPEfinderDictPathSettingButton)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Settings", menu=filemenu)

root.configure(width=40, menu=menubar)
root.title("EEV (Enrich Enforce Validate)")
root.geometry("400x340")
root.resizable(0, 0)

myCanvas = Canvas(root)
myCanvas.pack()
myCanvas.create_line(70, 60, 70, 170, 70, 170, 120, 170, fill="#476042", width=3, arrow=LAST)
myCanvas.create_line(150, 160, 150, 250, 150, 250, 200, 250, fill="#476042", width=3, arrow=LAST)

myCanvas.create_line(0, 45, 400, 45, fill="#476042", width=1)

EEVLogo = PhotoImage(file="EEV.png")
EEVLogoLabel = Label(root, image=EEVLogo)
EEVLogoLabel.place(x=10,y=210)

EEVLogoLabel = Label(root, text="EEV", font=("Arial", 20))
EEVLogoLabel.place(x=75,y=255)

buttonText = StringVar()
buttonText.set('STIX Bundle...')
fileSelectButton = Button(root, textvariable=buttonText, command=fileSelectButton)
fileSelectButton.place(x=10,y=10)

fileSelectedLabelText = StringVar()
fileSelectedLabel = Entry(root,textvariable=fileSelectedLabelText,bd=0,bg='#D9D9D9',width=32)
fileSelectedLabel.place(x=130,y=15)

enforceButton = Button(root,text="Enforce",command=enforceButton, width=15, height=3)
enforceButton.place(x=130,y=140)
enforceButton["state"] = "disabled"

enforceChecker = IntVar()   
enforceFixer = IntVar()   
enforceHolder = IntVar() 
checkerButton = Checkbutton(root, text = "Checkers",  
                      variable = enforceChecker, 
                      onvalue = 1, 
                      offvalue = 0, 
                      height = 1, 
                      width = 10) 
checkerButton.place(x=289, y=135)
checkerButton.select()
checkerButton["state"] = "disabled"
  
fixerButton = Checkbutton(root, text = "Fixers", 
                      variable = enforceFixer, 
                      onvalue = 1, 
                      offvalue = 0, 
                      height = 1, 
                      width = 10) 
fixerButton.place(x=280, y=155)
fixerButton.select()
fixerButton["state"] = "disabled"
  
holderButton = Checkbutton(root, text = "Holders", 
                      variable = enforceHolder, 
                      onvalue = 1, 
                      offvalue = 0, 
                      height = 1, 
                      width = 10)
holderButton.place(x=285, y=175)
holderButton["state"] = "disabled"

validateButton = Button(root,text="Validate",command=validateButton, width=15, height=3)
validateButton.place(x=210,y=220)
validateButton["state"] = "disabled"

enrichButton = Button(root,text="Enrich",command=enrichButton, width=15, height=3)
enrichButton.place(x=50,y=60)
enrichButton["state"] = "disabled"

enrichWAVgraph = IntVar()   
enrichCPEfinder = IntVar()
wavgraphButton = Checkbutton(root, text = "WAVgraph", 
                      variable = enrichWAVgraph, 
                      onvalue = 1, 
                      offvalue = 0, 
                      height = 1, 
                      width = 10) 
wavgraphButton.place(x=209, y=65)
wavgraphButton.select()
wavgraphButton["state"] = "disabled"

cpefinderButton = Checkbutton(root, text = "CPEfinder", 
                      variable = enrichCPEfinder, 
                      onvalue = 1, 
                      offvalue = 0, 
                      height = 1, 
                      width = 10) 
cpefinderButton.place(x=206, y=85)
cpefinderButton.select()
cpefinderButton["state"] = "disabled"

statusBox = Text(root, width=45, height=1, padx=5, pady=5, borderwidth=2)
statusBox.place(x=10, y= 300)

statusBox.insert(END,'Status')


root.mainloop()

