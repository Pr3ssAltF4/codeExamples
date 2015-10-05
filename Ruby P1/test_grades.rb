require_relative 'grades_util'
require 'test/unit'

# TetsGrades
#
# Unit test suite for testing grades_util.rb support methods:
#	compute_grade()
#	get_CSV_line()
#	numeric_to_letter()
#	sum_weights()

class TestGrades < Test::Unit::TestCase
   
  # Tests get_CSV_line to insure the entered input line
  # is correctly be parsed to an array of string words
  #
  def test_header_line
	headers = get_CSV_line("Name,ID,Grade")		  # pass in an input string 
	puts headers
	assert_equal ["Name","ID","Grade"], headers   # return an array of header words
  end

  def test_sum_weights
	weights = get_CSV_line("20,10,70")
	puts weights
	assert_equal ["20","10","70"], weights
	total_weight = sum_weights(weights)	
	puts total_weight
  end

  def test_numeric_to_letter
	numeric = 83
	puts numeric_to_letter(numeric)
	assert_equal "B-", numeric_to_letter(numeric)
  end

  def test_compute_grade
	weight = get_CSV_line("50")[0]
	grade = ("98")
	assert_equal(98 * 0.5, compute_grade(weight, grade), "Not equal")
  end
  
end
  
