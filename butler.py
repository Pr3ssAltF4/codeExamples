#!/opt/clearsky/bin/python2.7
__author__ = 'itaylor'

# OLD CODE. FIRST VERSION OF BUTLER. Property of ClearSky Data

# Automated bug logging tool, Butler.
# When log_bug_exec() is run the program begins piping a copy of stdout(from jenkins website) to process_file.
# When EOF is hit, the file is processed. A Bug is created, duplicates are checked, and
# the bugs are logged to JIRA via JIRA REST api (jira-python module).

import sys, os, re, requests
from jira import JIRA
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


# Class representing a Bug obj. Creates the necessary JSON for POSTing to JIRA.
class Bug(object):
    def __init__(self, summary, version, environment, description, url, repnum):
        self.project = 'QABL'
        self.issue_type = 'Bug'
        self.priority = 'Major'
        self.version = version
        self.assignee = 'XXXXXX'
        self.environment = environment
        self.description = description
        self.summary = summary

        # creating dictionary object (bug should not have to be changed after initialization)
        self.json_dict = {"fields": {
            "project": {'key': self.project},
            "issuetype": {'name': self.issue_type},
            "priority": {'name': self.priority},
            "assignee": {'name': self.assignee},
            "environment": self.environment,
            "description": self.description,
            "summary": self.summary,
            "customfield_10301": repnum,
            "customfield_10300": url}}


# Class to run through piping, processing, and posting bugged output to JIRA.
class Butler:

    my_server = JIRA(options={'server': 'XXXXXXXX'}, basic_auth=('XXXXXXX', 'XXXXXXXX'))

    # The method that should be called to execute the logging of the bugs.
    def log_bug_exec(cls):
        print '\n\n-------------------- logbugexec -------------------------\n\n'
        stdout = cls.capture_output()
        cls.process_file(stdout)

    # Scrapes the ConsoleText of its plaintext to create the desired representation of the outcome of the test.
    def capture_output(cls):
        print "\n\n-------------------- piping the output -------------------------\n\n"
        stdout = "If this is still here there is a big problem"
        try:
            pyout = open('/home/csd-user/workspace/{}/pyout.txt'.format(os.environ['JOB_NAME']), 'r+')
            stdout = pyout.readlines()
        except Exception as e:
            print str(e)
        return stdout

    # Method to process the stdout file into sub lists to become easily parsable into Bugs.
    def process_file(cls, stdout):
        print '\n\n-------------------- processing file -------------------------\n\n'
        # List of some common dividing points in py.test output format
        targets = ['Finished: FAILURE', #0
                   '>        ', #1
                   'E        ', #2
                   '= FAILURES =', #3
                   '_______________ Test', #4
                   '_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ \n', #5
                   '= slowest test durations =', #6
                   '= ERRORS =', #7
                   'ERROR at', #8
                   '============================= test session starts ==============================\n', #9
                   'ERROR at ', #10
                   'ERROR in ' #11
                   ]

        # Gets to the top the Failures block in Console given a copy of the console and also retrieves environment at
        # the beginning of the file
        full_failure_list = list()
        has_failed = False
        failed = False
        # print str(len(stdout)) + " " + str(stdout.__class__)
        for line in stdout:
            if failed is True:
                full_failure_list.append(line)
                print line
            elif targets[3] in line \
                    or targets[7] in line \
                    or targets[10] in line \
                    or targets[11] in line \
                    or "Traceback (most recent call last):" in line:
                full_failure_list.append(line)
                print line
                failed = True
                has_failed = True
            elif targets[6] in line:
                failed = False
        print "\n\n-------------------- Done checking for failures -------------------------\n\n"

        if not has_failed:
            print "\n\n-------------------- no bugs or failures...nothing logged -------------------------\n\n"
            return
        else:
            print "\n\n-------------------- found bugs -------------------------\n\n"
            driverstring = str(os.environ['NODE_LABELS'].split(' ')[0])
            # nums = [int(s) for s in driverstring.split('-') if s.isdigit()]
            nums = re.findall(r'\d+', str(driverstring))
            n0 = nums[0]
            n1 = nums[1]
            cls.create_artifacts(nums[0], nums[1])

        # For each bug created, check for duplication, if not a duplicate, submit.
        bugs = cls.process_failure(full_failure_list)
        print "BUGS :::::::" + str(bugs)
        if bugs == -1:
            print "*** ERROR CODE : -1 ***\nBroke because failure list is not a string\n"
            print str(bugs)
            print str(bugs.__class__)
            print stdout
            return
        for bug in bugs:
            print "BUGS :: ", str(bug), " ", str(bugs)
            dup = cls.is_duplicate(bug) # Boolean val
            print str(dup)
            if not dup:
                cls.submit_bug(bug)
        print '\n\n-------------------- finished processing file -------------------------\n\n'

    # grabs all necessary files and drops them in a directory in /home/csd-user/workspace/BugLoggerTest/ to be added
    # as artifacts. Will overwrite each file every time its run in order to not overload the system with to many
    # copies of the text files. Called on a per build basis.
    def create_artifacts(cls, drivernum, driverlabelnum):

        import paramiko
        from jupiter import csd_shell_lib
        import docker
        from docker.errors import APIError

        print "\n\n-------------------- creating artifacts -------------------------\n\n"

        # Establishing setup.
        username = 'XXXXX'
        password = 'XXXXX'
        host_keys = os.path.expanduser(os.path.join("~", ".ssh", "known_hosts"))
        driver_ip = os.environ['SSH_CONNECTION'].split(' ')[2]
        last_three_nums = int(driver_ip.split('.')[3])
        ip = driver_ip.split('.')
        directory_name = "/home/csd-user/workspace/{}/".format(os.environ['JOB_NAME'])
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        print "\nDirectory name :: " + directory_name + "\n\n"

        try: # Creating files for l20. csd-log and messages. All .txt files.

            l20_machine_name = str(int(drivernum) + 1) + "-qa-test" + str(driverlabelnum)
            port = 22
            transport_l20 = paramiko.Transport((l20_machine_name, port))
            transport_l20.connect(username='root', password='XXXXXX')

            sftp_l20 = paramiko.SFTPClient.from_transport(transport_l20)
            filepath = '/var/log/messages'
            sftp_l20.get(filepath, directory_name + "messages_l20.txt", None)
            sftp_l20.close()

            ssh_l20 = paramiko.SSHClient()
            ssh_l20.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_l20.connect(l20_machine_name, username='root', password='XXXXXXX')
            stdin, stdout, stderr = ssh_l20.exec_command('csd log --after "2 hours ago"')
            foobarfile = open('{}/l20_csdlog.txt'.format(directory_name), 'w+')
            foobarfile.write(stdout.read())
            print "l20 success"
            foobarfile.close()
            ssh_l20.close()

        except Exception as e:
            print "l20 " + str(e)
            print "Oops, the program went tits up at the connection l20."

        try: # Create files for the l21 machine. same as above.

            l21_machine_name = str(int(drivernum) + 2) + "-qa-test" + str(driverlabelnum)
            port = 22
            transport_l21 = paramiko.Transport((l21_machine_name, port))
            transport_l21.connect(username='root', password='XXXXXXXXX')

            sftp_l21 = paramiko.SFTPClient.from_transport(transport_l21)
            filepath = '/var/log/messages'
            sftp_l21.get(filepath, directory_name + "messages_l21.txt", None)
            sftp_l21.close()

            ssh_l21 = paramiko.SSHClient()
            ssh_l21.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_l21.connect(l21_machine_name, username='root', password='XXXXXXXX')
            inn,out,err = ssh_l21.exec_command('csd log --after "2 hours ago"')
            foobarfile = open('{}/l21_csdlog.txt'.format(directory_name), 'w+')
            foobarfile.write(out.read())
            print "l21 success"
            foobarfile.close()
            ssh_l21.close()

        except Exception as e:
            print "l21 " + str(e)
            print "Oops, the program went tits up at the connection to l21."

        try: # Create the files for the l30 machine. connects through docker instead of paramiko.
            l30_ip = ip
            l30_ip[3] = str(last_three_nums + 9)
            l30_ip_full = ""
            for element in l30_ip:
                l30_ip_full += element
                if len(element) != 3:
                    l30_ip_full += "."
            l30_docker = docker.Client(base_url="tcp://{}:13873".format(l30_ip_full), version="auto", timeout=180)

            stdout_l30 = l30_docker.execute("qa-test{}_L3".format(str(driverlabelnum)), "journalctl --no-pager -x --since='2 hours ago'")
            l30_journal = open('{}/l30_journalctl.txt'.format(directory_name), 'w+')
            l30_journal.write(stdout_l30)
            l30_journal.close()

            csd_log_l30 = l30_docker.execute("qa-test{}_L3".format(str(driverlabelnum)), "csd log --after '2 hours ago'")
            l30_csdlog = open('{}/l30_csd_log.txt'.format(directory_name), 'w+')
            l30_csdlog.write(str(csd_log_l30))
            print "L30 success \n"
            l30_csdlog.close()
        except Exception as e:
            print str(e)
            print "Bollocks, this (l30) container not available. Either change to the virtual IP (if set up as an HA machine) or this container" \
                  " is the failover machine."

        try: # same as above for l31.
            l31_ip = ip
            l31_ip[3] = str(last_three_nums + 12)
            l31_ip_full = ""
            for element in l31_ip:
                l31_ip_full += element
                if len(element) != 3:
                    l31_ip_full += "."
            l31_docker = docker.Client(base_url="tcp://{}:13873".format(l31_ip_full), version="auto", timeout=180)

            stdout_l31 = l31_docker.execute("qa-test{}_L3".format(str(driverlabelnum)), "journalctl --no-pager -x --since='2 hours ago'")
            l31_journal = open('{}/l31_journalctl.txt'.format(directory_name), 'w+')
            l31_journal.write(stdout_l31)
            l31_journal.close()

            csd_log_l31 = l31_docker.execute("qa-test{}_L3".format(str(driverlabelnum)), "csd log --after '2 hours ago'")
            l31_csdlog = open('{}/l31_csd_log.txt'.format(directory_name), 'w+')
            l31_csdlog.write(str(csd_log_l31))
            print "L31 success \n"
            l31_csdlog.close()

        except Exception as e:
            print str(e)
            print "Bollocks, this (l31) container not available. Either change to the virtual IP (if set up as an HA machine) or this container" \
                  " is the failover machine."

        # Creates the management files. Same format as in the above l30 and l31.
        mgmt_ip = ip
        mgmt_ip[3] = str(last_three_nums + 15)
        mgmt_ip_full = ""
        for element in mgmt_ip:
            mgmt_ip_full += element
            if len(element) != 3:
                mgmt_ip_full += "."
        mgmt_docker = docker.Client(base_url="tcp://{}:13873".format(mgmt_ip_full), version="auto", timeout=180)

        stdout_mgmt = mgmt_docker.execute("qa-test{}_mgmt".format(str(driverlabelnum)), "journalctl --no-pager -x --since='2 hours ago'")
        mgmt_journal = open('{}/mgmt_journalctl.txt'.format(directory_name), 'w+')
        mgmt_journal.write(stdout_mgmt)
        mgmt_journal.close()

        csd_log_mgmt = mgmt_docker.execute("qa-test{}_mgmt".format(str(driverlabelnum)), "csd log --after '2 hours ago'")
        mgmt_csdlog = open('{}/mgmt_csd_log.txt'.format(directory_name), 'w+')
        mgmt_csdlog.write(str(csd_log_mgmt))
        mgmt_csdlog.close()


        import subprocess
        # Getting  the database dump from the driver.
        db_dump = open('{}/dbdump.txt'.format(directory_name), 'w+')
        env = os.environ.copy()
        env['PGPASSWORD'] = 'XXXXXXX'
        foo1 = subprocess.Popen('pg_dump -h vm-postgres -d "qa-test{}db" -U "qatest" -a -x --disable-triggers'.format(str(driverlabelnum)), env=env, shell=True, stdout=subprocess.PIPE)
        foo = foo1.communicate()[0]
        db_dump.write(str(foo))
        db_dump.close()

        # # Getting the server.log on mgmt.
        serverlog = mgmt_docker.execute('qa-test{}_mgmt'.format(str(driverlabelnum)), 'cat /var/log/clearsky/server.log')
        slog = open('{}/webserver.log'.format(directory_name), 'w+')
        slog.write(str(serverlog))
        slog.close()


    # creates a list of bug objects representing individual errors, failures, and timeouts.
    def process_failure(cls, fail):
        print '\n\n-------------------- processing failures -------------------------\n\n'

        version = re.search("[A-Z]\d+v\d+(\.\d)?", os.environ['JOB_NAME'])

        # Gets the build environment by checking the Jenkins build environment variables.
        def get_env(v):
            env = list()
            # if v == '' or v is None:
            #     v = 'Not present. Check git hash. Maybe add in processing of full failure list!'
            #     env.append('version number => ' + v + '\n')
            env.append('node => ' + os.environ['NODE_NAME'] + '\n')
            env.append('url => ' + os.environ['BUILD_URL'] + '\n')
            env.append('timestamp => ' + os.environ['BUILD_ID'] + '\n')
            env.append('job name => ' + os.environ['JOB_NAME'] + '\n')
            env.append('build number => ' + os.environ['BUILD_NUMBER'] + '\n')
            envn = ""
            envn += "{noformat}"
            for line in env:
                envn += str(line)
            envn += "{noformat}"
            return envn
        environment = get_env(version)


        # creates the description field
        def get_desc(stack_trace):
            st = ""
            for line1 in stack_trace:
                st += str(line1)
            return st
        bug_list = list()
        tests_failed_dict = {}
        current_test = ""

        if not isinstance(fail[0], basestring):
            print str(fail[0])
            print str(fail.__class__), " ", str(fail[0].__class__)
            print  "NOT A STRING"
            return -1

        sum = ""

        # Get the sub section of text that you want for the description
        for line in fail:
            if "___ Test" in str(line) or "___ ERROR" in str(line) or "ERROR at " in str(line) or "ERROR in " in str(line):
                current_test = str(line)
                tests_failed_dict[current_test] = list()
                tests_failed_dict[current_test].append("{noformat}")
                tests_failed_dict[current_test].append(str(line))
            elif current_test is not "":
                tests_failed_dict.get(current_test).append(str(line) + "\n")
            if "E          " in line and "Error:" in line and "Traceback" not in line:
                if not line.replace(' ', '') in sum:
                    sum += line.replace(' ', '')

        # For each test sub-section create a bug and then return those bugs as a list to be processed.
        for test_failed in tests_failed_dict.keys():
            tests_failed_dict.get(test_failed).append("{noformat}")
            description = get_desc(tests_failed_dict.get(test_failed))
            bug_list.append(Bug(str(sum), str(version), str(environment), str(description), os.environ["BUILD_URL"], int(0)))

        print '\n\n-------------------- finished processing failures -------------------------\n\n'
        return bug_list

    # Method to find out whether or not the given bug is duplicated in JIRA.
    def is_duplicate(cls, bug):
        print '\n\n-------------------- checking for duplicates -------------------------\n\n'

        req_all = cls.my_server.search_issues('project=QABL')

        # Check each bug currently logged in JIRA for duplication.
        for issue_key in req_all:
            issue_name = cls.my_server.issue(id=issue_key)
            issue_desc = cls.my_server.issue(id=str(issue_key)).fields.description
            issue_repeat_count = cls.my_server.issue(id=str(issue_key)).fields.customfield_10301
            issue_repeat_us = cls.my_server.issue(id=str(issue_key)).fields.customfield_10300
            # TODO : update to check for regressions as well.
            print "\n\n", str(issue_name), " :: ", issue_repeat_count, " :: ", issue_repeat_us, "\n\n"
            if issue_desc is not None and issue_desc is not "":
                desc = bug.description.split('\n')
                errors = ""
                methods = ""
                filepath = ""
                # in the description of the bug being logged
                for line in desc:
                    if "Error: " in line:
                        errors += str(line)
                    elif "def " and ":" in line:
                        methods += line
                    elif ".py:" in line and "Error" in line:
                        filepath = line
                methods1 = ""
                errors1 = ""
                filepath1 = ""
                is_same_test = False
                # in the description of the bug being compared to
                for line in issue_desc.split('\n'):
                    if "___ ERROR" in line or "___ Test" in line or "Error at " in line or "Error in " in line:
                        if str(desc[0]).replace("{noformat}", '') == issue_desc.split('\n')[0].encode('ascii', 'ignore').replace('{noformat}', ''):
                            is_same_test = True
                    if "Error: " in line:
                        errors1 += line
                    elif "def " and ":" in line:
                        methods1 += line
                    elif ".py:" in line and "Error" in line:
                        filepath = line

                print "This is from the bug being logged :: \n" + desc[0] + " :::: " + str(desc[0].__class__) + " :::: " + str(desc[0]).replace("{noformat}", '')
                print "This is from the bug that it is being compared to :: \n" + issue_desc.split('\n')[0] + " :::: " + str(issue_desc.encode('ascii', 'ignore').__class__) # + " :::: \n" + issue_desc
                print "Were they the same? ::>> " + str(is_same_test)
                print "Errors: ", str(errors), "\nErrors 1: ", str(errors1)
                print "Methods: ", str(methods), "\nMethods 1: ", str(methods1)
                if (str(errors) == str(errors1) or str(methods) == str(methods1)) or (str(filepath1) == str(filepath)) and is_same_test:
                    if updated1 is not None: 
		    	updated1 = int(issue_repeat_count) + 1
                    else:
			updated1 = 1
		    for line in bug.environment.split('\n'):
                        if 'url => ' in line:
                            repeat_u = line.split('url => ', 1)
                            cls.my_server.issue(issue_name).update(customfield_10301=updated1)
                            cls.my_server.issue(issue_name).update(customfield_10300=str(repeat_u[1]))
                            break
                    return True

        print '\n\n-------------------- finished (F) checking for duplicates -------------------------\n\n'
        return False


    # Submits the bug to JIRA as a dictionary object, the jira module translates it into a valid json
    def submit_bug(cls, bug):
        print '\n\n-------------------- submitting bugs -------------------------\n\n'
        iss = cls.my_server.create_issue(fields=bug.json_dict['fields'])
        print str(iss)
        print '\n\n-------------------- results -------------------------\n\n'

# Main...
def main():
    print "\n\n-------------------- RUNNING BUG LOGGER -------------------------\n\n"
    b = Butler()
    b.log_bug_exec()
    try:
        for file in os.listdir('/home/csd-user/workspace/{}/'.format(os.environ['JOB_NAME'])):
            os.remove(file)
        print "\n\n-------------------- FINISHED BUG LOGGER -------------------------\n\n"
        if os.path.exists('/home/csd-user/workspace/{}/pyout.txt'.format(os.environ['JOB_NAME'])):
            os.remove('/home/csd-user/workspace/{}/pyout.txt'.format(os.environ['JOB_NAME']))
    except Exception as e:
        print str(e)

if __name__ == '__main__':
    main()





