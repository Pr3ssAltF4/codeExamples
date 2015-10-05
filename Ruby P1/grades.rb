require_relative 'grades_util'

# grades.rb Ruby Script
#
# Read the first row (column names) and second row (grade weights).
# If the weights don't sum up to 100, print an error message and exit.
# Otherwise print the column headers with their weights (empty weights simply don't print)
#
# For each student line, print the header and column for each field in the line.
# The field could be identifying information (if the weight is blank) or numeric (if the
# weight is non-negative). Grades can be numeric or letter (with optional +/-)
# Also prints final weighted numeric grade and letter grade.
#
# At end, prints a summary showing the number students for each letter grade and
# the class GPA.


# Create the hash for counting the number of occurrences of each letter grade.

letter_grade_count = Hash.new(0)   # default count is 0.

# Use get_CSV_line() to get the header and weight lines.
# Each line should be "chomped" to eliminate the end of line character(s).
# Create arrays for the headers and weights by splitting on commas.

header_line = get_CSV_line(ARGF.readline)
weights_line = get_CSV_line(ARGF.readline)

# For each header, print the header and, if present, its weight
i = 0
header_line.each do |entry|
	weight = weights_line[i]
	if weight != ''
		 weight += "%"
	end
	puts header_line[i] + " " + weight
	i += 1
end

# Use sum_weights() to check if the weights do not sum to 100, output the error message:
# "Weights add up to #{sum}, not 100" - where sum is the sum of input weights

if sum_weights(weights_line) != 100
	puts "Weights add up to #{sum_weights(weights_line)}, not 100"
end

# Get each of the remaining lines, representing grade information for an individual student.
# Print the header for each column and whatever is in that column on the student grade line.
# Compute contribution of each weighted field to the overall grade using compute_grade(),
# remember to skip fields that do not have weights associated with them.
# Convert the numeric grade to a letter grade using numeric_to_letter().
# Output the final numeric and letter grade for that student and update the 
# lettercount hash that is keeping track of the number of occurrences of each letter grade
# for the class.
puts ""
ARGF.each_line do |line|
	j = 0
	this_line = get_CSV_line(line)
	header_line.each do |entry|
		puts header_line[j] + ": " + this_line[j]
		j += 1	
	end
	k = 0
	final_grade = 0
	this_line.each do |e|
		if weights_line[k] != ''
			final_grade += compute_grade(weights_line[k], this_line[k])
		end
		k += 1
	end
	letter_grade_count[numeric_to_letter(final_grade.to_f)[0]] += 1
	puts "Final Numeric Grade = " + final_grade.to_s + " Letter = " + numeric_to_letter(final_grade.to_f).to_s
	puts ""
end 

# Now print the summary information - the number of students at each letter grade level
# and the class GPA using print_summary(). 

  gpa = 0.0
  student_count = 0.0
  letter_grade_count.each do |letter, count|
	print letter, " = ", count, "\n"
	gpa += QUALITY_POINTS[letter[0]] * count
	student_count += count.to_f
  end
  gpa /= student_count
  print "Class GPA = ", gpa, "\n"
