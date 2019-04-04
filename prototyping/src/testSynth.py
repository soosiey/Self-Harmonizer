import synth.synth as synth

RUN_BASE_TEST = True
freqs = []
dataArr = []

if RUN_BASE_TEST:
    f,d = autoc.runBaseTest()
    freqs.append(f)
    dataArr.append(d)

TEST_FILE_NAMES = ['Test_Vector_Rajan.wav']
TEST_FILE_DESCRIPTORS = ['Rajan Voice']

if len(TEST_FILE_NAMES) != len(TEST_FILE_DESCRIPTORS):
    print("The number of names and descriptors must match!")

for filename,descriptor in zip(TEST_FILE_NAMES,TEST_FILE_DESCRIPTORS):
    f,d = synth.runTest(filename,freqs)
    freqs.append(f)
    dataArr.append(d)
