import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

# BAZY

hz_sound = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            65.4, 69.3, 73.4, 77.7, 82.4, 87.3, 92.5, 98, 103.8, 110, 116.5, 123.5,  # wielka
            130.8, 138.6, 146.8, 155.6, 164.8, 174.6, 185, 196, 207.7, 220, 233.1, 246.9,  # mała
            261.6, 277.2, 293.7, 311.1, 329.6, 349.2, 370, 392, 415.3, 440, 466.2, 493.8,  # razkreślna
            523.3, 554.36, 587.3, 622.25, 659.25, 698.5, 739.98, 783.9, 830.6, 880, 932.3, 987.7,  # dwukreślna
            1046.5, 1108.73, 1174.66, 1244.5, 1318.5, 1396.9, 1479.98, 1567.98, 1661.21, 1760, 1864.65,
            1975.53]  # trzykreślna


# SŁOWNIKI

# rhythmic values
time_rythm = [0, 0.25, 0.375, 0.5, 0.75, 1, 1.5, 2, 3, 4]
rythm_sound = ["pauza", "16", "16.", "8", "8.", "4", "4.", "2", "2.", "1"]

rytm = {'wartosc': rythm_sound, 'czas': time_rythm}

# FUNKCJE

# -------------------------------------------------------------------------- SEGMENTATION

def midiRythm_toLily(name, rythm, adr):
    # do opisania metrum - rozpoczęcie, tonacja, etc


    nuty = []
    try:
        for i in range(len(name)):
            if rythm[i] != "pauza":  # jeśli jest różne od pauzy
                nuty.append(name[i] + rythm[i])
    except:
        print('błąd w midirythm to lily')

    # for n in range(len(nuty)):
    # print(nuty[n])


    # add metrum
    metrumm = '4/4'
    # add text to vector - necessary for display and generate notes
    w2 = "\\time"
    ttime = w2[0] + w2[1] + w2[2] + w2[3] + w2[4] + metrumm + " "

    # add tonal
    # to do

    t = 'C'
    k = 'major'

    poczatek = "{" + ttime # + ton_key
    for n in nuty:
        poczatek = poczatek + n + " "

    nuty_opis = poczatek + "}"

    # change the notes so they are the STRING itself, not a list
    nuty_same = " "
    for i in nuty:
        nuty_same = nuty_same + str(i) + " "

    print('\nNotes to generate in program', nuty_opis)
    print('\nOnly notes', nuty_same)
    return nuty_opis, nuty_same

# TEGO nie ma chyba
def midiRythm_toLily_basic(name, rythm, adr):

    nuty = []
    try:
        for i in range(len(name)):
            if rythm[i] != "pauza":  # jeśli jest różne od pauzy
                nuty.append(name[i] + rythm[i])
    except:
        print(' ')

    for n in range(len(nuty)):
        print(nuty[n])

    # dodawanie metrum
    metrumm = " 4/4 "

    w2 = "\\time"
    ttime = w2[0] + w2[1] + w2[2] + w2[3] + w2[4] + metrumm + " "

    # dodawanie tonacji
    # to do
    """
    dane_extractor, dane_extractor_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                                              rhythmStats=['mean', 'stdev'],
                                                              tonalStats=['mean', 'stdev'])(adr)
    t = dane_extractor['tonal.key_edma.key']
    k = dane_extractor['tonal.key_edma.scale']
    """

    t = 'C'
    k = 'major'


    poczatek = "{" + ttime # + ton_key
    for n in nuty:
        poczatek = poczatek + n + " "

    nuty_opis = poczatek + "}"

    # podmieniam nuty, żeby one były jednak samym stringiem, a nie listą
    nuty_same = " "
    for i in nuty:
        nuty_same = nuty_same + str(i) + " "

    return nuty_opis, nuty_same


# -------------------------------------------------------------------------- AFTER SEGMENTATION - MUSICAL ANALYSIS

def nazwy_nutek(numerki_midi, name_sound):
    # get midi numbers and return name sound
    nazwy = []
    for i in range(len(numerki_midi)):
        current = name_sound[numerki_midi[i]]
        nazwy.append(current)
    #print('Dźwięki...', nazwy)
    return nazwy


def Siatka_rytmiczna(slownik):
    # Calculate the lengths of the notes from the click times
    # Put everything into the MAIN DICTIONARY with the notes

    click = slownik['onset_times']
    dlugosci = []

    print('there will be  ', len(click)-2, ' notes')

    for index in range(len(click) - 1):
        el = click[index + 1] - click[index]
        dlugosci.append(el)

    # only for this method I cut off the first 2
    dlugosci.pop(0)

    return dlugosci


def f_to_midi(srednie_wartosci_nut):
    # take the F0 values of the notes and assign them to the nearest (standard) MIDI note frequencies
    # ex. F0 = 436 Hz, it's so close to 440 Hz --> 69 (MIDI)

    # OCTAVE ERRORS FUNCTION!

    numerki_midi = []
    for i in range(len(srednie_wartosci_nut)):

        for number in range(len(hz_sound)):
            fwiecej = round(1.029 * hz_sound[number], 2)
            fmniej = round(hz_sound[number] - (fwiecej - hz_sound[number]), 2)

            if fmniej < srednie_wartosci_nut[i] < fwiecej:
                numerki_midi.append(number)
    #print('\nin midi is...', numerki_midi)

    # --------------------------------------------------------------------------------------- control of octave errors
    # if the sound is more than an octave away from the previous one, change it to the previous octave
    # otherwords - rarely is the distance between notes in sung melodies greater than an octave

    def bledy_oktawowe(numerki_midi):

        start = 1  # so that the distance is okay

        for n in range(start, len(numerki_midi)):
            odleglosc = numerki_midi[n] - numerki_midi[n - 1]
            oktawy = int(odleglosc / 13)

            # octave error, if exist
            if oktawy != 0:
                numer = numerki_midi[n] - oktawy * 12

                numerki_midi[n] = numer
                start = n + 2  # skip one distance so as not to bring the note next to it into the wrong octave

        return numerki_midi

    numerki_midi = bledy_oktawowe(numerki_midi)
    return numerki_midi


def Tonacja(adres):

    # to do
    tonacja = 'C'
    tryb = 'major'

    # names compatible with abjad

    name_Ca = ["", "", "", "", "", "", "", "", "", "", "", "", "",
               "", "", "", "", "", "", "", "", "", "",
               "", "", "", "", "", "", "", "", "", "", "", "", "",
               "c", "cs", "d", "ef", "e", "f", "fs",
               "g", "gs", "a", "bf", "b", # 36-47 wielka #nie ma jej w wiolinowym
               "c", "cs", "d", "ef", "e", "f", "fs",
               "g", "gs", "a", "bf", "b",  # 48- 59 mała
               "c'", "cs'", "d'", "ef'", "e'", "f'", "fs'",
               "g'", "gs'", "a'", "bf'", "b'",  # 60-71 razkreślna
               "c''", "cs''", "d''", "ef''", "e''", "f''", "fs''",
               "g''", "gis''", "a''", "bf''", "b''",
               # 72-83 dwukreślna
               "c'''", "cs'''", "d'''", "ef'''", "e'''", "f'''", "fs'''",
               "g'''", "gs'''", "a'''", "bf'''", "b'''"]  # trzykreślna

    # no #, b
    lily = []
    if tonacja == 'C' and tryb == 'major' or tonacja == 'A' and tryb == 'minor':
        lily = name_Ca

    # place for another tonal with # G, A, D,
    # with b - F, B, Es

    return lily


# -------------------------------------------------------------------------- PO SEGMENTACJI - RYTHM


def Dlugosci_wartosciRytm(dlugosci):
    # take the lengths of the sounds and calculate the rhythmic values
    # TO DO - get the bpm or get the input
    bpm = 120
    wartosc_rytm = []

    for index in range(len(dlugosci)):

        for i in range(len(rytm['czas'])):
            try:
                if rytm['czas'][i] * 60 / bpm < dlugosci[index] < rytm['czas'][i + 1] * 60 / bpm:  # bpm
                    odleglosc1 = dlugosci[index] - rytm['czas'][i]
                    odleglosc2 = rytm['czas'][i + 1] - dlugosci[index]

                    if odleglosc1 < odleglosc2:
                        wartosc_rytm.append(rytm['wartosc'][i])
                        break

                    elif odleglosc1 > odleglosc2:
                        wartosc_rytm.append(rytm['wartosc'][i + 1])
                        break
            except:
                print("error in the calculation of rhythmic values")

    return wartosc_rytm