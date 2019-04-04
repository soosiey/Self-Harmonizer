import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import scipy.signal as signal
from numpy.fft import fft, ifft

TEST_DIR = '../../testFiles/'

def processFrame(frame, Fs):
    portionlen = int(len(frame)/4) # 4
    firstPortion = frame[:portionlen]
    thirdPortion = frame[3 * portionlen:] #5
    peak1 = np.amax(firstPortion)
    peak2 = np.amax(thirdPortion)
    clipping = .64 * min(peak1,peak2)

    # the following loop center clips and infinite clips at the same time
    clippedFrame = frame
    for i in range(len(clippedFrame)):
        if clippedFrame[i] > clipping:
            clippedFrame[i] = 1
        elif clippedFrame[i] < -clipping:
            clippedFrame[i] = -1
        else:
            clippedFrame[i] = 0

    R = ifft(fft(clippedFrame) * np.conj(fft(clippedFrame)))
    R = np.abs(R)
    m = R[0]

    R /= m


    ipos = np.argmax(R[int(.2 * portionlen):int(3 * portionlen)]) #6
    ipos += int(.2 * portionlen)
    ival = R[ipos]

    return Fs/ipos if ival > .3 else 0


def dataControl(data, Fs,test):
    frame_size = int(Fs * .04) #1
    fn = Fs * 2
    crit = 900 / fn
    b, a = signal.butter(4, crit)
    filteredSignal = signal.lfilter(b, a, data)
    rate = int(frame_size / 4) #2
    numFrames = len(filteredSignal) / rate
    numFrames = int(numFrames)
    frequencies = np.zeros(numFrames)
    cnt = 0
    thresh = (1.0 / 15.0) * np.amax(filteredSignal)
    for i in range(rate, len(filteredSignal) - (2*rate), rate):

        start = i - rate
        end = i + (2*rate) # 3
        if i + frame_size >= len(filteredSignal):
            end = len(filteredSignal)
        frame = filteredSignal[start: end]
        if np.amax(frame) < thresh:
            frequencies[cnt] = 0
        else:
            frequencies[cnt] = processFrame(frame.astype(float), Fs)
        cnt += 1

    if len(frequencies) > 1000:
        frequencies = frequencies[:1000]
    plt.plot(frequencies)
    plt.axis('tight')
    plt.xlabel('Frame idx')
    plt.ylabel('Hz')
    plt.title('Detected Frequencies in Hz (' + str(frame_size) + ' length frames) for ' + test)
    plt.show()
    return frequencies

def simpleVector():
    Fs, data = read(TEST_DIR + 'test_vector.wav')
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    plt.figure(figsize=(10, 20))
    return dataControl(data,Fs, 'simple voice'),data


def otherVector(fname,descriptor='other sample'):
    Fs, data = read(TEST_DIR + fname)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    plt.figure(figsize=(10, 20))
    return dataControl(data, Fs, descriptor),data


def runBaseTest():
    return simpleVector()

def runTest(fname,descriptor):
    return otherVector(fname,descriptor)

if __name__ == '__main__':

    freqs = runBaseTest()
    TEST_DIR = '../../testFiles'
    print(freqs)