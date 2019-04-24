//
// Created by daran on 1/12/2017 to be used in ECE420 Sp17 for the first time.
// Modified by dwang49 on 1/1/2018 to adapt to Android 7.0 and Shield Tablet updates.
//

#include <jni.h>
#include <algorithm>
#include "ece420_main.h"
#include "ece420_lib.h"
#include "kiss_fft/kiss_fft.h"
#include <iostream>
#include <vector>
#include <cstdlib>
#include <iterator>
#include <complex>
#include <map>
#include <string>

// JNI Function
extern "C" {
JNIEXPORT void JNICALL
Java_com_ece420_lab5_MainActivity_writeNewFreq(JNIEnv *env, jclass, jint);
JNIEXPORT void JNICALL
Java_com_ece420_lab5_MainActivity_writeNewFreq2(JNIEnv *env, jclass, jint);
}

//Dictionary for Notes
std::map<std::string, int> notesFreq = {{"B0",31},{"C1",33},{"C#1",35},{"D1",37},{"D#1",39},{"E1",41},{"F1",44},{"F#1",46},
                                   {"G1",49},{"G#1",52},{"A1",55},{"A#1",58},{"B1",62},{"C2",65},{"C#2",69},{"D2",73},
                                   {"D#2",78},{"E2",82},{"F2",87},{"F#2",93},{"G2",98},{"G#2",104},{"A2",110},{"A#2",117},
                                   {"B2",123},{"C3",131},{"C#3",139},{"D3",147},{"D#3",156},{"E3",165},{"F3",175},{"F#3",185},
                                   {"G3",196},{"G#3",208},{"A3",220},{"A#3",233},{"B3",247},{"C4",262},{"C#4",277},{"D4",294},
                                   {"D#4",311},{"E4",330},{"F4",349},{"F#4",370},{"G4",392},{"G#4",415},{"A4",440},{"A#4",466},
                                   {"B4",494},{"C5",523}};

// Dictionary for Circle of Fifths
std::map<std::string, std::map<std::map<std::string, int>, std::map<std::string, std::string>,std::map<std::string, std::string>>> circleFifths = {{"B0",{{"F",31},{"Next", "F#1"},{"Prev","E4"}}},
{"C1",{{"F",33},{"Next", "G1"},{"Prev", "F4"}}},
{"C#1",{{"F",35},{"Next","G#1"},{"Prev","F#4"}}},
{"D1",{{"F",37},{"Next","A1"},{"Prev","G4"}}},
{"D#1",{{"F",39},{"Next","A#1"},{"Prev","G#4"}}},
{"E1",{{"F",41},{"Next", "B1"},{"Prev","A4"}}},
{"F1",{{"F",44},{"Next", "C2"},{"Prev","A#4"}}},
{"F#1",{{"F",46},{"Next","C#2"},{"Prev","B0"}}},
{"G1",{{"F",49},{"Next","D2"},{"Prev", "C1"}}},
{"G#1",{{"F",52},{"Next","D#2"},{"Prev", "C#1"}}},
{"A1",{{"F", 55},{"Next","E2"},{"Prev","D1"}}},
{"A#1",{{"F",58},{"Next","F2"},{"Prev","D#1"}}},
{"B1",{{"F",62},{"Next","F#2"},{"Prev","E1"}}},
{"C2",{{"F",65},{"Next","G2"},{"Prev","F1"}}},
{"C#2",{{"F",69},{"Next","G#2"},{"Prev","F#1"}}},
{"D2",{{"F",73},{"Next","A2"},{"Prev","G1"}}},
{"D#2",{{"F",78},{"Next","A#2"},{"Prev", "G#1"}}},
{"E2",{{"F",82},{"Next","B2"},{"Prev","A1"}}},
{"F2",{{"F",87},{"Next","C3"},{"Prev","A#1"}}},
{"F#2",{{"F",93},{"Next","C#3"},{"Prev","B1"}}},
{"G2",{{"F",98},{"Next","D3"},{"Prev","C2"}}},
{"G#2",{{"F",104},{"Next","D#3"},{"Prev","C#2"}}},
{"A2",{{"F",110},{"Next","E3"},{"Prev","D2"}}},
{"A#2",{{"F",117},{"Next","F3"},{"Prev","D#2"}}},
{"B2",{{"F",123},{"Next", "F#3"},{"Prev","E2"}}},
{"C3",{{"F",131},{"Next", "G3"},{"Prev", "F2"}}},
{"C#3",{{"F",139},{"Next","G#3"},{"Prev","F#2"}}},
{"D3",{{"F",147},{"Next","A3"},{"Prev","G2"}}},
{"D#3",{{"F",156},{"Next","A#3"},{"Prev","G#2"}}},
{"E3",{{"F",165},{"Next","B3"},{"Prev","A2"}}},
{"F3",{{"F",175},{"Next","C4"},{"Prev","A#2"}}},
{"F#3",{{"F",185},{"Next","C#4"},{"Prev","B2"}}},
{"G3",{{"F",196},{"Next","D4"},{"Prev","C3"}}},
{"G#3",{{"F",208},{"Next", "D#4"},{"Prev","C#3"}}},
{"A3",{{"F",220},{"Next","E4"},{"Prev","D3"}}},
{"A#3",{{"F",233},{"Next","F4"},{"Prev","D#3"}}},
{"B3",{{"F",247},{"Next","F#4"},{"Prev","E3"}}},
{"C4",{{"F",262},{"Next","G4"},{"Prev","F3"}}},
{"C#4",{{"F",277},{"Next","G#4"},{"Prev","F#3"}}},
{"D4",{{"F",294},{"Next","A4"},{"Prev","G3"}}},
{"D#4",{{"F",311},{"Next","A#4"},{"Prev","G#3"}}},
{"E4",{{"F",330},{"Next","B4"},{"Prev","A3"}}},
{"F4",{{"F",349},{"Next","C5"},{"Prev","A#3"}}},
{"F#4",{{"F",370},{"Next","C#1"},{"Prev","B3"}}},
{"G4",{{"F",392},{"Next","D1"},{"Prev","C4"}}},
{"G#4",{{"F",415},{"Next","D#1"},{"Prev","C#4"}}},
{"A4",{{"F",440},{"Next","E1"},{"Prev","D4"}}},
{"A#4",{{"F",466},{"Next","F1"},{"Prev","D#4"}}},
{"B4",{{"F",494},{"Next","F#1"},{"Prev","E4"}}},
{"C5",{{"F",523},{"Next","G1"},{"Prev","F4"}}}};


// Student Variables
#define EPOCH_PEAK_REGION_WIGGLE 30
#define VOICED_THRESHOLD 200000000
#define FRAME_SIZE 1024
#define BUFFER_SIZE (4 * FRAME_SIZE)
#define F_S 48000
float bufferIn[BUFFER_SIZE] = {};
float bufferOut[BUFFER_SIZE] = {};
int newEpochIdx = FRAME_SIZE;

// We have two variables here to ensure that we never change the desired frequency while
// processing a frame. Thread synchronization, etc. Setting to 300 is only an initializer.
int NumFifths = 1;
int NumHarm = 1;
int FREQ_NEW = 300;

bool lab5PitchShift(float *bufferIn) {
    // Lab 4 code is condensed into this function
    int periodLen = detectBufferPeriod(bufferIn);
    float freq = ((float) F_S) / periodLen;

    // If voiced
    if (periodLen > 0) {

        LOGD("Frequency detected: %f\r\n", freq);

        // Epoch detection - this code is written for you, but the principles will be quizzed
        std::vector<int> epochLocations;
        findEpochLocations(epochLocations, bufferIn, periodLen);

        // In this section, you will implement the algorithm given in:
        // https://courses.engr.illinois.edu/ece420/lab5/lab/#buffer-manipulation-algorithm
        //
        // Don't forget about the following functions! API given on the course page.
        //
        // getHanningCoef();
        // findClosestInVector();
        // overlapAndAdd();
        // *********************** START YOUR CODE HERE  **************************** //


        int  new_epoch_spacing = F_S/FREQ_NEW;
        while(newEpochIdx < 2 * FRAME_SIZE){
            int e = findClosestInVector(epochLocations, newEpochIdx, 1, epochLocations.size() - 1);
            int eNext = e + 1;
            int ePrev = e - 1;

            int P_0 = (epochLocations[eNext] - epochLocations[ePrev])/2;
            int winSize = 2 * P_0 + 1;

            float windowedResponse[winSize];
            for(int i =0 ; i < winSize ; i++){
                windowedResponse[i] = 0;

            }
            int j = 0;
            for(int i = epochLocations[e] - P_0 ; i < epochLocations[e] + P_0 + 1 ; i++){
                windowedResponse[j] = bufferIn[i] * getHanningCoef(winSize,j);
                j++;
            }
            overlapAddArray(bufferOut, windowedResponse, newEpochIdx - P_0, winSize);
            newEpochIdx += new_epoch_spacing;
        }





        // ************************ END YOUR CODE HERE  ***************************** //
    }

    // Final bookkeeping, move your new pointer back, because you'll be
    // shifting everything back now in your circular buffer
    newEpochIdx -= FRAME_SIZE;
    if (newEpochIdx < FRAME_SIZE) {
        newEpochIdx = FRAME_SIZE;
    }

    return (periodLen > 0);
}

void ece420ProcessFrame(sample_buf *dataBuf) {
    // Keep in mind, we only have 20ms to process each buffer!
    struct timeval start;
    struct timeval end;
    gettimeofday(&start, NULL);

    // Get the new desired frequency from android
    //FREQ_NEW = FREQ_NEW_ANDROID;

    // Data is encoded in signed PCM-16, little-endian, mono
    int16_t data[FRAME_SIZE];
    for (int i = 0; i < FRAME_SIZE; i++) {
        data[i] = ((uint16_t) dataBuf->buf_[2 * i]) | (((uint16_t) dataBuf->buf_[2 * i + 1]) << 8);
    }

    // Shift our old data back to make room for the new data
    for (int i = 0; i < 2 * FRAME_SIZE; i++) {
        bufferIn[i] = bufferIn[i + FRAME_SIZE - 1];
    }

    // Finally, put in our new data.
    for (int i = 0; i < FRAME_SIZE; i++) {
        bufferIn[i + 2 * FRAME_SIZE - 1] = (float) data[i];
    }

    // The whole kit and kaboodle -- pitch shift
    bool isVoiced = lab5PitchShift(bufferIn);

    if (isVoiced) {
        for (int i = 0; i < FRAME_SIZE; i++) {
            int16_t newVal = (int16_t) bufferOut[i];

            uint8_t lowByte = (uint8_t) (0x00ff & newVal);
            uint8_t highByte = (uint8_t) ((0xff00 & newVal) >> 8);
            dataBuf->buf_[i * 2] = lowByte;
            dataBuf->buf_[i * 2 + 1] = highByte;
        }
    }

    // Very last thing, update your output circular buffer!
    for (int i = 0; i < 2 * FRAME_SIZE; i++) {
        bufferOut[i] = bufferOut[i + FRAME_SIZE - 1];
    }

    for (int i = 0; i < FRAME_SIZE; i++) {
        bufferOut[i + 2 * FRAME_SIZE - 1] = 0;
    }

    gettimeofday(&end, NULL);
    LOGD("Time delay: %ld us",  ((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec)));
}

// Returns lag l that maximizes sum(x[n] x[n-k])
int detectBufferPeriod(float *buffer) {

    float totalPower = 0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
        totalPower += buffer[i] * buffer[i];
    }

    if (totalPower < VOICED_THRESHOLD) {
        return -1;
    }

    int portionLen = BUFFER_SIZE / 4;

    std::vector<float> firstPortion{};
    std::vector<float> thirdPortion{};
    float peak1=-1*INFINITY;
    float peak2=-1*INFINITY;
    for (int i = 0; i<portionLen; i++){
        firstPortion.push_back(buffer[i]);
        if (buffer[i]>peak1)
            peak1=buffer[i];
    }
    for (int i = (BUFFER_SIZE-portionLen); i<BUFFER_SIZE; i++){
        thirdPortion.push_back(buffer[i]);
        if (buffer[i]>peak2)
            peak2=buffer[i];
    }

    float clipping = (float)(.64 * std::min(peak1, peak2));

    // the following loop center clips and infinite clips at the same time
    float clippedFrame[BUFFER_SIZE];
    for (int i = 0; i<BUFFER_SIZE; i++){
        if (buffer[i] > clipping)
            clippedFrame[i] = 1;
        else if (buffer[i] < -clipping)
            clippedFrame[i] = -1;
        else
            clippedFrame[i] = 0;
    }


    // FFT is done using Kiss FFT engine. Remember to free(cfg) on completion
    kiss_fft_cfg cfg = kiss_fft_alloc(BUFFER_SIZE, false, 0, 0);

    kiss_fft_cpx buffer_in[BUFFER_SIZE];
    kiss_fft_cpx buffer_fft[BUFFER_SIZE];

    for (int i = 0; i < BUFFER_SIZE; i++) {
        buffer_in[i].r = clippedFrame[i];
        buffer_in[i].i = 0;
    }

    kiss_fft(cfg, buffer_in, buffer_fft);
    free(cfg);


    // Autocorrelation is given by:
    // autoc = ifft(fft(x) * conj(fft(x))
    //
    // Also, (a + jb) (a - jb) = a^2 + b^2
    kiss_fft_cfg cfg_ifft = kiss_fft_alloc(BUFFER_SIZE, true, 0, 0);

    kiss_fft_cpx multiplied_fft[BUFFER_SIZE];
    kiss_fft_cpx autoc_kiss[BUFFER_SIZE];

    for (int i = 0; i < BUFFER_SIZE; i++) {
        multiplied_fft[i].r = (buffer_fft[i].r * buffer_fft[i].r)
                              + (buffer_fft[i].i * buffer_fft[i].i);
        multiplied_fft[i].i = 0;
    }

    kiss_fft(cfg_ifft, multiplied_fft, autoc_kiss);
    free(cfg_ifft);

    // Move to a normal float array rather than a struct array of r/i components
    std::vector<float> R{};
    int m = 0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if(i == 0){
            m = autoc_kiss[i].r;
        }
        R.push_back(std::abs((autoc_kiss[i].r)/m));
    }

    //float m = R[0];

    //for (int i=0;i<BUFFER_SIZE;i++){
    //    R[i]=std::abs(R[i]/m);
    //}
    //2304
    //960
    //
    int first=(int)(.1 * portionLen);
    int last=(int)(3 * portionLen);
    int ipos=-100000000;
    for (int i=first;i<last+1;i++){
        if (R[i]>ipos)
            ipos=i;
    }

    float retVal = (F_S / ipos);
    if (retVal > 700) {
        return -1;
    }
    FREQ_NEW=(int)((F_S/ipos)*1.5*NumFifths*NumHarm);
    return ipos;

}


void findEpochLocations(std::vector<int> &epochLocations, float *buffer, int periodLen) {
    // This algorithm requires that the epoch locations be pretty well marked

    int largestPeak = findMaxArrayIdx(bufferIn, 0, BUFFER_SIZE);
    epochLocations.push_back(largestPeak);

    // First go right
    int epochCandidateIdx = epochLocations[0] + periodLen;
    while (epochCandidateIdx < BUFFER_SIZE) {
        epochLocations.push_back(epochCandidateIdx);
        epochCandidateIdx += periodLen;
    }

    // Then go left
    epochCandidateIdx = epochLocations[0] - periodLen;
    while (epochCandidateIdx > 0) {
        epochLocations.push_back(epochCandidateIdx);
        epochCandidateIdx -= periodLen;
    }

    // Sort in place so that we can more easily find the period,
    // where period = (epochLocations[t+1] + epochLocations[t-1]) / 2
    std::sort(epochLocations.begin(), epochLocations.end());

    // Finally, just to make sure we have our epochs in the right
    // place, ensure that every epoch mark (sans first/last) sits on a peak
    for (int i = 1; i < epochLocations.size() - 1; i++) {
        int minIdx = epochLocations[i] - EPOCH_PEAK_REGION_WIGGLE;
        int maxIdx = epochLocations[i] + EPOCH_PEAK_REGION_WIGGLE;

        int peakOffset = findMaxArrayIdx(bufferIn, minIdx, maxIdx) - minIdx;
        peakOffset -= EPOCH_PEAK_REGION_WIGGLE;

        epochLocations[i] += peakOffset;
    }
}

void overlapAddArray(float *dest, float *src, int startIdx, int len) {
    int idxLow = startIdx;
    int idxHigh = startIdx + len;

    int padLow = 0;
    int padHigh = 0;
    if (idxLow < 0) {
        padLow = -idxLow;
    }
    if (idxHigh > BUFFER_SIZE) {
        padHigh = BUFFER_SIZE - idxHigh;
    }

    // Finally, reconstruct the buffer
    for (int i = padLow; i < len + padHigh; i++) {
        dest[startIdx + i] += src[i];
    }
}


JNIEXPORT void JNICALL Java_com_ece420_lab5_MainActivity_writeNewFreq(JNIEnv *env, jclass, jint newFreq) {
    NumFifths = (int) newFreq;
    return;
}

JNIEXPORT void JNICALL Java_com_ece420_lab5_MainActivity_writeNewFreq2(JNIEnv *env, jclass, jint newFreq2) {
    NumHarm = (int) newFreq2;
    return;
}