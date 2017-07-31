from Tkinter import *
import tkFileDialog
import oop_gen_config
import os
import platform
import subprocess
from pathlib import Path

# for mac app when bundled
baseDir = Path(os.getcwd()).parents[2]

ipv4Path = ""
ipv6Path = ""

def get_file(type):

  if (type=='ipv4'):
    global ipv4Path
    ipv4Path = tkFileDialog.askopenfilename(initialdir = baseDir)
    if ipv4Path != "":
     generate_4.configure(state=NORMAL)
     ipv4Label.config(text=ipv4Path)

  elif (type == 'ipv6'):
    global ipv6Path
    ipv6Path = tkFileDialog.askopenfilename(initialdir = baseDir)

    if ipv6Path != "":
      generate_6.configure(state=NORMAL)
      ipv6Label.config(text=ipv6Path)

def create_config(type):
  if type == 4:
    ipv4 = oop_gen_config.Config(4, ipv4Path)
    ipv4.generate_config()
    if ipv4.success:
      messageLog.configure(state=NORMAL)
      messageLog.insert(END, "Generated IPv4 config files in " + ipv4.get_path() +  "files" + "\n")
      messageLog.configure(state=DISABLED)
      open_folder_btn.configure(state=NORMAL)
  else:
    ipv6 = oop_gen_config.Config(6, ipv6Path)
    ipv6.generate_config()
    if ipv6.success:
      messageLog.configure(state=NORMAL)
      messageLog.insert(END, "Generated IPv6 config files in " + ipv6.get_path() + "files/" + "\n")
      messageLog.configure(state=DISABLED)
      open_folder_btn.configure(state=NORMAL)
    #ipv6.generate_config()
  
def open_folder():
  files_folder = str(baseDir) + "/files"
  if os.path.isdir(files_folder):
    if platform.system() == "Windows":
        os.startfile(files_folder)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", files_folder])
    else:
        subprocess.Popen(["xdg-open", files_folder])

root = Tk()

choose4Button = Button(text='Browse IPv4 List', relief = GROOVE, width=15, command= lambda: get_file('ipv4'))
choose4Button.grid(row=0, column=0, pady = 15, padx=20, sticky=EW)
choose6Button = Button(text='Browse IPv6 List', relief = GROOVE, width=15, command= lambda: get_file('ipv6'))
choose6Button.grid(row=1, column=0, pady = 15, padx=20, sticky=EW)
ipv4Label = Label(text='. . .', relief = SUNKEN, width=50)
ipv4Label.grid(row=0, column=1, padx=20)
ipv6Label = Label(text='. . .', relief = SUNKEN, width=50)
ipv6Label.grid(row=1, column=1, padx=20)

generate_4 = Button(text='Generate ipv4 Config', relief=GROOVE, width=20, state=DISABLED, command= lambda: create_config(4))
generate_4.grid(row=0, column = 2, pady = 15, padx=10)

generate_6 = Button(text='Generate ipv6 config', relief=GROOVE, width=20, state=DISABLED, command = lambda: create_config(6))
generate_6.grid(row=1, column = 2, pady = 15, padx=10)

messageLog = Text(relief = SUNKEN, width=80, height = 4, 
                        highlightbackground = '#ffffff',
                        highlightcolor = "#7baedc",
                        bg='#ffffff', borderwidth = 1, )
messageLog.configure(state=DISABLED)
messageLog.grid(row=3, column=0, pady = 15, padx=20, columnspan=3, sticky=EW)

open_folder_btn = Button(text='Open Folder', command = open_folder, state=DISABLED)
open_folder_btn.grid(row=4, column = 0, sticky=W, padx= 20)
#root.grid_columnconfigure(0, weight=1)
root.title("Generate Configuration Files")
root.geometry('1000x250')
mainloop()
