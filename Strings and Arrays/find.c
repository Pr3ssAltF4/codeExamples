/*
 * Implementation of functions that find values in strings.
 *****
 * YOU MAY NOT USE ANY FUNCTIONS FROM <string.h>
 *****
 */

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include "find.h"

#define NOT_FOUND (-1)	// integer indicator for not found.

/*
 * Return the index of the first occurrence of <ch> in <string>,
 * or (-1) if the <ch> is not in <string>.
 */
int find_ch_index(char string[], char ch) {
	int iter = 0;
	while(string[iter] != '\0') {
		if(string[iter] == ch) { return iter; }
		iter++;
	}
	return NOT_FOUND;	// placeholder
}

/*
 * Return a pointer to the first occurrence of <ch> in <string>,
 * or NULL if the <ch> is not in <string>.
 *****
 * YOU MAY *NOT* USE INTEGERS OR ARRAY INDEXING.
 *****
 */
// Help obtained from stack overflow.
char *find_ch_ptr(char *string, char ch) {
	char * point = string;
	while(*point != '\0') {
		if(*point == ch) return point;
		else point++;
	}
// printf("---Point %c\n", *point);
	return NULL;	// placeholder
}

/*
 * Return the index of the first occurrence of any character in <stop>
 * in the given <string>, or (-1) if the <string> contains no character
 * in <stop>.
 */
int find_any_index(char string[], char stop[]) {
	int iter = 0;
	int index, curEarliest;
	curEarliest = NOT_FOUND;
	while(stop[iter] != '\0') {
		index = find_ch_index(string, stop[iter]);
		if((curEarliest == NOT_FOUND || index < curEarliest) && index != NOT_FOUND) curEarliest = index;
		iter++;
	}
	return curEarliest;	// placeholder
}

/*
 * Return a pointer to the first occurrence of any character in <stop>
 * in the given <string> or NULL if the <string> contains no characters
 * in <stop>.
 *****
 * YOU MAY *NOT* USE INTEGERS OR ARRAY INDEXING.
 *****
 */
char *find_any_ptr(char *string, char* stop) {
	char * point = string;
	char * point0 = stop;
	while(*point != '\0') {
		while(*point0 != '\0') {
			if(*point == *point0) return point;
			point0 += 1;
		}
		point0 = stop;
		point += 1;
	}
	return NULL;
}

/*
 * Return a pointer to the first character of the first occurrence of
 * <substr> in the given <string> or NULL if <substr> is not a substring
 * of <string>.
 * Note: An empty <substr> ("") matches *any* <string> at the <string>'s
 * start.
 *****
 * YOU MAY *NOT* USE INTEGERS OR ARRAY INDEXING.
 *****
 */
char *find_substr(char *string, char* substr) {
	char * point = string;
	char * sub = substr;
	if(*sub == '\0') return point;
	// Tests for substring contained
	while(*point != '\0' && *sub != '\0') {
		if(*sub != *point) return NULL;
		sub++;
		point++;
	}
	// Finds the first occurence
	return find_any_ptr(string, substr);
}
