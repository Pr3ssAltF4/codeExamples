#include <stdlib.h>
#include "adc.h"

int main(int argc, char *argv[]) {
	// Setup GPIO
	gpio_setup();

	// Setup ADC
	adc_setup();

	// Infinite loop to continuously check ADC value
	// and write value out to port A
	while(1){ check_adc(); }
	return EXIT_SUCCESS;
}
