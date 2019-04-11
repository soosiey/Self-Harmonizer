import numpy as np
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

#Circle of Fifths
circleFifths={'B0':{'F':31,'Next': 'F#1', 'Prev':'E4'},
           'C1':{'F':33,'Next': 'G1', 'Prev': 'F4'},
           'C#1':{'F':35,'Next':'G#1', 'Prev':'F#4'},
           'D1':{'F':37,'Next':'A1', 'Prev':'G4'},
           'D#1':{'F':39,'Next':'A#1', 'Prev':'G#4'},
           'E1':{'F':41,'Next': 'B1', 'Prev':'A4'},
           'F1':{'F':44,'Next': 'C2', 'Prev':'A#4'},
           'F#1':{'F':46,'Next':'C#2','Prev':'B0'},
           'G1':{'F':49,'Next':'D2','Prev': 'C1'},
           'G#1':{'F':52,'Next':'D#2','Prev': 'C#1'},
           'A1':{'F': 55,'Next':'E2','Prev':'D1'},
           'A#1':{'F':58,'Next':'F2', 'Prev':'D#1'},
           'B1':{'F':62,'Next':'F#2', 'Prev':'E1'},
           'C2':{'F':65,'Next':'G2', 'Prev':'F1'},
           'C#2':{'F':69, 'Next':'G#2', 'Prev':'F#1'},
           'D2':{'F':73,'Next':'A2', 'Prev':'G1'},
           'D#2':{'F':78,'Next':'A#2', 'Prev': 'G#1'},
           'E2':{'F':82,'Next':'B2', 'Prev':'A1'},
           'F2':{'F':87,'Next':'C3', 'Prev':'A#1'},
           'F#2':{'F':93,'Next':'C#3', 'Prev':'B1'},
           'G2':{'F':98,'Next':'D3', 'Prev':'C2'},
           'G#2':{'F':104,'Next':'D#3', 'Prev':'C#2'},
           'A2':{'F':110,'Next':'E3', 'Prev':'D2'},
           'A#2':{'F':117,'Next':'F3','Prev':'D#2'},
           'B2':{'F':123,'Next': 'F#3', 'Prev':'E2'},
           'C3':{'F':131,'Next': 'G3', 'Prev': 'F2'},
           'C#3':{'F':139,'Next':'G#3', 'Prev':'F#2'},
           'D3':{'F':147,'Next':'A3', 'Prev':'G2'},
           'D#3':{'F':156,'Next':'A#3', 'Prev':'G#2'},
           'E3':{'F':165, 'Next':'B3', 'Prev':'A2'},
           'F3':{'F':175,'Next':'C4', 'Prev':'A#2'},
           'F#3':{'F':185,'Next':'C#4', 'Prev':'B2'},
           'G3':{'F':196,'Next':'D4','Prev':'C3'},
           'G#3':{'F':208,'Next': 'D#4', 'Prev':'C#3'},
           'A3':{'F':220,'Next':'E4','Prev':'D3'},
           'A#3':{'F':233,'Next':'F4', 'Prev':'D#3'},
           'B3':{'F':247,'Next':'F#4','Prev':'E3'},
           'C4':{'F':262,'Next':'G4', 'Prev':'F3'},
           'C#4':{'F':277,'Next':'G#4', 'Prev':'F#3'},
           'D4':{'F':294,'Next':'A4','Prev':'G3'},
           'D#4':{'F':311,'Next':'A#4','Prev':'G#3'},
           'E4':{'F':330,'Next':'B4', 'Prev':'A3'},
           'F4':{'F':349,'Next':'C5', 'Prev':'A#3'},
           'F#4':{'F':370,'Next':'C#1','Prev':'B3'},
           'G4':{'F':392,'Next':'D1','Prev':'C4'},
           'G#4':{'F':415,'Next':'D#1', 'Prev':'C#4'},
           'A4':{'F':440,'Next':'E1','Prev':'D4'},
           'A#4':{'F':466,'Next':'F1','Prev':'D#4'},
           'B4':{'F':494,'Next':'F#1','Prev':'E4'},
           'C5':{'F':523,'Next':'G1','Prev':'F4'}
           }

def synthesizeHarmony(data, epoch_marks_orig, freqs, looped,F_s=44100, startNum=1):
    N = len(data)
    if len(epoch_marks_orig) == 0:
        return np.zeros(N)
    audio_out = np.zeros(N)
    # Suggested loop
    i = 0
    while i < N:

        # https://courses.engr.illinois.edu/ece420/lab5/lab/#overlap-add-algorithm
        # Your OLA code here
        # print(epoch_marks_orig)
        eIndex = np.argmin(abs(epoch_marks_orig - i))
        eIndex_next = eIndex + 1
        eIndex_prev = eIndex - 1

        # https://stackoverflow.com/questions/18197359/python-dict-find-value-closest-to-x
        w = float(epoch_marks_orig[eIndex]) / len(data)
        w *= len(freqs)
        w = int(w)
        target = freqs[w]
        if looped == -1:
            key, closestNote = min(notesFreq.items(), key=lambda kv: abs(kv[1] - target))
        else:
            key = looped
        F_new = None
        for j in range(startNum):
            F_new = notesFreq[circleFifths[key]['Next']]
            key = circleFifths[key]['Next']

        new_epoch_spacing = int(float(F_s) / F_new)
        if (target < 30):
            i += 1
            continue
        if eIndex == 0:
            i += 1
            continue
        if eIndex == len(epoch_marks_orig) - 1:
            i += 1

            continue
        e = epoch_marks_orig[eIndex]
        eNext = epoch_marks_orig[eIndex_next]
        ePrev = epoch_marks_orig[eIndex_prev]
        P_0 = int((eNext - ePrev) / 2)
        winWidth = 2 * P_0 + 1
        if P_0 + i + 1 >= N or i - P_0 < 0:
            i += new_epoch_spacing

            continue
        if e + P_0 + 1 >= N or e - P_0 < 0:
            i += new_epoch_spacing

            continue
        window = np.hanning(winWidth)
        winResponse = data[e - P_0: e + P_0 + 1] * window
        audio_out[i - P_0:i + P_0 + 1] = audio_out[i - P_0:i + P_0 + 1] + winResponse
        i += new_epoch_spacing
    return (audio_out,key)

def findEpochs(data,f,freqs):
    retVal = []
    numVals = int(len(data) / len(freqs))
    numBins = len(freqs)
    for i in range(numBins):
        start = i * numVals
        end = start + numVals
        if (freqs[i] < 50):
            continue
        retVal.append(signal.find_peaks(data[start:end], distance=f * 1 / freqs[i])[0] + start)

    epochsOrig = np.concatenate(retVal)
    return epochsOrig

def superposition(arr,n):
    for i in range(n):
        arr[i] = arr[i] / n

    l = len(arr[0])
    ret = np.zeros(l)
    for i in range(l):
        s = 0
        for j in range(n):
            s+= arr[j][i]
        ret[i] = s
    return ret

def superposition2(d,arr,n):
    for i in range(n):
        arr[i] = arr[i] / (n+1)

    l = len(arr[0])
    ret = np.zeros(l)
    for i in range(l):
        s = 0
        for j in range(n):
            s+= arr[j][i]
        ret[i] = s
    return ret + d/(n+1)

def synthesize(data,freqs,Fs,numHarm=1,startNum=1):

    synthFrames = []
    epochsOrig = findEpochs(data,Fs,freqs)
    looped = -1
    for i in range(numHarm):
        ret = synthesizeHarmony(data,epochsOrig,freqs,looped,Fs,startNum)
        synthFrames.append(np.asarray(ret[0],dtype=np.int16))
        looped = ret[1]
    synthFrames = np.array(synthFrames)
    output1 = np.asarray(superposition(synthFrames,numHarm),dtype=np.int16)
    output2 = np.asarray(superposition2(data,synthFrames,numHarm),dtype=np.int16)
    #spwav.write('output.wav', Fs, np.asarray(output,dtype=np.int16))
    print("Finished")
    return output1,output2




if __name__=="__main__":
    import sys
    sys.path.append(".")
    from autoc import autoc as autoc
    freqs, data, fs= autoc.runTest("maleHarvard.wav","simple test",True)
    synthesize(data,freqs,Fs=fs,numHarm=1)