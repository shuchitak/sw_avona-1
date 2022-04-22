#ifndef __VNR_INFERENCE_API_H__
#define __VNR_INFERENCE_API_H__

#include "vnr_inference_state.h"

void vnr_inference_init(vnr_ie_t *ie_ptr);
void vnr_inference(vnr_ie_t *ie_ptr, int8_t *vnr_output);
#endif