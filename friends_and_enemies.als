// Freinds & Enemies Activity
// @ Author Ian Taylor ixt7265

some sig Person {
	friends : set Person,
	enemies : set Person
}


--------------------------------------- FACTS -----------------------------------------

// The enemies of a person's enemies are friends
// of that person.
fact EnemyOfEnemyIsFriend {
	all p : Person, q : p.enemies {
		q.enemies in p.friends
	}
}

// Everyone is a friend of him or her self.
fact AreOwnFriend {
	all p : Person {
		p in p.friends
	}
}

// Nobody has someone else as both a friend and an enemy.
fact NoFriendsAreEnemies {
	all p : Person {
		p.enemies not in p.friends and p.friends not in p.enemies
	}
}


// A person's friends have that person as their
// friend.
fact FriendsAreSymmetric {
	all p1, p2 : Person {
		p1 in p2.friends => p2 in p1.friends
		p2 in p1.friends => p1 in p2.friends
	}
}

// A person's enemies have that person as their
// enemy.
fact EnemiesAreSymmetric {
	all p1, p2 : Person {
		p1 in p2.enemies => p2 in p1.enemies
		p2 in p1.enemies => p1 in p2.enemies
	}
}

--------------------------------------- ASSERTIONS -----------------------------------------

// No person is his or her own enemy. // COULD NOT FIGURE THIS ONE OUT SORRY!!!!
//assert NotOwnEnemy {
	//all p : Person {
		//p not in p.enemies
	//}
//}
//check NotOwnEnemy for 8


--------------------------------------- PREDICATES -----------------------------------------

// There is exactly one person who is the enemy of
// everyone else.
pred CommonEnemy () {
	one p : Person {
		lone p.friends
	}
}
//run CommonEnemy for exactly 5 Person

// Some persons have no friends other than themselves.
pred SomeLonelyPersons () {
	some p : Person {
		lone p.friends
	}
}
run SomeLonelyPersons for exactly 5 Person

--------------------------------------- RUN -----------------------------------------

run {} for exactly 40 Person






