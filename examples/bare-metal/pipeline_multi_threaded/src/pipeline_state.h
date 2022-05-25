#ifndef AP_STAGE_A_STATE_H
#define AP_STAGE_A_STATE_H

#include "pipeline_config.h"
#include "xs3_math.h"

typedef struct {
    float_s32_t max_ref_energy;
    float_s32_t aec_corr_factor[AP_MAX_Y_CHANNELS];
    int32_t vad_flag;
    int32_t ref_active_flag;
    int32_t vnr_pred_flag;
}pipeline_metadata_t;

#endif
