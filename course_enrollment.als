abstract sig Person{}
sig Faculty extends Person {}

abstract sig Student extends Person{}
sig Grad, Undergrad extends Student {}

sig Instructor in Person{
	teaches : Course
}

sig Course{
	taughtby:  one Instructor,
	enrolled:	some Student,
	waitlist:	set Student,
	prereq:		set Course
}



--------------------- FACTS ------------------------------
// (Complete the following facts)

// Fact 1 : All instructors are either faculty or graduate students

fact{
	// FILL IN

// Fact 2 : You cannot teach a course that you are enrolled in or are on the waitlist for

   // FILL IN
	
// Fact 3 : No one can be on the waiting list of a course unless someone is enrolled in that course

  // FILL IN	

// Fact 4 : No student can be enrolled and on the waiting list for the same course

	// FILL IN

// Fact 5 : Course cannot be a pre-req of itself (or any course that it is a pre-req for)

   // FILL IN 

}

------------------- Assertions ----------------------------------

// No instructor is on the waitlist for a course they teach

assert InsWaitList {
   // FILL IN
}
check InsWaitList

// No student can be enrolled and on the waiting list for the same course
assert StudentEnroll{
  // FILL IN
}
check StudentEnroll

run MyRun1{}

-----------------Predicates -------------------------------------
pred p_academic{
	some Grad & Instructor
#Course > 1
#Undergrad > 2
}

run p_academic for 4
