#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <sys/netmgr.h>
#include <sys/neutrino.h>
#include <sys/siginfo.h>
#include <pthread.h>
#include <unistd.h>

// Defines
#define TRUE 1
#define FALSE 0

// Structs
typedef union {
        struct _pulse   pulse;
} message_t;

// struct representing a teller.
typedef struct teller{

	// semaphores, number, and next break time needed.
	_Bool available;
	_Bool needs_break;
	uint8_t teller_num;
	uint16_t break_time;
	uint16_t next_break;

	// metrics
	uint8_t num_breaks_today;
	uint16_t total_idle_time;

} Teller;

// struct representing a customer.
typedef struct customer {

	struct Customer * next_customer;
	struct Customer * prev_customer;

	// status
	_Bool waiting;
	_Bool processed;

	// metrics
	uint16_t entry_time, exit_time, wait_time; // wait = exit - entry
	uint16_t processing_time;

} Customer;

//typedef struct customer_node {
//
//	struct NodeC * next_customer;
//	Customer * self;
//	struct NodeC * prev_customer;
//
//} NodeC;

// The first customer enters through the head and exits through the tail.
typedef struct queue {

	Customer * front;
	Customer * back;

	uint8_t customers_in_line;

} Queue;

uint16_t current_time; // in ms
uint8_t who_has_queue_mutex; // #0-3. 0 is available, 1-3 are teller nums.
Queue * line;
_Bool break_on = FALSE;

// Function declarations
void* do_nothing (void* arg);
void* run_teller (void* arg);
int uniform_distribution (int rangeLow, int rangeHigh);
Customer * create_customer (void);
Teller * create_teller (void);

// Function definitions
void* run_teller (void* arg) {

	Customer * current_cust;
	Teller * teller;

	teller = (Teller *) arg;
	teller->next_break = current_time + uniform_distribution(3000, 6000);

	printf("Teller %d initialized\n", teller->teller_num);

	while (line->customers_in_line > 0 || current_time < 42000) { // while the day is still going and there are customers in line

		//printf("Teller %d doing stuff %d, %d, %d, %d\n", teller->teller_num, current_time, teller->next_break, line->customers_in_line, teller->available);

		if(teller->next_break != 0 && current_time >= teller->next_break && break_on) // TODO : IMPORTANT SET EVERYTHING TO ZERO INITIALLY
			teller->needs_break = TRUE;

		if (teller->needs_break && break_on) {

			teller->break_time = uniform_distribution(100, 400);
			delay(teller->break_time);
			teller->needs_break = FALSE;
			teller->num_breaks_today++;
			teller->next_break = current_time + uniform_distribution(3000, 6000);

		}
		else if (line->customers_in_line > 0) { // if we have customers in line

			if(who_has_queue_mutex == 0)
				who_has_queue_mutex = teller->teller_num;

			if(who_has_queue_mutex == teller->teller_num) {

				current_cust = line->front; // update the line and the current customer.
				if(line->front->next_customer != NULL)
					line->front = (Customer *) line->front->next_customer;
				else
					line->front = NULL;
				line->customers_in_line-- ;

				who_has_queue_mutex = 0;

				current_cust->waiting = FALSE;
				current_cust->exit_time = current_time; // entry_time needs to be set in main
				current_cust->wait_time = current_cust->exit_time - current_cust->entry_time;

				current_cust->processing_time = uniform_distribution(50, 800);
				delay(current_cust->processing_time);
				current_cust->processed = TRUE;

			}

		}
		else {

			teller->total_idle_time++; // this MIGHT work because the thread should just continue to run and loop every ms.
			delay(1);

		}

	}

	printf("Teller %d finished\n", teller->teller_num);

	return "";

}


// Credit to user : jxh --- Uniform Distribution Generator function.
// http://stackoverflow.com/questions/11641629/generating-a-uniform-distribution-of-integers-in-c
// We added the randomness seed for the rand() function. Grabs the current nano second value from the
// CLOCK_REALTIME and uses it to randomize each nano second (instant new values for the rand function).
int uniform_distribution (int rangeLow, int rangeHigh) {

	struct timespec tp;
	clock_gettime(CLOCK_REALTIME, &tp);
	srand((unsigned) tp.tv_nsec);

    double myRand = rand() / (1.0 + RAND_MAX); // RAND_MAX being the maximum range (the maximum and minimum times).
    int range = rangeHigh - rangeLow + 1;
    int myRand_scaled = (myRand * range) + rangeLow;
    // average over the max random number you can generate with rand() | myRand < 1
    // * current range given.
    // + offset from mimimum value.

    return myRand_scaled;

}

// Testing function for threads, timers, and random dist. generator.
void* do_nothing (void* arg) {

	int x;

	printf("Doing nothing\n");

	x = uniform_distribution(50, 800);

	printf("Running do nothing delay %d, %d\n", pthread_self(), x);

	delay(x);

	printf("Ran do nothing delay %d, %d\n", pthread_self(), x);

	printf("%d\n", uniform_distribution(50, 800));

	while(1) {

		x = uniform_distribution(50, 800);
		printf("%d, %d\n", uniform_distribution(50, 800), x);
		delay(x);

	}

	return "";

}

Customer * create_customer() {

	return malloc(sizeof(Customer));

}

Teller * create_teller() {

	return malloc(sizeof(Teller));

}

int main(int argc, char *argv[]) {

	printf("Welcome to the QNX Momentics IDE\n");

	struct sigevent event;
	struct itimerspec time_interval;
	timer_t timer_id;
	int channel_id;
	int receive_id;
	message_t msg;

	Customer * first_customer;
	Customer * current_customer;
	Teller * teller1;
	Teller * teller2;
	Teller * teller3;
	uint16_t next_customer_arrival;
	_Bool added_customer;

	printf("Initializing\n");

	line = malloc(sizeof(Queue));

	// Teller initialization
	teller1 = create_teller();
	teller1->available = TRUE;
	teller1->needs_break = FALSE;
	teller1->break_time = 0;
	teller1->next_break = 0;
	teller1->teller_num = 1;
	teller1->num_breaks_today = 0;
	teller1->total_idle_time = 0;

	teller2 = create_teller();
	teller2->available = TRUE;
	teller2->needs_break = FALSE;
	teller2->break_time = 0;
	teller2->next_break = 0;
	teller2->teller_num = 2;
	teller2->num_breaks_today = 0;
	teller2->total_idle_time = 0;

	teller3 = create_teller();
	teller3->available = TRUE;
	teller3->needs_break = FALSE;
	teller3->break_time = 0;
	teller3->next_break = 0;
	teller3->teller_num = 3;
	teller3->num_breaks_today = 0;
	teller3->total_idle_time = 0;

	printf("Tellers initialized\n");

	// pthread_create(NULL, NULL, &do_nothing, NULL); // Testing function for timers and threads

	channel_id = ChannelCreate(0);

	event.sigev_notify = SIGEV_PULSE;
	event.sigev_coid = ConnectAttach(ND_LOCAL_NODE, 0, channel_id, _NTO_SIDE_CHANNEL, 0);
	event.sigev_priority = getprio(0);
	event.sigev_code = _PULSE_CODE_MINAVAIL;

	printf("Creating timer\n");

	timer_create(CLOCK_REALTIME, &event, &timer_id);

	// resetting timer values needs to be done whenever we do something (deal with a customer)
	// (take a break) (etc...)

	time_interval.it_value.tv_sec = 0;
	/* 500 million nsecs = .001 secs */
	time_interval.it_value.tv_nsec = 1000000;
	time_interval.it_interval.tv_sec = 0;
	/* 500 million nsecs = .001 secs */
	time_interval.it_interval.tv_nsec = 1000000;

	printf("Starting timer\n");

	timer_settime(timer_id, 0, &time_interval, NULL); // This is where the timer gets 'turned on'.

	// Initial time setting and initial customer creation.
	next_customer_arrival = uniform_distribution(100, 400);

	first_customer = create_customer();

	first_customer->next_customer = NULL;
	first_customer->prev_customer = NULL;

	current_customer = first_customer;

	line->front = current_customer;
	line->back = current_customer;

	who_has_queue_mutex = 0;

	printf("Starting threads\n");

	pthread_create(NULL, NULL, &run_teller, (void *)teller1);
	printf("Teller %d check\n", teller1->teller_num);
	pthread_create(NULL, NULL, &run_teller, (void *)teller2);
	printf("Teller check %d\n", teller2->teller_num);
	pthread_create(NULL, NULL, &run_teller, (void *)teller3);
	printf("Teller check %d\n", teller3->teller_num);

	printf("Main timer loop\n");

	// Main timer loop
	for(;;) {

		receive_id = MsgReceive(channel_id, &msg, sizeof(msg), NULL);
		if(receive_id == 0) {

			if(msg.pulse.code == _PULSE_CODE_MINAVAIL) {

				//printf("It's ALIVE %d\n", current_time++); // Reset the timer value here with the random distribution.

				if(current_time % 1000 == 0)
					printf("%d\n", current_time);

				if(current_time >= next_customer_arrival) { // Process for adding a new customer to the queue.

					//printf("creating customer\n");

					added_customer = FALSE;

					while(!added_customer) {

						if(who_has_queue_mutex == 0) { // if we can work with the queue.

							who_has_queue_mutex = 4;

							current_customer = create_customer();

							current_customer->prev_customer = (struct Customer *) line->back;
							current_customer->next_customer = NULL;

							line->back = current_customer;

							added_customer = TRUE;
							who_has_queue_mutex = 0;

						} else
							delay(1);

					}

				}

				current_time++; // Timer pulses every ms, incrementing the current time during the day, 0 = 9 am, 42000 = 4 pm

			}

			if(current_time > 42000 && line->customers_in_line == 0) // TODO : CHANGE THIS TO WAIT UNTIL ALL CUSTOMERS ARE PROCESSED.
				break;

		}

	}

	printf("Timer done");

	return EXIT_SUCCESS;

}
