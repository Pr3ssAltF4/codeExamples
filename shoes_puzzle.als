abstract sig FName{
	lname : one LName,
	shoe : one Shoe,
	color: one Color
}

one sig Clarisse, Margaret, Nancy, Sally extends FName {}

enum LName { Barlow, Parker, Stevens, West }

enum Shoe { Boots, Flats, Pumps, Sandals }

enum Color { Black, Brown, Green, Pink }

	/* These one-to-one mappings only work using the '=' operator since
		there is exactly the same number of enum's and Couples	
	*/
fact OneToOne {			   
//	all  disjoint fn1, fn2 : FName | fn1.lname!= fn2.lname  
	FName.lname = LName 	// unique names (first, last)
	FName.shoe = Shoe       //unique shoe
	FName.color = Color	   //shoe has unique color
}

fact One{
	Nancy.lname = Barlow
	Nancy.shoe != Boots
}

fact Two {
	Sally.shoe = Pumps
	let first_name = lname.Parker{
		first_name.color = Green
	}
}

fact Three {
	let w_pumps = shoe.Pumps {
		w_pumps.color != Pink
	}
}

fact Four {
		let w_boots = shoe.Boots{
			w_boots.color = Brown
			w_boots.lname != West
		}
}

fact Five {
	Sally.lname != Stevens
	Clarisse.shoe != Flats
}

fact Six {
	Margaret.lname  != Parker
	Margaret.shoe = Sandals
	Margaret.color != Black
}

run{} for 4
