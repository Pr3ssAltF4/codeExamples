abstract sig Couple {
	husband	:  one MaleName,	
	wife	:  one FemaleName,
	surname	:  one SurName,
	animal	:  one Animal,
	bird	: one  Bird
}
enum SurName { Connor, Carver, Jones, Porter, White }
enum MaleName{ Paul, Peter, Jim, Tom, Mike }
enum FemaleName { Joanna, Marjorie, Olivia, Patricia, Sandra }
enum Animal { Beaver, Rabbit, Coyote, Woodchuck, Fox }
enum Bird { Eagle, Goose, Pheasant, Swan, WildTurkey }

/*
* NOTE TO PROF ::>
* So I tried to make this work with only one instance, but was not entirely sure of why it is
* producing 4 possible results. There was an option to do it without let statements, but 
* I haven't had time to try that.
*/

fact One_to_One_Mappings {
	/* These one-to-one mappings only work using the '=' operator since
		there is exactly the same number of enum's and Couples	
	*/
	Couple.husband = MaleName
	Couple.wife = FemaleName
	Couple.surname = SurName
	Couple.animal = Animal
	Couple.bird = Bird

}

// FILL IN THE FOLLOWING FACTS

/* Fact #1 - Tom, who wasnâ€™t married to Olivia, saw a fox. 
                   The couple that saw the beaver also saw wild turkeys
 */
fact F1 {
	let t = husband.Tom {
		t.wife != Olivia
		t.animal = Fox
	}
	let c = animal.Beaver {
		c.bird = WildTurkey
	}
}

/* Fact #2 - Patricia Carver didnâ€™t see the pheasant. Paul didnâ€™t see the eagle. 
				   The Jonesâ€™s saw a coyote. Jimâ€™s last name wasnâ€™t White
*/
fact F2 {
	let p = wife.Patricia {		// GIVEN: Patrica's surname is Carver
		p.surname = Carver
		p.bird != Pheasant
	}
	let p1 = husband.Paul {
		p1.bird != Eagle
	}
	let j = surname.Jones {
		j.animal = Coyote
	}
	let j1 = husband.Jim {
		j1.surname != White
	}
}

/* Fact #3 - The Porters didnâ€™t see the swans. Tom wasnâ€™t married to Sandra and his last name wasnâ€™t Jones. 
                    The Connors spotted a rabbit
*/
fact F3 {
	let p = surname.Porter {
		p.bird != Swan
	}
	let t = husband.Tom {
		t.wife != Sandra
		t.surname != Jones
		surname.Connor.animal = Rabbit
	}
}

/* Fact #4 - The couple who saw the coyote didnâ€™t see the swan. 
                   Mike, whose last name wasnâ€™t Connor, didnâ€™t see the woodchuck. Sandra saw the goose
*/
fact F4 {
	let c = animal.Coyote {
		c.bird != Swan
	}
	let m = husband.Mike {
		m.surname != Connor
		m.animal != Woodchuck
	}
	let s = wife.Sandra {
		s.bird = Goose
	}
}

/* Fact #5 - Peter and his wife Joanna didnâ€™t see the wild turkeys. 
				    Jim, whose last name wasnâ€™t Jones, saw the pheasant but not the woodchuck.  
*/
fact F5 {
	let p = husband.Peter {
		p.wife = Joanna
		p.bird != WildTurkey
	}
	let j = husband.Jim {
		j.surname != Jones
		j.bird = Pheasant
		j.animal = Woodchuck
	}
}
/* Fact #6 - Marjorie White didnâ€™t see the swans. Paul Porter didnâ€™t see the beaver
*/
fact F6 {
	let m = wife.Marjorie {
		m.surname = White
		m.bird != Swan
	}
	let p = husband.Paul {
		p.surname != Porter
		p.animal != Beaver
	}
}

run { } for 5 		
