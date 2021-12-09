import librosa
import librosa.display
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor
from functions import *


def seg_manual():
    print('Segmentation with graph')
    adres = filedialog.askopenfilename(title="wybierz plik seg2",
                                       filetypes=(("wav mono files", ".wav"), ("all files", "*.*")))

    y, sr = librosa.load(adres)
    x = np.linspace(0.0, len(y) / 44100.0, len(y))

    print('You probably also have to mark the end of the last note!')

    fig, ax = plt.subplots()
    plt.plot(x, y)

    cursor = Cursor(ax, horizOn=False, vertOn=True, color='green')

    click_draw = []

    def click(event):
        x1, y1 = event.xdata, event.ydata
        print(round(x1, 3))
        click_draw.append(x1)

    fig.canvas.mpl_connect('button_press_event', click)
    plt.show()

    # print('Number of click', len(click_draw))
    # print('Clicks', click_draw)

    # main dictionary
    nutyLib = {}
    # click draw to dictionary
    nutyLib['onset_times'] = click_draw
    # calculate
    nutyLib['dlugosci'] = Siatka_rytmiczna(nutyLib)
    # rythm values
    nutyLib['rythmLily'] = Dlugosci_wartosciRytm(nutyLib['dlugosci'])  # szesnatska, 0.25
    print('Rythm values of melody will be:  ', nutyLib['rythmLily'])

    print('\n!!!!!!\nIn this place the F0 values of the notes will be calculated\n!!!!!!\n')

    nuty_hz = []

    # to do function to get F0 of note

    """
    nutyLib['nameLily'] = estimate_pitch_and_generate_sine(y, nutyLib['onset_boundaries'], sr=sr)

    # first element
    nutyLib['nameLily'].pop(0)

    nutyLib['midi'] = f_to_midi(nutyLib['nameLily'])
    nutyLib['nameLily'] = nazwy_nutek(nutyLib['midi'], name_sound)
    nutyLib['generate_opis'], nutyLib['generate'] = midiRythm_toLily(nutyLib['nameLily'], nutyLib['rythmLily'],
                                                                     audio_file)
    """

# seg_manual()
