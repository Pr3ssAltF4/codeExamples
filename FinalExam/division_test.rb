require_relative 'division' #We need to access our code to test
require 'test/unit'          #We need Ruby's unit testing library

class DivisionTest < Test::Unit::TestCase #This is a class. (It's ok if you don't know what those are yet)

  #Test methods MUST start with test_
  # define a success test dividing 48 by 2
  def test_normal
      assert_equal 24, division(48,2), "48 divided by 2 should be 24"
  end

  # define a success test dividing 20.4 by 4
  def test_another_normal
    assert_equal 5.1, division(20.4,4), "20.4 divided by 4 should be 5.1"
  end

  # define test to verify exception on 0 denominator
  def test_zero
    assert_raise ArgumentError do
      division(5,0)
    end
  end
  
  # define test to verify check for string value in numerator
  def test_string
    assert_raise ArgumentError do
      division("I'm not a number", "Yes I am")
    end
  end
  
end
