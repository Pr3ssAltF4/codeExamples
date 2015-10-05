# simple division code
# first checks for string parameters and raises exception if so
# then checks for a divisor of 0 before dividing.

def division(numerator, denominator)
  raise ArgumentError, 'no strings allowed' if numerator.is_a? String
  raise ArgumentError, 'no strings allowed' if denominator.is_a? String
  raise ArgumentError,' number is negative' if denominator == 0 
  
  result = numerator / denominator
  return result
end
