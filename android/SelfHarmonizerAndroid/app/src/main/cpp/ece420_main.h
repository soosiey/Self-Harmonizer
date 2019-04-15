//
// Created by daran on 1/12/2017 to be used in ECE420 Sp17 for the first time.
// Modified by dwang49 on 1/1/2018 to adapt to Android 7.0 and Shield Tablet updates.
//

#ifndef ECE420_MAIN_H
#define ECE420_MAIN_H

#include "audio_common.h"
#include "buf_manager.h"
#include "debug_utils.h"

int detectBufferPeriod(float *buffer);
void findEpochLocations(std::vector<int> &epochLocations, float *buffer, int periodLen);
void overlapAddArray(float *dest, float *src, int startIdx, int len);
bool lab5PitchShift(float *bufferIn);
void ece420ProcessFrame(sample_buf *dataBuf);

#endif //ECE420_MAIN_H
