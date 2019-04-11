import synth.synth as synth
import autoc.autoc as autoc
import scipy.io.wavfile as spwav


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

noInputSynth,inputSynth = synth.synthesize(data,freqs,fs,numHarm,startNum)

spwav.write('SynthWithoutInput.wav',fs,noInputSynth)
spwav.write('SynthWithInput.wav',fs,inputSynth)
