import synth.synth as synth
import autoc.autoc as autoc
import scipy.io.wavfile as spwav


testFile = 'test_vector.wav'

freqs, data, fs = autoc.runTest(testFile,"simple test",True)

sFrames,newFreqs = synth.synthesize(data,freqs,fs,numHarm=1,startNum=2)

o1 = np.asarray(synth.superposition(sFrames,numHarm),dtype=np.int16)
o2 = np.asarray(synth.superposition2(data,sFrames,numHarm),dtype=np.int16)
spwav.write('SynthWithoutInput.wav',fs,noInputSynth)
spwav.write('SynthWithInput.wav',fs,inputSynth)
