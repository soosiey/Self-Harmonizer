import synth.synth as synth
import autoc.autoc as autoc
import scipy.io.wavfile as spwav
import numpy as np
import matplotlib.pyplot as plt


testFile = input('What is the test file called? Make sure the file is in the testFiles folder.\n')
plot = input('Would you like to see the plot of the frequencies?(y/n)\n')

if(plot == 'y'):
    plot = True
elif(plot == 'n'):
    plot = False
else:
    print("Please type y or n")
    exit(0)
freqs, data, fs = autoc.runTest(testFile,"simple test",plot)

numHarm = int(input('What is the number of harmonies you would like to hear?\n'))
startNum = int(input('How many fifths would you like to space out each harmony?\n'))

outputSynths, newFreqs = synth.synthesize(data,freqs,fs,numHarm,startNum)
o1 = np.asarray(synth.superposition(outputSynths,numHarm),dtype=np.int16)
o2 = np.asarray(synth.superposition2(data,outputSynths,numHarm),dtype=np.int16)

spwav.write('SynthWithoutInput.wav',fs,o1)
spwav.write('SynthWithInput.wav',fs,o2)

print("Superposition finished, written to files")


plt.figure(figsize=(10,20))
cnt = 0
for i in newFreqs:
    plt.plot(i,color='red',label = str(cnt))
    cnt += 1


plt.plot(freqs,color='blue',label='Original')
plt.xlabel('Frame Idx')
plt.ylabel('Frequency')
plt.title('Frequencies of Harmonies of Original Input')
plt.legend()
plt.show()

