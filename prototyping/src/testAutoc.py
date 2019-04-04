import autoc.autoc as autoc

RUN_BASE_TEST = True

if RUN_BASE_TEST:
    autoc.runBaseTest()


TEST_FILE_NAMES = ['Test_Vector_Rajan.wav',
                   'sin300hz.wav',
                   'sin1000hz.wav',
                   'maleHarvard.wav',
                   'femaleHarvard.wav',
                   'obamaSOU.wav'
                   ]
TEST_FILE_DESCRIPTORS = ['Rajan Voice',
                         'Pure Sine 300 Hz Tone',
                         'Pure Sine 1000 Hz Tone',
                         'Male Test Data from OSR',
                         'Female Test Data from OSR',
                         'First 10 seconds of Obama 2010 State of the Union']

if len(TEST_FILE_NAMES) != len(TEST_FILE_DESCRIPTORS):
    print("The number of names and descriptors must match!")

for filename,descriptor in zip(TEST_FILE_NAMES,TEST_FILE_DESCRIPTORS):
    autoc.runTest(filename,descriptor)
