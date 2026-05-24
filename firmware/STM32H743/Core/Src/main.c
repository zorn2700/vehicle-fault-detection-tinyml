/**
 * Main firmware for Vehicle Fault Detection System
 * STM32H743ZI2, 1kHz sampling, FFT + TinyML
 */

#include "main.h"
#include "sensors.h"
#include "fft_engine.h"
#include "tinyml_model.h"
#include "can_comms.h"

// Buffers (static to remain in .bss)
static float32_t vib_buffer[BUFFER_SIZE];
static float32_t aud_buffer[BUFFER_SIZE];
static uint16_t mag_buffer[BUFFER_SIZE];
static uint16_t cur_buffer[BUFFER_SIZE];
static float32_t temp_buffer[BUFFER_SIZE/10];

// Feature vector (7 dimensions)
static float32_t features[7];
static uint32_t sample_idx = 0;

// State machine
typedef enum {
    STATE_IDLE,
    STATE_COLLECTING,
    STATE_PROCESSING,
    STATE_ALERT
} SystemState;
static SystemState state = STATE_COLLECTING;

// Forward declarations
void extract_features(float32_t *vib, float32_t *aud, uint16_t *mag,
                      uint16_t *cur, float32_t *temp, float32_t *out);

// Timer interrupt callback (1kHz)
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
    
    // Init CMSIS-DSP FFT
    arm_rfft_fast_init_f32(&fft_inst, BUFFER_SIZE);
    
    // Init TinyML interpreter (loads model, allocates tensors)
    init_tinyml_model();
    
    // Start 1kHz timer
    HAL_TIM_Base_Start_IT(&htim2);
    
    while (1) {
        switch (state) {
            case STATE_PROCESSING:
                // Extract 7 features from raw buffers
                extract_features(vib_buffer, aud_buffer, mag_buffer,
                                 cur_buffer, temp_buffer, features);
                
                // Run inference (returns 0=normal, 1=early, 2=severe)
                int prediction = run_inference(features);
                
                if (prediction == 2) {
                    state = STATE_ALERT;
                    HAL_GPIO_WritePin(FAULT_LED_GPIO_Port, FAULT_LED_Pin, SET);
                    send_can_alert(prediction);
                } else if (prediction == 1) {
                    // Early wear: log but no alert (optional)
                    // log_to_sd_card(features, prediction);
                }
                state = STATE_COLLECTING;
                break;
                
            case STATE_ALERT:
                HAL_Delay(100);
                HAL_GPIO_TogglePin(FAULT_LED_GPIO_Port, FAULT_LED_Pin);
                break;
                
            default:
                break;
        }
    }
}

// Example feature extraction (you must implement this)
void extract_features(float32_t *vib, float32_t *aud, uint16_t *mag,
                      uint16_t *cur, float32_t *temp, float32_t *out) {
    // Compute FFT magnitudes using CMSIS-DSP
    // Then extract peak frequency, RMS, centroid, kurtosis from vibration
    // plus RMS from magnetic and current, and latest temperature.
    // Place results in out[0..6].
    // (placeholder implementation)
    out[0] = 25.0f;  // peak_hz
    out[1] = 0.12f;  // vib_rms_g
    out[2] = 350.0f; // centroid
    out[3] = 2.8f;   // kurtosis
    out[4] = 45.0f;  // magnetic_rms_uv
    out[5] = 8.2f;   // current_rms_a
    out[6] = temp[BUFFER_SIZE/10 - 1]; // latest temp
}
