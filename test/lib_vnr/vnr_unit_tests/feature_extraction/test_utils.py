
import numpy as np
import data_processing.frame_preprocessor as fp
import xscope_fileio
import xtagctl
import os
import tempfile
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../shared/python"))
import py_vs_c_utils as pvc
import scipy.io.wavfile
import math
import tensorflow as tf
import subprocess

def run_dut(input_data, test_name, xe):
    tmp_folder = tempfile.mkdtemp(dir=".", suffix=os.path.basename(test_name))
    prev_path = os.getcwd()
    os.chdir(tmp_folder)
    input_data.astype(np.int32).tofile("input.bin")

    if(os.path.splitext(xe)[-1] == ".xe"): # xcore run
        with xtagctl.acquire("XCORE-AI-EXPLORER") as adapter_id:
            xscope_fileio.run_on_target(adapter_id, xe)
    else: # x86 run
        subprocess.run([xe])
        
    with open("output.bin", "rb") as fdut:
        dut_output = np.fromfile(fdut, dtype=np.int32)
    os.chdir(prev_path)
    os.system("rm -r {}".format(tmp_folder))
    return dut_output

def double_to_int32(x, exp):
    y = x.astype(np.float64) * (2.0 ** -exp)
    y = y.astype(np.int32)
    return y

def int32_to_double(x, exp):
    y = x.astype(np.float64) * (2.0 ** exp)
    return y

def double_to_float_s32(d):
    m,e = math.frexp(d)
    m_int = int(m * (2.0 ** 31))
    e = e-31
    return (m_int, e)

def get_closeness_metric(ref, dut):
    tmp_folder = tempfile.mkdtemp(dir=".")
    prev_path = os.getcwd()
    os.chdir(tmp_folder)
    output_file = "temp.wav"
    output_wav_data = np.zeros((2, len(ref)))
    output_wav_data[0,:] = ref
    output_wav_data[1,:] = dut
    scipy.io.wavfile.write(output_file, 16000, output_wav_data.T)
    arith_closeness, geo_closeness, c_delay, peak2ave = pvc.pcm_closeness_metric(output_file, verbose=False)
    os.chdir(prev_path)
    os.system("rm -r {}".format(tmp_folder))
    return arith_closeness, geo_closeness

def quantise_patch(model_file, this_patch):
    interpreter_tflite = tf.lite.Interpreter(model_path=model_file)
    # Get input and output tensors.
    input_details = interpreter_tflite.get_input_details()[0]
    output_details = interpreter_tflite.get_output_details()[0]
    # quantization spec
    assert(input_details["dtype"] in [np.int8, np.uint8]), "Error: Need 8bit model for quantisation"
    if input_details["dtype"] in [np.int8, np.uint8]:
        input_scale, input_zero_point = input_details["quantization"]
        this_patch = this_patch / input_scale + input_zero_point
        this_patch = np.round(this_patch)
        this_patch = this_patch.astype(input_details["dtype"])
        return this_patch

def dequantise_output(model_file, output_data):
    interpreter_tflite = tf.lite.Interpreter(model_path=model_file)
    output_details = interpreter_tflite.get_output_details()[0]
    assert(output_details["dtype"] in [np.int8, np.uint8]), "Error: Need 8bit model for dequantisation"
    output_scale, output_zero_point = output_details["quantization"]
    output_data = output_data.astype(np.float64)
    output_data = (output_data - output_zero_point)*output_scale
    return output_data

def get_feature_patch_min_limit(model_file):
    interpreter_tflite = tf.lite.Interpreter(model_path=model_file)
    # Get input tensors.
    input_details = interpreter_tflite.get_input_details()[0]
    # quantization spec
    assert (input_details["dtype"] in [np.int8, np.uint8]), "Only 8bit quantised tflite models supported"
    input_scale, input_zero_point = input_details["quantization"]

    # quant output = np.round(this_patch / input_scale + input_zero_point).astype(np.int8)
    # quantisation output is in the range [-128,127]. Find the min and max values before quantisation that lead to -128 and 127 post quantisation
    max_val = (127-input_zero_point)*input_scale
    min_val = (-128-input_zero_point)*input_scale
    print(f"max_val = {max_val}, min_val = {min_val}")
    # We'll only test within input range [min_val, max_val]
    assert(max_val == 0.0), "ERROR: Normalised features always have a max at 0dB"
    min_mant, min_exp = double_to_float_s32(min_val)
    return min_mant, min_exp


