#ifndef __UART_H
#define __UART_H
#include "sys.h"
#include "system.h"

#define USART_TASK_PRIO		3     //Task priority 
#define USART_STK_SIZE 		512   //Task stack size 

/*----------------------------------*/

void uart_init(u32 baudRate);
void usart3_send(u8 data);
int USART3_IRQHandler(void);
void usart_task(void *pvParameters);

extern TimerHandle_t xAutoTimer;
extern uint32_t ledOnTime;

#endif