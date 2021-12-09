from tkinter import *
from seg_librosa import *
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
#import abjad

# from matplotlib.widgets import Cursor
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# from seg_manual import *

# import auto_py_to_exe

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024


#######################################        FUNCTION         #########################################

# --------------------------------------------------- OKNO 1 - MAIN

def recording():
    print('to do')
    # to do


def wybieram_seg2():
    # tutaj ogarrniam zaznaczanie segmentacji
    # to do z essentią

    seg_manual()


def wybieram_seg3():
    print('Segmentation with librosa')

    slownik = seg_librosa()




def _quit():
    window.quit()
    window.destroy()


# ====================================      MAIN WINDOW     ===========================================

window = Tk()

# kolory przycisków
tpcolor = '#283655'
tpcolor_kliknij = '#212c45'
bgcolor2 = '#7A0008'
fgcolor = '#b3cde0'

top = Toplevel()
window.title("main")
window.geometry("740x200")
window.configure(bg=tpcolor)

# ===========================================   FRAME    ===============================================

frame_title = Frame(master=window, width=40, height=120, bg=tpcolor)
frame_title.pack()

frame1 = Frame(master=window, width=700, height=120, bg=tpcolor)
frame1.pack()

# frame_wyniki = Frame(master=window, width=700, height=400, bg=tpcolor)
# frame_wyniki.pack()

frame_button = Frame(window, bg=tpcolor)
frame_button.pack(side=BOTTOM)

# ============================================ BUTTON =========================================================

label_title = Label(frame_title, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 14), pady=10, text='\n[tytuł]',
                    justify=CENTER)
label_title.pack()

btns_nagraj = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10,
                     text='TO DO - RECORD YOUR MELODY', command=recording)
btns_nagraj.grid(row=1, column=0, padx=25, pady=20)

# --------------------------------------------- seg 2 -------------------------------------------------------------

btns2 = Button(frame1, bg=tpcolor, fg=fgcolor, font=("Times New Roman", 10), pady=10,
               text='TO DO - SEGMENTATION MANUAL ',
               command=wybieram_seg2)
btns2.grid(row=1, column=2, padx=10, pady=20)


btns3 = Button(frame1, bg=tpcolor_kliknij, fg=fgcolor, font=("Times New Roman", 10), pady=10,
               text=' SEGMENTATION AUTOMATICAL ', command=wybieram_seg3)
btns3.grid(row=1, column=1, padx=15, pady=20)


window.mainloop()