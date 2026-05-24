#ifndef __MAIN_H
#define __MAIN_H

#include "stm32h7xx_hal.h"
#include <stdint.h>
#include <stdbool.h>

#define BUFFER_SIZE 256
#define SAMPLE_RATE_HZ 1000

extern TIM_HandleTypeDef htim2;
extern SPI_HandleTypeDef hspi1;
extern I2C_HandleTypeDef hi2c1;
extern I2C_HandleTypeDef hi2c2;
extern I2S_HandleTypeDef hi2s3;
extern CAN_HandleTypeDef hcan;

void SystemClock_Config(void);
void MX_GPIO_Init(void);
void MX_SPI1_Init(void);
void MX_I2C1_Init(void);
void MX_I2S3_Init(void);
void MX_CAN_Init(void);
void MX_DMA_Init(void);
void MX_TIM2_Init(void);

#endif
