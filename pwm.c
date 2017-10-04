#include "pwm.h"

// Configures Timer 5 for PWM use
void configure_pwm(void){

    // General GPIOA Enable
    RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN ;

    // Configure for Servo 1
    // Setup timer
    RCC->APB1ENR1 |= RCC_APB1ENR1_TIM5EN;
    TIM5->PSC = PRESCALER;
    TIM5->EGR |= TIM_EGR_UG;
    TIM5->CCER &= ~TIM_CCER_CC1E;
    TIM5->CCMR1 &= ~(TIM_CCMR1_OC1PE | TIM_CCMR1_OC1M);
    TIM5->CCMR1 |= (TIM_CCMR1_OC1PE | TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2);
    TIM5->CR1 |= TIM_CR1_ARPE;
    TIM5->CCER |= TIM_CCER_CC1E;
    TIM5->EGR = TIM_EGR_UG;

    // Set Servo 1 Period
    TIM5->ARR = PERIOD;
    TIM5->EGR = TIM_EGR_UG;

    // Setup GPIO PA0
    GPIOA->MODER &= 0xfffffffe;
    GPIOA->AFR[0] |= 0x00000002;

    return ;
}

// Resets the servo to the zero position
void reset_servo(){

	TIM5->CCR1 = PERIOD * SCALAR * 128;
	TIM5->EGR |= TIM_EGR_UG;
	TIM5->CR1 |= TIM_CR1_CEN;

}

// Sets the servo position for the servo
void set_servo_position(int servo_position){

	TIM5->CCR1 = (int)((OFFSET + (SCALAR * servo_position)) * PERIOD);
	TIM5->EGR |= TIM_EGR_UG;
	TIM5->CR1 |= TIM_CR1_CEN;

}

// Stops PWM generation for servo
void stop_pwm(){
    TIM5->CR1 &= ~TIM_CR1_CEN;
}

// start pwm for servo
void start_pwm(){
    TIM5->CR1 |= TIM_CR1_CEN;
}

// configures the timer
void config_timer1(){

    RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;
    TIM1->PSC = PRESCALER;
    TIM1->EGR |= TIM_EGR_UG;
    TIM1->CCMR1 |= TIM_CCMR1_OC1M_0;
    TIM1->CCER |= TIM_CCER_CC1E;

}

// Waits for specified amount of time using delay in units of 1/10 of a second
void wait( int delay ){

	// Delay is in units of 1/10 of a second
    TIM1->CCR1 = 1000*(delay+1);
    TIM1->CR1 |= TIM_CR1_CEN;

    while((TIM1->SR & TIM_SR_CC1IF) != 2) ;

	TIM1->SR = 0;
    TIM1->CR1 &= ~TIM_CR1_CEN;
	TIM1->CNT = 0;

}
