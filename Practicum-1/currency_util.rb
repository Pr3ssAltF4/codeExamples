# Currency Calculator Utility Methods

# Hash of currency conversions to be used in calculations
# For any given currency, multiplying by the rate converts
#     the currency to USD (U. S. dollars).
# For any given currency, dividing by the rate converts
#     USD (U.S. dollars) to the currency.
RATES = {
    "GBP" => 1.54,
    "CAN" => 0.80,
	"AUD" => 1.28,
	"EUR" => 1.12,
	"USD" => 1.0
}

# Given a currency code and floating point amount, convert to the
# equivalent amount in USD (U. S. dollars).
# The result *MUST* be rounded to two fractional digits.
def to_dollars(currency_code, amount)
  dollar = (amount * RATES[currency_code]).round(2)
end

# Given a currency code and floating point amount, convert to the
# amount in USD (U. S. dollars) to an equivalent amount in the
# currency.
# The result *MUST* be rounded to two fractional digits.
def from_dollars(currency_code, amount)
  other_cur = (amount / RATES[currency_code]).round(2)
end

# Given an input string in CSV format, return an array
# of strings representing the fields as demarcated by commas.
def parse( line )
  arr = line.split(',')
end
