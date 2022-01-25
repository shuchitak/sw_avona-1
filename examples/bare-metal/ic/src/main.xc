// Copyright 2021 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <platform.h>
#include <xs1.h>
#include <xscope.h>
#include <stdlib.h>
#ifdef __XC__
#define chanend_t chanend
#else
#include <xcore/chanend.h>
#endif

extern "C" {
#include "xs3_math.h"
void main_tile0(chanend, chanend);
void main_tile1(chanend);
}

#ifndef BURN_THREADS
#define BURN_THREADS    0 //If set to 1, all other threads on IC tile will run, simulating fully loaded system
#endif

void burn_div() {
    unsafe {
    while(1) {
        float_s32_t a, b, c;
        a = double_to_float_s32(5.678765);
        b = double_to_float_s32(3.5667);
        volatile float_s32_t * unsafe p = &c;
        for(int i=0; i<32; i++) {
            *p = float_s32_div(b, a);
            b = *p;
        }
    }
    }
}

int main (void)
{
  chan c_cross_tile, xscope_chan;
  par
  {
#if TEST_WAV_XSCOPE
    xscope_host_data(xscope_chan);
#endif
    on tile[0]: {
        par {
            #if BURN_THREADS
            par(int t=0; t<8-1; t++) {
                {
                    set_core_fast_mode_on();
                    burn_div();
                }
            }
            #endif
            {
            main_tile0(c_cross_tile, xscope_chan);
            _Exit(0);
            }
        }
    }
    on tile[1]: main_tile1(c_cross_tile);
  }
  return 0;
}
