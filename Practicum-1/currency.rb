require_relative 'currency_util'

# Currency Calculator Main Driver


# For each line of CSV input from $stdin:
#	- chomp the line to remove any end of line characters.
#	- parse into the two currencies and the amount.
#	- convert the amount from string to floating point.
#	- get the converted amount.
#	- print the result as
#	      "<OAMT> in <FC> is <CAMT> in <TC>"
#         where
#           <OAMT>  is the original amount from the input line,	  
#           <FC>    is the from currency identifier string,
#           <CAMT>  is the converted amount, and
#           <TC>    is the to currency identifier string.

$stdin.each do |line|
  arr = line.chomp.split(',')
  if arr[0] == 'USD'
	amount = to_dollars(arr[2],arr[1].to_f)
	puts arr[1].to_f,' in USD is ', amount,' in ', arr[2]  
  else
	amount = from_dollars(arr[2], arr[1].to_f)
	puts arr[1].to_f,' in ', arr[0],' is ', amount,' in USD' 	
  end
end
