import numpy as np
import scipy.io.wavfile as spwav
import scipy.signal as signal
import matplotlib.pyplot as plt

# Remember to pass in the full data into the following function so that
# we can output the full audio file

def synthesizeHarmony(data, epoch_marks_orig, freq, F_s=44100, startNum=1, numHarmonies=1):
    N=len(data)
    closestFreq=196.00
    F_new=startNum*1.5*closestFreq
    new_epoch_spacing = int(float(F_s) / F_new)
    audio_out = np.zeros(N)

    # Suggested loop
    for i in range(0, N, new_epoch_spacing):

        # https://courses.engr.illinois.edu/ece420/lab5/lab/#overlap-add-algorithm
        # Your OLA code here

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
    # first=True
    for i in range(rate, len(data) - (2*rate), rate):
        start = i - rate
        end = i + (2*rate)
        if i + frame_size >= len(data):
            end = len(data)
        frame=data[start:end]
        epochsOrig=findEpochs(frame)
        # if first:
        #     epochVals=np.zeros(len(epochsOrig))
        #     plt.figure()
        #     plt.plot(frame)
        #     for e in range(len(epochsOrig)):
        #         epochVals[e]=frame[epochsOrig[e]]
        #     plt.scatter(epochsOrig,epochVals,marker='o',c='red')
        #     plt.show()
        #     first=False
        synthesizeHarmony(frame,epochsOrig,freqs[count])
        count+=1




if __name__=="__main__":
    import sys
    sys.path.append(".")
    from autoc import autoc as autoc
    freqs, data =autoc.runTest("test_vector.wav","simple test")
    runBaseTest(data,freqs,Fs=44100)