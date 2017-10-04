#ifndef __GPIO_H
#define __GPIO_H

// Includes
#include "stm32l476xx.h"
#include <stdint.h>

// Defines
#define BUFFER_SIZE (0x20)
#define PRESCALER (7999)
#define RESET_BYTE (0x00000000)
#define TRUE (1)
#define FALSE (0)

// Function Declarations
void setup_gpio(void);
uint8_t read_pins(void);

#endif // __GPIO_H