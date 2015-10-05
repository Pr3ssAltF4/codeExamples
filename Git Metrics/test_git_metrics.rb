require_relative 'git_metrics'
require 'test/unit'

class TestGitMetrics < Test::Unit::TestCase

  def test_commit_example
  	assert_equal 2, num_commits(["commit abc", "commit 123"]), "Should have counted two commits"
  end

  def test_dates_with_three_days
  	exp = [ "Date:  Sun Jan 26 21:25:22 2014 -0600", \
  			"Date:  Sun Jan 23 21:25:22 2014 -0600", \
  			"Date:  Sun Jan 25 21:25:22 2014 -0600"]
    assert_equal 3, days_of_development(exp), "Should have been a 3 days difference"
  end

  #Add more tests here

  def test_unique_dev_num
	assert_equal 3, num_developers(["Author: Ian Taylor <artfowl@ymail.com>", "Author: Izzy Taylor <iataylor12@live.com>", "Author: Adam Taylor <ixt7265@g.rit.edu>"]), "Should have had 3 unique devs"
  end

  def test_repeat_dev_num
	assert_equal 1, num_developers(["Author: Ian Taylor <artfowl@ymail.com>", "Author: Ian Taylor <artfowl@ymail.com>"]), "Should have had 1 developer"
  end

end
