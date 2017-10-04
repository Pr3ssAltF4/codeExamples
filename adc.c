/*
 * adc.c
 *
 *  Created on: May 5, 2017
 *      Author: Zack Teasdale, Ian Taylor
 */

#include "adc.h"

// GPIO variables
uintptr_t ctrl_handle;
uintptr_t data_handle_a;
uintptr_t data_handle_b;

// GPIO setup
void gpio_setup(void){
	int permission_err;
	// Setup GPIO
	permission_err = ThreadCtl(_NTO_TCTL_IO, NULL);
	if(permission_err == -1){
		fprintf(stderr, "Can't get root permissions\n");
		return;
	}

	// Map handle for control register, data register, and setup data register for output
	ctrl_handle = mmap_device_io(1, GPIO_CONTROL_ADDRESS);
	out8(ctrl_handle, 0x00);
	data_handle_a = mmap_device_io(1, GPIO_A_ADDRESS);
	data_handle_b = mmap_device_io(1, GPIO_B_ADDRESS);
}

// ADC setup
void adc_setup(void){
	// set input channel to channel 1
	out8(BASE+2, 0x11);
	// set input range to +/- 10V with resolution 305uV and gain of 1
	out8(BASE+3, 0x00);
	// set polarity to bipolar
	out8(BASE+1, 2);
	out8(BASE+13, 0x00);

}

void check_adc(void){
	uint8_t AD_LSB;
	uint8_t AD_MSB;

	// Actually capture into ADC
	// wait for analog input circuit to settle
	while(in8(BASE+3) & 0x20); // wait for ADWAIT to go low,BASE+3 bit 5

	// perform a/d conversion on current channel
	out8(BASE, 0x80);

	// wait for conversion to finish
	//while(in8(BASE+3) & 0x80); // wait for ADBUSY to go low,BASE+3 bit 7
	check_adc_status();

	// read data from the board
	AD_LSB = in8(BASE);
	AD_MSB = in8(BASE+1);
	//ad = (int16_t) ((AD_MSB * 256) + AD_LSB);
	//ad = AD_MSB;
	//ad_out = ad >> 8;
	// send data out via port A and port B
	// A is MSByte, B is LSByte
	if(AD_MSB < 128) {
		out8(data_handle_a, (127 + (AD_MSB)));
		printf("%d\n", (127 + (AD_MSB)));
	} else {
		out8(data_handle_a, (AD_MSB) - 127);
		printf("%d\n", (AD_MSB) - 127);
	}

}

	// OR USE
	int check_adc_status(void){
		int i;
		for (i = 0; i < 20000; i++)
			if(!(in8(BASE+3) & 0x80)) return(0);	// conversion completed
		return(-1);									// conversion did not complete
	}
