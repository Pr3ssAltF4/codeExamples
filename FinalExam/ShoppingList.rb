# Shopping list - Create shopping list with weekly and monthly items
# 				- Support retrieving monthly list or weekly list

# Write a class that uses a hash to store the name of a food item
# like milk, eggs, and bread. For each food item define a frequency
# of purchase (monthly or weekly).
#
# You can assume that the data provided is valid -- no failure cases
# are required.
#
# Note -- if you cannot complete any part of this be sure
# to add comments describing how you would implement it.
class ShoppingList
  # 'm' = monthly replacement
  # 'w' = weekly replacement
  attr_accessor :shop

  # Create the shopping list hash
  def init()
   @shop = Hash.new
  end

  # add one item to the list with either a weekly or monthly frequency
  def addItem (food, frequency)
	    @shop[food] = frequency
  end

  def empty?
	    @shop.empty?
  end
    
  # How long is the list?
  def numList
	    @shop.size
  end

  def listAll
	    @shop.each do |food, freq|
        printf("%s is restocked %c\n", food, freq);
      end
  end
  
  def listMonthly
	   @shop.each do |food, freq|
        if(freq == 'm')
          printf("%s is restocked monthly\n", food);
        end
      end
  end

  def listWeekly
    @shop.each do |food, freq|
      if(freq == 'w')
        printf("%s is restocked weekly\n", food)
      end
    end
  end

end