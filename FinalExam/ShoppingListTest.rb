require_relative './ShoppingList'
require 'test/unit'

class ShoppingListTest < Test::Unit::TestCase

  # Getting a noMethodError every time I run it.
  # My best guess is I either initialize it wrong
  # or am missing a line or two of code somewhere.
  # Spent 45 min going over it and looking for answers
  # online, but to no avail.
  # division_test works just fine though.

  attr_accessor :my_list
  attr_accessor :my_cart

	# Create a new list
	def setup
    @my_cart = ShoppingList.new
    @my_list = my_cart.init
	end
	
	# Verify that it is empty
	def test1
    assert_equal true, @my_cart.empty?, "Not empty"
	end
	
	# add a weekly item and check that there is one entry
	def test2
		@my_cart.addItem("Beer", 'w')
    assert_equal 1, @my_cart.numList, "Not length of 1"
	end
	
	# add 4 more items that are half monthly and half weekly
	def test3
		@my_cart.addItem("Scotch", 'm')
    @my_cart.addItem("More Cheese", 'w')
    @my_cart.addItem("Apples", 'w')
    @my_cart.addItem("Carrots", 'm')
    assert_equal 4, @my_cart.numList, "Not length of 5"
	end
	
	# list all items (weekly and monthly)
	def test4
    @my_cart.addItem("Scotch", 'm')
    @my_cart.addItem("More Cheese", 'w')
    @my_cart.addItem("Apples", 'w')
    @my_cart.addItem("Carrots", 'm')
    # needed to add cause only temp storage currently

		@my_cart.listAll
	end
	
	# list only monthly items
	def test5
    @my_cart.addItem("Scotch", 'm')
    @my_cart.addItem("More Cheese", 'w')
    @my_cart.addItem("Apples", 'w')
    @my_cart.addItem("Carrots", 'm')
    # needed to add cause only temp storage currently

		@my_cart.listMonthly
  end
end