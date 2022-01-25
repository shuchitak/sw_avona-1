# Copyright 2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.
from builtins import range
import sys
import os
import numpy as np
import scipy.io.wavfile
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import subprocess as sub
import xtagctl
import xscope_fileio
import argparse

package_dir = os.path.dirname(os.path.abspath(__file__))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("xe", nargs='?',
                        help=".xe file to run")
    args = parser.parse_args()
    return args


#To convert the wav file
# sox InHouse_VF_222_v1.1_20180903_Loc2_Noise2_70dB__Take1.wav -r 16000 -c 2 -b 32 input.wav trim 0 30 remix 3 4

args = parse_arguments()
# assert args.xe is not None, "Specify vaild .xe file"
if not args.xe:
    args.xe = os.path.join(package_dir, 'bin/test_wav_ic_xcoreai.xe')
#example code to set runtime config in args.bin
# with open("args.bin", "wb") as fp:
#     fp.write("stop_adapting -1\n".encode('utf-8'))
#     fp.write("adaption_mode 0\n".encode('utf-8'))
#     fp.write("main_filter_phases 10\n".encode('utf-8'))
#     fp.write("shadow_filter_phases 5\n".encode('utf-8'))
#     fp.write("y_channels 2\n".encode('utf-8'))
#     fp.write("x_channels 2\n".encode('utf-8'))
#Create an empty args.bin file. xscope_open_file() doesn't handle file not present. Ideally, would like
#to use posix open with O_CREAT flag 
#fp = open("args.bin", "wb")
#fp.close()

with xtagctl.acquire("XCORE-AI-EXPLORER") as adapter_id:
    xscope_fileio.run_on_target(adapter_id, args.xe)



