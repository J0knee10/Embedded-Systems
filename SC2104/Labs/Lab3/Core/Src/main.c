/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "MPU6050.h"
#include <math.h>
#include <stdio.h>
#include <string.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c2;
IMU_Data imu1;
UART_HandleTypeDef huart3;

/* USER CODE BEGIN PV */
// Complementary filter variables
float compRoll = 0, compPitch = 0;
float alpha_comp = 0.98f;

// Kalman filter variables for Roll
float kalmanRoll = 0; // This will be x_est_gyro
float kalmanUncertaintyRoll = 4; // Initial σ_est_gyro^2
// Kalman filter variables for Pitch
float kalmanPitch = 0; // This will be x_est_gyro for pitch
float kalmanUncertaintyPitch = 4; // Initial σ_est_gyro^2

const float var_acc = 9; // σ_acc^2
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C2_Init(void);
static void MX_USART3_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	char sbuf[10];

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C2_Init();
  MX_USART3_UART_Init();
  /* USER CODE BEGIN 2 */
  // (optional) If you want to explicitly set the address here:
  IMU_ADDR = 0x68 << 1;   // only if it's not already set in MPU6050.c

  // Initialise the IMU
  uint8_t *status = IMU_Initialise(&imu1, &hi2c2, &huart3);
  if (status != 0) {
      // Error string is inside 'status'; you can send it to UART
      HAL_UART_Transmit(&huart3, status, strlen((char*)status), HAL_MAX_DELAY);
      while (1);  // Stop here
  }
  // Gyro variables
  float gyroRoll = 0, gyroPitch = 0, gyroYaw = 0;
  static uint32_t millisOld = 0;
  // Low-pass filter variables
  static float accX_filtered = 0;
  static float accY_filtered = 0;
  static float accZ_filtered = 0;
  float alpha = 0.1f;  // filter coefficient (0 < alpha < 1)

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, GPIO_PIN_SET);

	  // Read IMU
	  IMU_AccelRead(&imu1);
	  IMU_GyroRead(&imu1);
	  char newline[] = "\r\n";

	  // Accelerometer XYZ
	  for (int i = 0; i < 3; i++){
		  sprintf(sbuf, "%5.2f, ", imu1.acc[i]);
		  HAL_UART_Transmit(&huart3, sbuf, strlen(sbuf), HAL_MAX_DELAY);
	  }


	  // Apply low-pass filter
	  accX_filtered = alpha * imu1.acc[0] + (1 - alpha) * accX_filtered;
	  accY_filtered = alpha * imu1.acc[1] + (1 - alpha) * accY_filtered;
	  accZ_filtered = alpha * imu1.acc[2] + (1 - alpha) * accZ_filtered;

//	  // Acce Roll and pitch w/o filter
//	  float roll  = atan2f(imu1.acc[1], imu1.acc[2]) * (180.0f / M_PI);
//	  float pitch = atan2f(-imu1.acc[0], sqrtf(imu1.acc[1]*imu1.acc[1] + imu1.acc[2]*imu1.acc[2])) * (180.0f / M_PI);

	  // Acce Roll and pitch with filter
	  float pitch = atan2f(-accX_filtered, sqrtf(accY_filtered*accY_filtered + accZ_filtered*accZ_filtered)) * (180.0f / M_PI);
	  float roll  = atan2f(accY_filtered, accZ_filtered) * (180.0f / M_PI);

	  sprintf(sbuf, "%5.2f, %5.2f, ", roll, pitch);
	  HAL_UART_Transmit(&huart3, sbuf, strlen(sbuf), HAL_MAX_DELAY);



	  // Gyro XYZ
	  for (int i = 0; i < 3; i++){
		  sprintf(sbuf, "%5.2f, ", imu1.gyro[i]);
		  HAL_UART_Transmit(&huart3, sbuf, strlen(sbuf), HAL_MAX_DELAY);
	  }

	  // Time elapsed for gyro integration
	  uint32_t millisNow = HAL_GetTick();
	  float dt = (millisOld == 0) ? 0.01f : (millisNow - millisOld) * 0.001f; // in seconds
	  millisOld = millisNow;


	  // Gyro roll pitch yaw integration (degrees/s * dt = degrees)
	  gyroRoll  += imu1.gyro[0] * dt;
	  gyroPitch += imu1.gyro[1] * dt;
	  gyroYaw   += imu1.gyro[2] * dt;
	  sprintf(sbuf, "%5.2f, %5.2f, %5.2f, ", gyroRoll, gyroPitch, gyroYaw);
	  HAL_UART_Transmit(&huart3, (uint8_t*)sbuf, strlen(sbuf), HAL_MAX_DELAY);


	  /* --- Complementary Filter Implementation --- */
	  // compRoll and compPitch are Θ[n-1]
	  // imu1.gyro[0] is ωG[n] for roll
	  // roll is ΘA[n] for roll
	  compPitch = alpha_comp * (compPitch + imu1.gyro[0] * dt) + (1 - alpha_comp) * imu1.acc[0];
	  compRoll = alpha_comp * (compRoll + imu1.gyro[1] * dt) + (1 - alpha_comp) * imu1.acc[1];
	  sprintf(sbuf, "%5.2f, %5.2f, ", compRoll, compPitch);
	  HAL_UART_Transmit(&huart3, (uint8_t*)sbuf, strlen(sbuf), HAL_MAX_DELAY);


	  /* --- Kalman Filter Implementation --- */ //KALMAN FILTER HAS ERRORS
	  // --- Roll ---
	  // Prediction step (based on gyro)
	  kalmanRoll += imu1.gyro[1] * dt; // x_est_gyro at n based on n-1

	  // Update step (correction based on accelerometer)
	  float KG_roll = kalmanUncertaintyRoll / (kalmanUncertaintyRoll + var_acc);
	  kalmanRoll = kalmanRoll + KG_roll * (roll - kalmanRoll);
	  kalmanUncertaintyRoll = (1 - KG_roll) * kalmanUncertaintyRoll;

	  // --- Pitch ---
	  // Prediction step (based on gyro)
	  kalmanPitch += imu1.gyro[0] * dt; // x_est_gyro at n based on n-1

	  // Update step (correction based on accelerometer)
	  float KG_pitch = kalmanUncertaintyPitch / (kalmanUncertaintyPitch + var_acc);
	  kalmanPitch = kalmanPitch + KG_pitch * (pitch - kalmanPitch);
	  kalmanUncertaintyPitch = (1 - KG_pitch) * kalmanUncertaintyPitch;
	  sprintf(sbuf, "%5.2f, %5.2f, ", kalmanRoll, kalmanPitch);
	  HAL_UART_Transmit(&huart3, (uint8_t*)sbuf, strlen(sbuf), HAL_MAX_DELAY);


	  HAL_UART_Transmit(&huart3, (uint8_t*)newline,
	  	                        strlen(newline), HAL_MAX_DELAY);
	  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, GPIO_PIN_RESET);

	  // Optional slowing down the reading
	  HAL_Delay(100);

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C2_Init(void)
{

  /* USER CODE BEGIN I2C2_Init 0 */

  /* USER CODE END I2C2_Init 0 */

  /* USER CODE BEGIN I2C2_Init 1 */

  /* USER CODE END I2C2_Init 1 */
  hi2c2.Instance = I2C2;
  hi2c2.Init.ClockSpeed = 100000;
  hi2c2.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c2.Init.OwnAddress1 = 0;
  hi2c2.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c2.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c2.Init.OwnAddress2 = 0;
  hi2c2.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c2.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C2_Init 2 */

  /* USER CODE END I2C2_Init 2 */

}

/**
  * @brief USART3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 115200;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */

  /* USER CODE END USART3_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LED3_GPIO_Port, LED3_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : PB12 */
  GPIO_InitStruct.Pin = GPIO_PIN_12;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : LED3_Pin */
  GPIO_InitStruct.Pin = LED3_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LED3_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
