/* Author = Ian Taylor & Zack Teasdale
 * Date : 5.4.17
 * SWEN 563 Project 4 main file.
 */


// Imports
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "SysClock.h"
#include "pwm.h"
#include "UART.h"
#include "LED.h"
#include "GPIO.h"


// Defines
#define BUFFER_SIZE (0x20)


// Globals
//uint8_t buffer [BUFFER_SIZE] ;


// Function Declarations
static void move_servo(int new_position);
static void pause_servo(void);
static void resume_servo(void);
static void test_board(void);
static uint8_t decode(void);


// Function Definitions

// Moves servo to new position.
static void move_servo(int new_position) { set_servo_position(new_position); }

// Pauses the servo. Stops the pwm signal generation.
static void pause_servo() { stop_pwm(); }

// Resumes the servo. Restarts the pwm signal generation.
static void resume_servo() { start_pwm(); }

// Tests the LED's to make sure we can manage the board.
static void test_board() {

	wait(10);
	Green_LED_Off();
	Red_LED_Off();
	wait(10);
	Green_LED_Off();
	Red_LED_On();
	wait(10);
	Green_LED_On();
	Red_LED_Off();
	wait(10);
	Green_LED_Off();
	Red_LED_Off();
	wait(10);
	Green_LED_On();
	Red_LED_On();
	wait(10);
	Green_LED_Off();
	Red_LED_Off();
	wait(10);

}

// Main function
int main(void) {
	uint8_t buffer [BUFFER_SIZE] ;
	int n;
	uint8_t input;
	
	// Init for sys clock and UART.
	System_Clock_Init() ;
	UART2_Init() ;
	LED_Init();
	setup_gpio();

	//n = sprintf(buffer, "We're working boys!\r\n") ;
	//USART_Write(USART2, buffer, n) ;

	// pwm and timer setup.
	configure_pwm();
	config_timer1();

	//test_board();
	reset_servo();

	while(1) {

		// read in input (1 bit per pin)
		input = read_pins();
		move_servo(input);
		//n = sprintf(buffer, "%d\r\n", (int)((OFFSET + (SCALAR * input)) * PERIOD));
		//USART_Write(USART2, buffer, n) ;
		wait(0);

	}

}


