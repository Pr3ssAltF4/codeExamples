require_relative 'currency_util' 
require 'test/unit'          

class CurrencyTest < Test::Unit::TestCase 

  def close_enough(expected, actual, epsilon = 0.001)
    return (expected - actual).abs <= epsilon
  end

  ### Tests of to_dollars ###

  def test_001a_convert_3_33_units_to_dollars
    assert close_enough(5.13, to_dollars('GBP', 3.33))
    assert close_enough(2.66, to_dollars('CAN', 3.33))
    assert close_enough(4.26, to_dollars('AUD', 3.33))
    assert close_enough(3.73, to_dollars('EUR', 3.33))
    assert close_enough(3.33, to_dollars('USD', 3.33))
  end

  def test_001b_your_tests
    assert close_enough(3.20, to_dollars('CAN', 4.00)), "Should have been 5, was #{to_dollars('CAN', 4.00)}"
    assert close_enough(0.03, to_dollars('AUD', 0.02)), "Should have been 0.02, was #{to_dollars('AUD',0.02)}"
  end

  ### Tests of from_dollars ###

  def test_002a_convert_3_33_units_to_dollars
    assert close_enough(2.16, from_dollars('GBP', 3.33))
    assert close_enough(4.16, from_dollars('CAN', 3.33))
    assert close_enough(2.60, from_dollars('AUD', 3.33))
    assert close_enough(2.97, from_dollars('EUR', 3.33))
    assert close_enough(3.33, from_dollars('USD', 3.33))
  end

  def test_002b_your_tests
    assert close_enough(0.89, from_dollars('EUR', 1.00)), "Should have been 1.12, was #{from_dollars('EUR', 1.00)}"
    assert close_enough(0.01, from_dollars('CAN', 0.01)), "Should have been 0.01, was #{from_dollars('CAN', 0.01)}"
  end

  ### Tests of parse ###
  
  def test_003a_normal_line
    expect = ['AUD', '1.56' ,'EUR']
    actual = parse('AUD,1.56,EUR')
    assert_equal(expect, actual)
  end

  def test_003b_your_first_test
    expect = ['CAN', '4.00', 'USD']
    actual = parse('CAN,4.00,USD')
    assert_equal(expect,actual)
  end

  def test_003c_your_second_test
    expect = ['USD', '4.0', 'CAN']
    actual = parse('USD,4.0,CAN')
    assert_equal(expect, actual)
  end
end
