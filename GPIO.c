/* GPIO ports to use
Bit#		:	7		6		5		4		3		2		1		0
GPIO ports 	:	PA0		PA5		PE10	PE11	PE12	PE13	PE14	PE15

PE8 is data-ready bit ???
*/

#include "GPIO.h"
#include "pwm.h"

// Setting up the aforementioned pins for GPIO input.
void setup_gpio() {

	// General GPIOA Enable
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOBEN ;
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOEEN ;

	// Set all GPIO Ports to input mode (00)
	GPIOB->MODER &= RESET_BYTE;
	GPIOE->MODER &= RESET_BYTE;
	
}

// Reads the pins. PE10-15 and PA0/5 , in order from lowest to highest, into a byte.
uint8_t read_pins() {
	//uint8_t buffer [20] ;
	int bits_e
		, bits_b3
		, bits_b2;
	int i, n, input;

	
	bits_e = (GPIOE->IDR & 0xFC00) >> 10;
	
	bits_b3 = ((GPIOB->IDR & 0x0008) >> 3) * 64; // Grab PA0 and PA5.
	bits_b2 = ((GPIOB->IDR & 0x0004) >> 2) * 128; // Grab PA0 and PA5.
	
	input = bits_e + bits_b3 + bits_b2;
	set_servo_position(input);
	//n = sprintf(buffer, "%d\r\n", input);
	//USART_Write(USART2, buffer, n) ;
	
	return input;

}
