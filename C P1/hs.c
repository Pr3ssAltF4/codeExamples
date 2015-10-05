
/*
 * Home Security System
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "hs_config.h"
#include "hs_util.h"

/**
 * An event node on the linked list of events for
 * a room. Consists of an event as gathered from a
 * reading and a link to the next node on the list
 * (if any).
 */
struct evnode_t {
	struct event_t event ;
	struct evnode_t *next ;
} ;

/*
 * Room event information
 * 	The room number.
 * 	Total number of events that have been logged.
 * 	Pointer to the most recent reading's node (if any).
 * 	Pointer to the next room (if any).
 */
struct room_t {
	int room;
	int ecount;
	struct evnode_t *evl_head;
	struct room_t *next_room;
} ;

/*
 * Head of the list of rooms being monitored.
 */
static struct room_t *room_list = NULL ;

/*
 * Local support functions (static).
 * You have to fill in the details.
 * Feel free to add more to make your work easier!
 */
static void process_a_reading(struct reading_t reading) ;

static struct room_t *find_room(int room) ;
static struct room_t *add_new_room(int room) ;
static void trim_list(int room, int keep, char timestamp[]) ;

static struct evnode_t *make_event_node() ;


/*
 * Main driver function.
 *
 * First, initialize global data structures (rooms array).
 *
 * Next, read lines of text representing readings, parse these, and if there
 * are no syntax errors, record the associated events. Syntactically incorrect
 * input reading lines are silently discarded.
 */
int main() {

	char next_line[MAX_LINELENGTH+1] ;
	struct reading_t reading ;

	/*
	 * Read a line of text into next_line, then attempt to parse
	 * it as a <reading> line. If the line is parsable, get the
	 * last reading structure and process it according to the
	 * specification for the appropriate level.
	 * See hs_util.h for useful utility functions.
	 */

	// FILL IN THE BODY
        while( read_line(next_line, MAX_LINELENGTH) != EOF) {
                if(parse_line(next_line)) {
                        reading = get_last_reading();
                        process_a_reading(reading);
                }
        }
        return 0 ;
}

static void print_reading(struct event_t event1, int roomNum) {
        char timeString [MAX_LINELENGTH + 1];
        strcpy(timeString, event1.time_stamp);
        int sensor = event1.sensor;
        int eventType = event1.event_id;
        int eventData = event1.event_info;

        if(eventType == 1) printf("Sensor %d @ %s: temperature reading %d degrees\n", sensor, timeString, eventData);
        if(eventType == 2) printf("Sensor %d @ %s: carbon monoxide reading %d PPB\n", sensor, timeString, eventData);
        if(eventType == 3) printf("Sensor %d @ %s: intruder alert\n", sensor, timeString);
	if(eventType == 8) printf("Trim log @ %s: room %d log trimmed to length %d (%d entries removed).", timeString, roomNum, eventData, find_room(roomNum)->ecount - eventData);
}



static void print_room(int roomId, struct event_t latest_event) {
	printf("*****\nHome Security System: Room %d @ %s\nTriggered by sensor %d\n%d total room events\n", roomId, latest_event.time_stamp, latest_event.sensor, find_room(roomId)->ecount);
	struct room_t * printTarget = find_room(roomId);
	struct evnode_t * evNode1 = printTarget->evl_head;
	if(evNode1 != NULL) {
		while(evNode1) {
			print_reading(evNode1->event, roomId);
			evNode1 = evNode1->next;
		}
	}
	printf("\n");
}


/*
 * Given a reading, process the included event for the room in the reading.
 * T_PRINT and T_TRIM readings are really commands; once executed they ar * discarded.
 * For all other readings check to see whether an alert should be printed,
 * then add the event to as the newest event in the room's event list.
 */
static void process_a_reading(struct reading_t reading) {

	int roomId = reading.room_id;
	struct room_t * changedRoom;
	changedRoom = find_room(roomId);
printf("---Made it to initialization\n");
	if(reading.event.event_id == 9) {
printf("---Printing\n");
		print_room(roomId, reading.event);
	} else if (reading.event.event_id == 8) {
printf("---Trimming\n");
		trim_list(roomId, reading.event.event_info, reading.event.time_stamp);
	} else {
printf("---Starting behavior\n");
		struct room_t * current = find_room(roomId);
		current->ecount++;
		struct evnode_t * newNode = make_event_node(reading.event);
		struct evnode_t * temp = current->evl_head;
printf("---Made it to checking evl head\n");
		if(current->evl_head == NULL) {
			current->evl_head = newNode;
		} else {
			while(temp) {
				if(temp != NULL && temp->next == NULL) { temp->next = newNode; break; }
				else if(temp != NULL && temp->next != NULL) temp = temp->next;
			}
		}
printf("---Made it to alert prints\n");
		if(reading.event.event_id == 1 && (reading.event.event_info < 50
			|| reading.event.event_info > 110)) {
			printf("Temperature alert @ %s: room %d / sensor %d / %d degrees\n", reading.event.time_stamp, roomId, reading.event.sensor, reading.event.event_info);
		}
		if(reading.event.event_id == 2 && (reading.event.event_info > 3000)) {
			printf("Carbon Monoxide alert @ %s: room %d / sensor %d / %d PPB\n", reading.event.time_stamp, roomId, reading.event.sensor, reading.event.event_info);
		}
		if(reading.event.event_id == 3) {
			printf("Intruder alert @ %s: room %d / sensor %d\n", reading.event.time_stamp, roomId, reading.event.sensor);
		}
	}

}

/*
 * Find the specified <room> in the <room_list>, returning a pointer to the
 * found room_t structure or NULL if there is no such <room> in the list.
 */
static struct room_t *find_room(int room) {
printf("---FINDING ROOM %d\n", room);
	struct room_t * temp = room_list;

// testing purposes only
struct room_t * temp2 = room_list;
printf("\n------ PRINTING CURRENT ROOM LIST { ");
while(temp2) {
	printf(" [%d] ", temp2->room);
	temp2 = temp2->next_room;
} printf(" } END PRINT OF ROOM LIST -------\n");

// printf("Temp %d", temp->room); ----------------------------------------NULL POINTER IS THE PROBLEM
	while(temp) {
		if(temp->room == room) return temp;
		else temp = temp->next_room;
	}
	return add_new_room(room);
}

/*
 * Create a new room_t node for <room>, initialize its fields, and append
 * the node to the end of the <room_list>.
 * Returns a pointer to the new room's structure.
 */
static struct room_t *add_new_room(int room) {
printf("---ADDING ROOM\n");
	struct room_t * newRoom = malloc(sizeof(struct room_t));
	newRoom->room = room;
	newRoom->ecount = 0;
	newRoom->next_room = NULL;
	newRoom->evl_head = NULL;
printf("---..........\n");
	struct room_t * temp = room_list;
	if(temp != NULL) {
		while(temp) {
			if(temp->next_room == NULL){
				temp->next_room = newRoom;
				break;
			} else temp = temp->next_room;
		}
printf("---Finished adding\n");
	} else room_list = newRoom;
	return newRoom;
}

/*
 * If the <room> is in the <room_list>, trim the room's event node list
 * to at most <keep> entries. As the list is ordered from newest to
 * oldest, the oldest entries are discarded.
 *
 * Whether the room exists or not, and whether or not the list holds
 * anything, the specified "Trim log" message must be printed. Obviously,
 * for a non-existent room nothing is actually trimmed (removed).
 *
 * Note - dynamically allocated space for event nodes removed from
 *        the list must be freed.
 */
static void trim_list(int room, int keep, char timestamp[]) {
// You might have a problem with the fact that you add nodes onto the end of the list
// from oldest to most recent.

	struct room_t * cur = find_room(room);
	struct evnode_t * fakeHead = cur->evl_head;
	struct evnode_t * temp = fakeHead;
	int count = 1;

	if(cur->ecount > keep) {

		while(count <= cur->ecount - keep) {
			struct  evnode_t * nextNode = temp->next;
			fakeHead = temp->next;
			temp->next = NULL;
			free(temp);
			temp = nextNode;
			count++;
		}

	}
}

/*
 * Create a new evnode_t node, initialize it using the provided
 * event and a NULL link, and return the pointer to the node.
 */
static struct evnode_t *make_event_node(struct event_t event) {
	struct evnode_t * new_evnode = (struct evnode_t *) malloc(sizeof(struct evnode_t));

	new_evnode->next = NULL;
	new_evnode->event = event;

	return new_evnode ;
}
