/**
 * Main firmware for Vehicle Fault Detection System
 * STM32H743ZI2, 1kHz sampling, FFT + TinyML
 */

#include "main.h"
#include "sensors.h"
#include "fft_engine.h"
#include "tinyml_model.h"
#include "can_comms.h"

static float32_t vib_buffer[BUFFER_SIZE];
static float32_t aud_buffer[BUFFER_SIZE];
static uint16_t mag_buffer[BUFFER_SIZE];
static uint16_t cur_buffer[BUFFER_SIZE];
static float32_t temp_buffer[BUFFER_SIZE/10];

static float32_t features[7];
static uint32_t sample_idx = 0;

typedef enum {
    STATE_IDLE,
    STATE_COLLECTING,
    STATE_PROCESSING,
    STATE_ALERT
} SystemState;
static SystemState state = STATE_COLLECTING;

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        vib_buffer[sample_idx] = read_vibration_x();
        aud_buffer[sample_idx] = read_audio_pressure();
        mag_buffer[sample_idx] = read_magnetic_field();
        cur_buffer[sample_idx] = read_current_ina219();
        
        if (sample_idx % 10 == 0) {
            temp_buffer[sample_idx/10] = read_temperature_mlx();
        }
        
        sample_idx++;
        if (sample_idx >= BUFFER_SIZE) {
            sample_idx = 0;
            state = STATE_PROCESSING;
        }
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_SPI1_Init();
    MX_I2C1_Init();
    MX_I2S3_Init();
    MX_CAN_Init();
    MX_DMA_Init();
    MX_TIM2_Init();
    
    arm_rfft_fast_init_f32(&fft_inst, BUFFER_SIZE);
    init_tinyml_model();
    
    HAL_TIM_Base_Start_IT(&htim2);
    
    while (1) {
        switch (state) {
            case STATE_PROCESSING:
                extract_features(vib_buffer, aud_buffer, mag_buffer,
                                 cur_buffer, temp_buffer, features);
                int prediction = run_inference(features);
                
                if (prediction == 2) {
                    state = STATE_ALERT;
                    HAL_GPIO_WritePin(FAULT_LED_GPIO_Port, FAULT_LED_Pin, SET);
                    send_can_alert(prediction);
                } else if (prediction == 1) {
                    // log only
                }
                state = STATE_COLLECTING;
                break;
                
            case STATE_ALERT:
                HAL_Delay(100);
                HAL_GPIO_TogglePin(FAULT_LED_GPIO_Port, FAULT_LED_Pin);
                break;
                
            default: break;
        }
    }
}
