# Script that obtains various git metrics from a basic git log file
require 'set'
require 'date'

# Given an array of git log lines, count the number of commits in the log
def num_commits(lines)
	commit_count = 0
	lines.each do |line| 
		if line.split[0] == "commit"
			commit_count += 1
		end
	end
	commit_count
end

# Given an array of git log lines, count the number of different authors
#   (Don't double-count!)
# You may assume that emails make a developer unique, that is, if a developer
# has two different emails they are counted as two different people.
def num_developers(lines)
	unique_dev = Set.new{}
	lines.each do |line|
		if line.split[0] == "Author:"
			unique_dev << line.downcase.gsub(/\([^>]+\)\s+/,'')
		end
	end
	unique_dev.length
end

# Given an array of Git log lines, compute the number of days this was in development
# Note: you cannot assume any order of commits (e.g. you cannot assume that the newest commit is first).
def days_of_development(lines)
	unique_dates = SortedSet.new{}
	lines.each do |line|
		arr = line.split
		if arr[0] == "Date:"
			unique_dates <<  DateTime.parse(line[5..-1])
		end
	end
	arr_dates = unique_dates.to_a
	if (arr_dates[arr_dates.length - 1].jd - arr_dates[0].jd) == 0
		return 1
	else
		return (arr_dates[arr_dates.length - 1].jd - arr_dates[0].jd) + 1
	end
end

# This is a ruby idiom that allows us to use both unit testing and command line processing
# Does not get run when we use unit testing, e.g. ruby test_git_metrics.rb
# These commands will invoke this code with our test data: 
#    ruby git_metrics.rb < ruby-progressbar-short.txt
#    ruby git_metrics.rb < ruby-progressbar-full.txt
if __FILE__ == $PROGRAM_NAME
  lines = []
  $stdin.each { |line| lines << line }
  puts "Nunber of commits: #{num_commits lines}"
  puts "Number of developers: #{num_developers lines}"
  puts "Number of days in development: #{days_of_development lines}"
end
