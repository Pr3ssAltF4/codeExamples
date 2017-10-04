/*
 * adc.h
 *
 *  Created on: May 5, 2017
 *      Author: ixt7265
 */

#ifndef ADC_H_
#define ADC_H_

#include <unistd.h>
#include <stdio.h>
#include <stdint.h>       /* for uintptr_t */
#include <hw/inout.h>     /* for in*() and out*() functions */
#include <sys/neutrino.h> /* for ThreadCtl() */
#include <sys/mman.h>     /* for mmap_device_io() */

// Defines
#define BASE (0x280)
#define GPIO_A_ADDRESS ( 0x288 )
#define GPIO_B_ADDRESS ( 0x289 )
#define GPIO_CONTROL_ADDRESS ( 0x28B )
#define DATA_READY (0x01)
#define DATA_NOT_READY (0x00)

// Function prototypes
void gpio_setup(void);
void adc_setup(void);
void check_adc(void);
int check_adc_status(void);

#endif /* ADC_H_ */
