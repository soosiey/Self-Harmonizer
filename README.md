# Self-Harmonizer

This is an android application to harmonize with a voice. The main usage of the app is that a harmonic or key may be selected, and a number of voices to harmonize with may be selected. Then, when singing into the application, the harmonies will be superpositioned and output to the user.

# Prototyping

The prototyping is done in Python, the source code is in the prototyping/src folder. The input signal is put through the modified autocorrelation with clipping method to determine if there is a voice being input, and then it will be sent through a TD-PSOLA algorithm to synthesize various harmonies. These will be superpositioned and and output.

Prototyping is now finished. To run the system, go into prototyping/src/ and run the runSystem.py script. Follow the instructions on the console.
# Android Application

TBD


~
