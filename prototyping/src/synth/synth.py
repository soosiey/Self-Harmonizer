import numpy as np
import scipy.io.wavfile as spwav
import scipy.signal as signal
import matplotlib.pyplot as plt

# Remember to pass in the full data into the following function so that
# we can output the full audio file

#Dictionary for Notes (30 Hz to 500 Hz)
notesFreq={'B0':31,'C1':33,'C#1':35,'D1':37,'D#1':39,'E1':41,'F1':44,'F#1':46,'G1':49,'G#1':52,'A1':55,'A#1':58,
           'B1':62,'C2':65,'C#2':69,'D2':73,'D#2':78,'E2':82,'F2':87,'F#2':93,'G2':98,'G#2':104,'A2':110,'A#2':117,
           'B2':123,'C3':131,'C#3':139,'D3':147,'D#3':156,'E3':165,'F3':175,'F#3':185,'G3':196,'G#3':208,'A3':220,'A#3':233,
           'B3':247,'C4':262,'C#4':277,'D4':294,'D#4':311,'E4':330,'F4':349,'F#4':370,'G4':392,'G#4':415,'A4':440,'A#4':466,
           'B4':494,'C5':523}

def synthesizeHarmony(data, epoch_marks_orig, freq, F_s=44100, startNum=1):
    N=len(data)
    if len(epoch_marks_orig)==0:
        return np.zeros(N)
    #https://stackoverflow.com/questions/18197359/python-dict-find-value-closest-to-x
    target = freq
    key, closestFreq = min(notesFreq.items(), key=lambda kv: abs(kv[1] - target))

    F_new=startNum*1.5*closestFreq
    new_epoch_spacing = int(float(F_s) / F_new)
    audio_out = np.zeros(N)

    # Suggested loop
    for i in range(0, N, new_epoch_spacing):

        # https://courses.engr.illinois.edu/ece420/lab5/lab/#overlap-add-algorithm
        # Your OLA code here
        #print(epoch_marks_orig)
        eIndex = np.argmin(abs(epoch_marks_orig - i))
        eIndex_next = eIndex + 1
        eIndex_prev = eIndex - 1
        if eIndex == 0:
            continue
        if eIndex == len(epoch_marks_orig) - 1:
            continue
        e = epoch_marks_orig[eIndex]
        eNext = epoch_marks_orig[eIndex_next]
        ePrev = epoch_marks_orig[eIndex_prev]

        P_0 = int((eNext - ePrev) / 2)
        winWidth = 2 * P_0 + 1
        window = np.hanning(winWidth)
        winResponse = data[e - P_0: e + P_0 + 1] * window
        audio_out[i - P_0:i + P_0 + 1] = audio_out[i - P_0:i + P_0 + 1] + winResponse
    return audio_out

def findEpochs(data):
    epochsOrig=signal.find_peaks(data,threshold=550,distance=55)
    return epochsOrig[0]

def runBaseTest(data,freqs,Fs):

    frame_size = int(Fs * .04)
    rate = int(frame_size / 4)
    numFrames = int(len(data) / rate)
    count=0
    first=True
    for i in range(rate, len(data) - (2*rate), rate):
        start = i - rate
        end = i + (2*rate)
        if i + frame_size >= len(data):
            end = len(data)
        frame=data[start:end]
        epochsOrig=findEpochs(frame)
        if first:
            epochVals=np.zeros(len(epochsOrig))
            plt.figure()
            plt.plot(frame)
            for e in range(len(epochsOrig)):
                epochVals[e]=frame[epochsOrig[e]]
            plt.scatter(epochsOrig,epochVals,marker='o',c='red')
            plt.show()
            first=False
        #print(epochsOrig)
        synthesized=synthesizeHarmony(frame,epochsOrig,freqs[count])
        plt.figure()
        plt.plot(synthesized)
        plt.plot(freqs)
        plt.show()
        count+=1




if __name__=="__main__":
    import sys
    sys.path.append(".")
    from autoc import autoc as autoc
    freqs, data =autoc.runTest("test_vector.wav","simple test")
    runBaseTest(data,freqs,Fs=44100)