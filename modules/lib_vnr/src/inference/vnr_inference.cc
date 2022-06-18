// Copyright 2022 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.
#include <stdio.h>
#include <string.h>
#include "inference_engine.h"
#include "vnr_model_data.h"
#include "vnr_inference_api.h"
#include "vnr_inference_priv.h"

// Allocate all memory required by the inference engine
static struct tflite_micro_objects tflmo; // This structure can only be allocated from a C++ file since tflite_micro_objects definition is only visible in C++ files. 
static inference_engine_t ie; 
static vnr_ie_state_t vnr_ie_state;


// TODO: unsure why the stack can not be computed automatically here
#pragma stackfunction 1000
int32_t vnr_inference_init() {
    vnr_ie_state_t *ie_ptr = &vnr_ie_state; 
    auto *resolver = inference_engine_initialize(&ie, (uint32_t *)&ie_ptr->tensor_arena, TENSOR_ARENA_SIZE_BYTES, (uint32_t *) vnr_model_data, vnr_model_data_len, &tflmo);
    // When adding a new operator, refer to lib_tflite_micro/lib_tflite_micro/submodules/tflite-micro/tensorflow/lite/micro/all_ops_resolver.cc for all available add operator functions
    // Make sure XTFLM_OPERATORS defined in xtflm_conf.h is the same as the number of operators added
    resolver->AddConv2D();
    resolver->AddReshape();
    resolver->AddLogistic();
    resolver->AddCustom(tflite::ops::micro::xcore::Conv2D_V2_OpCode,
            tflite::ops::micro::xcore::Register_Conv2D_V2());
    int ret = inference_engine_load_model(&ie, vnr_model_data_len, (uint32_t *) vnr_model_data, 0);

    // Initialise input quant and output dequant parameters
    vnr_priv_init_quant_spec(&ie_ptr->quant_spec);
    return ret;
}



#pragma stackfunction 1000
void vnr_inference(float_s32_t *vnr_output, bfp_s32_t *features) {
    vnr_ie_state_t *ie_state = &vnr_ie_state;
    // Quantise features to 8bit
    vnr_priv_feature_quantise((int8_t *) ie.input_buffers[0], features, &ie_state->quant_spec);
    
    // Inference
    interp_invoke(&ie);

    // Dequantise inference output
    vnr_priv_output_dequantise(vnr_output, (int8_t*)ie.output_buffers[0], &ie_state->quant_spec);
}

