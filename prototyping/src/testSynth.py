import synth.synth as synth
import autoc.autoc as autoc
import scipy.io.wavfile as spwav


testFile = 'test_vector.wav'

freqs, data, fs = autoc.runTest(testFile,"simple test",True)

noInputSynth,inputSynth = synth.synthesize(data,freqs,fs,numHarm=1,startNum=2)

spwav.write('SynthWithoutInput.wav',fs,noInputSynth)
spwav.write('SynthWithInput.wav',fs,inputSynth)
