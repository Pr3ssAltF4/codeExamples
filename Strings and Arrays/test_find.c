/*
 * Unit tests for the find module.
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include "find.h"

#define NOT_FOUND	(-1)	// not found integer indicator

/*
 * Local test and support functions.
 */
static bool test_find_ch_index() ;
static bool test_find_ch_ptr() ;
static bool test_find_any_index() ;
static bool test_find_any_ptr() ;
static bool test_find_substr() ;
static void test_failure() ;
static void summary() ;
static bool assert_impl(bool expr, char *f_name, int f_line, char *message) ;

/*
 * Macros so we don't have to explicitly pass filenames and line numbers
 * for each assertion.
 */
#define assert(e) assert_impl(e, __FILE__, __LINE__, NULL)
#define assert_msg(e, m) assert_impl(e, __FILE__, __LINE__, m)

/*
 * Number of tests, number of assertions passed, number of assertions failed.
 */
static int ntests = 0 ;
static int npass = 0 ;
static int nfail = 0 ;

/*
 * Strings used in the tests.
 * We need constant names for them so we can test accuracy of
 * the returned pointed.
 */

char ts_abc[] = "abccba" ;
char ts_empty[] = "" ;

int main(int ac, char **av) {
	fprintf(stderr, "** Tests of find_ch_index **\n") ;
	if( ! test_find_ch_index() ) {
		test_failure() ;
	}

	fprintf(stderr, "** Tests of find_ch_ptr **\n") ;
	if( ! test_find_ch_ptr() ) {
		test_failure() ;
	}

	fprintf(stderr, "** Tests of find_any_index **\n") ;
	if( ! test_find_any_index() ) {
		test_failure() ;
	}

	fprintf(stderr, "** Tests of find_any_ptr **\n") ;
	if( ! test_find_any_ptr() ) {
		test_failure() ;
	}

	fprintf(stderr, "** Tests of find_substr **\n") ;
	if( ! test_find_substr() ) {
		test_failure() ;
	}

	summary() ;
	return 0 ;
}

static bool test_find_ch_index() {
	bool pass = true ;

	ntests++ ;

	pass = assert_msg(find_ch_index(ts_abc, 'a') == 0,
			"'a' not at position 0 in \"abccba\"") && pass ;
	pass = assert_msg(find_ch_index(ts_abc, 'b') == 1,
			"'b' not at position 1 in \"abccba\"") && pass ;
	pass = assert_msg(find_ch_index(ts_abc, 'c') == 2,
			"'c' not at position 2 in \"abccba\"") && pass ;
	pass = assert_msg(find_ch_index(ts_abc, 'd') == NOT_FOUND,
		       "'d' found in \"abccba\"") && pass ;
	pass = assert_msg(find_ch_index("", 'a') == NOT_FOUND,
		       "'d' found in \"\"") && pass ;
	return pass ;
}

static bool test_find_ch_ptr() {
	bool pass = true ;
	char *found ;

	ntests++ ;

	found = find_ch_ptr(ts_abc, 'a') ;
	pass = assert_msg(found == ts_abc,
			"'a' not at position 0 in \"abccba\"") && pass ;
	found = find_ch_ptr(ts_abc, 'b') ;
	pass = assert_msg(found == ts_abc + 1,
			"'b' not at position 1 in \"abccba\"") && pass ;
	found = find_ch_ptr(ts_abc, 'c') ;
	pass = assert_msg(found = ts_abc + 2,
			"'c' not at position 2 in \"abccba\"") && pass ;
	found = find_ch_ptr(ts_abc, 'd') ;
	pass = assert_msg(found == NULL,
			"'d' found in \"abccba\"") && pass ;
	found = find_ch_ptr("", 'd') ;
	pass = assert_msg(found == NULL,
		       "'d' found in \"\"") && pass ;
	return pass ;
}

static bool test_find_any_index() {
	bool pass = true ;
	int idx ;

	ntests++ ;

	idx = find_any_index(ts_abc, "cba") ;
	pass = assert_msg(idx == 0,
		"'a' not at position 0 in \"abccba\"") && pass ;

	idx = find_any_index(ts_abc, "cbx") ;
	pass = assert_msg(idx == 1,
		"'b' not at position 1 in \"abccba\"") && pass ;

	idx = find_any_index(ts_abc, "cxy") ;
	pass = assert_msg(idx == 2,
		"'c' not at position 2 in \"abccba\"") && pass ;

	idx = find_any_index(ts_abc, "xyz") ;
	pass = assert_msg(idx == NOT_FOUND,
		"found 'x' or 'y' or 'z' in \"abccba\"") && pass ;

	idx = find_any_index("", "xyz") ;
	pass = assert_msg(idx == NOT_FOUND,
		"found 'x' or 'y' or 'z' in \"\"") && pass ;
	
	return pass ;
}

static bool test_find_any_ptr() {
	bool pass = true ;
	char *p ;

	ntests++ ;

	p = find_any_ptr(ts_abc, "cba") ;
	pass = assert_msg(p == ts_abc + 0,
		"'a' not at position 0 in \"abccba\"") && pass ;

	p = find_any_ptr(ts_abc, "cbx") ;
	pass = assert_msg(p == ts_abc + 1,
		"'b' not at position 1 in \"abccba\"") && pass ;

	p = find_any_ptr(ts_abc, "cxy") ;
	pass = assert_msg(p == ts_abc + 2,
		"'c' not at position 2 in \"abccba\"") && pass ;

	p = find_any_ptr(ts_abc, "xyz") ;
	pass = assert_msg(p == NULL,
		"found 'x' or 'y' or 'z' in \"abccba\"") && pass ;

	p = find_any_ptr("", "xyz") ;
	pass = assert_msg(p == NULL,
		"found 'x' or 'y' or 'z' in \"\"") && pass ;
	
	return pass ;
}

static bool test_find_substr() {
	bool pass = true ;
	char *p ;

	ntests++ ;

	p = find_substr(ts_empty, "") ;
	pass = assert_msg(p == ts_empty,
		"didn't match empty string at start of empty string") && pass ;

	p = find_substr(ts_abc, "") ;
	pass = assert_msg(p == ts_abc,
		"didn't match empty string at start of \"abccba\"") && pass ;

	p = find_substr(ts_abc, "abcc") ;
	pass = assert_msg(p == ts_abc,
		"didn't match \"abcc\" at start of \"abccba\"") && pass ;

	p = find_substr(ts_abc, "ccba") ;
	pass = assert_msg(p == ts_abc + 2,
		"didn't match \"ccba\" at end of \"abccba\"") && pass ;

	p = find_substr(ts_abc, "bca") ;
	pass = assert_msg(p == NULL,
		"matched \"bca\" in \"abccba\"") && pass ;

	return pass ;
}

static void test_failure() {
	fprintf(stderr, "** Test failed - exiting **\n") ;
	summary() ;
	exit(1) ;
}
	
static void summary() {
	fprintf(stderr, "*** TEST SUMMARY ***\n") ;
	fprintf(stderr, "%d test%s, ",
			ntests, ntests != 1 ? "s" : "");
	fprintf(stderr, "%d assertion%s ",
			npass + nfail, npass + nfail != 1 ? "s" : "") ;
	fprintf(stderr, "(%d passed/%d failed)\n",
			npass, nfail) ;
}

static bool assert_impl(bool expr, char *f_name, int f_line, char *message) {
	if( expr ) {
		npass++ ;
		return true ;
	}

	nfail++ ;
	if( message ) {
		fprintf(stderr, "Assertion failure (%s @ %d): %s\n",
				f_name, f_line, message) ;
	} else {
		fprintf(stderr, "Assertion failure (%s @ %d)\n",
				f_name, f_line) ;
	}
	return false ;
}
