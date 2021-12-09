import librosa.util
import librosa, librosa.display
from functions import *
# import abjad


# is for displaying a pdf of the sheet music and playing a melody

# Segmentation, which is based on signal amplitude analysis
# 1. New function is created, which analyses changes in the energy of the signal
# 2. Maxima of the function are interpreted as the beginnings of a note
# 3. Data are packed into a dictionary, played and displayed

# * it is worth emphasizing the beginnings of the sounds,
# it highlights the changes and classifies the beginnings of the sounds


def seg_librosa():
    audio_file = filedialog.askopenfilename(title="Wybierz plik",
                                            filetypes=(("wav mono files", ".wav"), ("all files", "*.*")))

    y, sr = librosa.load(audio_file)
    name_sound = Tonacja(audio_file)

    # main dictionary
    nutyLib = {}

    # when notes start - when peaks is
    hop_length = 256  # 100 - 300
    nutyLib['onset_env'] = librosa.onset.onset_strength(y, sr=sr, hop_length=hop_length)

    nutyLib['onset_samples'] = librosa.onset.onset_detect(y, sr=sr, units='samples',
                                                          hop_length=hop_length, backtrack=False,
                                                          pre_max=20, post_max=20,
                                                          pre_avg=100, post_avg=100,  # 100 100
                                                          delta=0.05, wait=0)  # 0.1

    # sample, but with boundaries
    nutyLib['onset_boundaries'] = np.concatenate([[0], nutyLib['onset_samples'], [len(y)]])

    # "clicks"
    nutyLib['onset_times'] = librosa.samples_to_time(nutyLib['onset_boundaries'], sr=sr)

    plt.subplot(211)
    plt.plot(nutyLib['onset_env'])
    plt.ylabel('The power of energy', fontsize=13)
    plt.xlabel('Number of samples', fontsize=13)
    plt.title('New function')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlim(0, len(nutyLib['onset_env']))

    plt.subplot(212)
    librosa.display.waveplot(y)
    plt.vlines(nutyLib['onset_times'], -0.5, 0.5, color='#973333')
    plt.ylabel('Amplitude', fontsize=13)
    plt.xlabel('Time [s]', fontsize=13)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.ylim(-0.5, 0.5)
    plt.show()

    # pitch
    def estimate_pitch(segment, sr, fmin=50.0, fmax=2000.0):
        r = librosa.autocorrelate(segment)

        # zakres auto
        i_min = sr / fmax
        i_max = sr / fmin

        # append, del
        r[:int(i_min)] = 0
        r[int(i_max):] = 0

        # max
        i = r.argmax()
        f0 = float(sr) / i
        return f0

    def estimate_pitch_and_generate_sine(y, onset_samples, sr):
        for i in range(len(nutyLib['onset_boundaries']) - 1):
            n0 = onset_samples[i]
            n1 = onset_samples[i + 1]
            f0 = estimate_pitch(y[n0:n1], sr)
            nuty_hz.append(f0)

        return nuty_hz

    nuty_hz = []
    nutyLib['nameLily'] = estimate_pitch_and_generate_sine(y, nutyLib['onset_boundaries'], sr=sr)


    # first element
    nutyLib['nameLily'].pop(0)

    nutyLib['midi'] = f_to_midi(nutyLib['nameLily'])
    nutyLib['nameLily'] = nazwy_nutek(nutyLib['midi'], name_sound)

    nutyLib['dlugosci'] = Siatka_rytmiczna(nutyLib)

    nutyLib['rythmLily'] = Dlugosci_wartosciRytm(nutyLib['dlugosci'])  # szesnatska, 0.25

    nutyLib['generate_opis'], nutyLib['generate'] = midiRythm_toLily(nutyLib['nameLily'], nutyLib['rythmLily'],
                                                                     audio_file)

    # ------------------------------------------------- DO WYNIKÓW -----------------------------------------------------

    # same nuty
    # abjad
    """
    voice_1 = abjad.Voice(nutyLib['generate'], name="Voice_1")

    staff_1 = abjad.Staff([voice_1], name="Staff_1")

    abjad.show(staff_1)
    abjad.play(voice_1)
    print('Notes in text: ', nutyLib['generate'])
    print('\nskopiuj i generuj', nutyLib['generate_opis'])
    """
    return nutyLib

# seg_librosa()
