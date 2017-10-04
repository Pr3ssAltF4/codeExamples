#ifndef __PWM_H
#define __PWM_H

#include "stm32l476xx.h"

void configure_pwm(void);
void reset_servo(void);
void set_servo_position(int servo_position);
void stop_pwm(void);
void start_pwm(void);
void config_timer1(void);
void wait(int delay);
int check_input(void);

#define PERIOD (200)
#define SCALAR (0.0003906)
#define OFFSET (0.02)
#define PRESCALER (7999)

#endif /* __PWM_H */
