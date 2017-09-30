import unicodecsv

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'


def read_cvs(filename):
	with open(filename, 'rb') as f:
	    reader = unicodecsv.DictReader(f)
	    return list(reader)


enrollments = read_cvs(enrollments_filename)
daily_engagement = read_cvs(engagement_filename)
project_submissions = read_cvs(submissions_filename)

print enrollments[0]
print daily_engagement[0]
print project_submissions[0]