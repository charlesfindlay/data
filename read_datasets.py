import unicodecsv

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

def get_enrollment_record(accountNumber):
    for record in enrollments:
        if record['account_key'] == accountNumber:
            return record
    return None

def read_cvs(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def removeTestAccounts(data):
    response = []
    for record in data:
        if record['account_key'] not in udacity_test_accounts:
            response.append(record)
    return response

def withinOneWeek(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7


def removeTrialAccountCancels(data):
    newData = []
    for record in data:
        if record['account_key'] in paid_students:
            newData.append(record)
    
    return newData




enrollments = read_cvs(enrollments_filename)
daily_engagement = read_cvs(engagement_filename)
project_submissions = read_cvs(submissions_filename)

print enrollments[0]
print daily_engagement[0]
print project_submissions[0]

# convert data types
print "New section"
from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')
    
# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    
print enrollments[0]




# Clean up the data types in the engagement table
print "New section"
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
print daily_engagement[0]


# Clean up the data types in the submissions table
print "New section"
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

print project_submissions[0]

print "New section"
def rename_acct_to_account_key(list):
    for record in list:
        try:
            record['account_key'] = record['acct']
            del record['acct']
        except:
            pass
    

rename_acct_to_account_key(daily_engagement)
print daily_engagement[0]['account_key']


print "New section"
# count unique students in each file

def count_unique_students(file):
    uniqueStudents = set()
    for record in file:
       uniqueStudents.add(record['account_key'])
    
    return uniqueStudents

enrollment_num_rows = len(enrollments)
enrollment_num_unique_students = count_unique_students(enrollments)

submission_num_rows = len(project_submissions)
submission_num_unique_students = count_unique_students(project_submissions)

engagement_num_rows = len(daily_engagement)
engagement_num_unique_students = count_unique_students(daily_engagement)

print "Enrollments"
print enrollment_num_rows
print len(enrollment_num_unique_students)

print "Submissions"
print submission_num_rows
print len(submission_num_unique_students)

print "Engagement"
print engagement_num_rows
print len(engagement_num_unique_students)


# Surprising enrollment record
print "New section Surprising students"
for record in enrollment_num_unique_students:
    if record not in engagement_num_unique_students:
        student = get_enrollment_record(record)
        print student
        break

surprising_students = 0
for record in enrollments:
    if record['account_key'] not in engagement_num_unique_students:
        if record['days_to_cancel'] == None or record['days_to_cancel'] > 0:
            surprising_students += 1
            print record
        
print surprising_students

#
print "New section"
udacity_test_accounts = set()
for record in enrollments:
    if record['is_udacity']:
        udacity_test_accounts.add(record['account_key'])
        
print len(udacity_test_accounts)


# remove test accounts
print "New section -  remove test accounts"
cleanedEnrollments = removeTestAccounts(enrollments)
cleanedSubmissions = removeTestAccounts(project_submissions)
cleanedEngagements = removeTestAccounts(daily_engagement)
print len(cleanedEnrollments)
print len(cleanedSubmissions)
print len(cleanedEngagements)

# paid students
print "New section - paid students"
paid_students = {}
for record in cleanedEnrollments:
    if record['days_to_cancel'] == None or record['days_to_cancel'] > 7:
        accountKey = record['account_key']
        enrollDate = record['join_date']

        if accountKey not in paid_students or enrollDate > paid_students[accountKey]:
            paid_students[accountKey] =  enrollDate
        
print len(paid_students)


# paid students not trial accounts
print "New section - paid students not trial accounts"
paidEnrollments = removeTrialAccountCancels(cleanedEnrollments)
paidSubmissions = removeTrialAccountCancels(cleanedSubmissions)
paidEngagements = removeTrialAccountCancels(cleanedEngagements)

print len(cleanedEnrollments)
print len(cleanedSubmissions)
print len(cleanedEngagements)


# paid engagements within one week
print "New section - paid engagements within one week"
engagements_within_week_one = []
for record in paidEngagements:
    engagementDate = record['utc_date']
    key = record['account_key']
    joinDate = paid_students[key]
    if withinOneWeek(joinDate, engagementDate):
        engagements_within_week_one.append(record)


print len(engagements_within_week_one)


# engagement by account
print "New section - engagement by account"
from collections import defaultdict
print len(engagements_within_week_one)


engagement_by_account = defaultdict(list)
for engagement_record in engagements_within_week_one:
    account_key = engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)
    
print len(engagement_by_account)

# total minutes
total_minutes_by_account = {}

for account_key, engagement_for_student in engagement_by_account.items():
    total_minutes = 0
    for engagement_record in engagement_for_student:
        total_minutes += engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key] = total_minutes

# stats
print "New section - stats"

total_minutes = total_minutes_by_account.values()

import numpy as np

np.mean(total_minutes)
print "Mean:", np.mean(total_minutes)
print "Standard deviation:", np.std(total_minutes)
print "Minimum:", np.min(total_minutes)
print "Maximum:", np.max(total_minutes)





