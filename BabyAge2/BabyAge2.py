import ui
import datetime
from dateutil import rrule


class BabyAge

	DOB

	weeks = null
	months = null
	years = null

	def between_dates(rule, start_date, end_date):
		weeks = rrule.rrule(rule, dtstart=start_date, until=end_date)
		return weeks.count()

	DOB = datetime.datetime.now()
	NOW = datetime.datetime.now()

	full_weeks = (NOW - DOB).days/7

	weeks = between_dates(rrule.WEEKLY, DOB, NOW)
	months = between_dates(rrule.MONTHLY, DOB, NOW)
	years = between_dates(rrule.YEARLY, DOB, NOW)

	#print 'Full weeks {}'.format(full_weeks)
	#print '{}th week'.format(weeks)
	#print 'Months {}'.format(months)

	def button_smilla_action(sender):
		v = sender.superview
		DOB = datetime.datetime(2017, 9, 8, 2, 44)
		v['datepicker'].date = DOB
		calc()
		display()
		
		
	def datepicker_action(sender):
		dob = sender.date
		calc()
		
	def calc():
		weeks = between_dates(rrule.WEEKLY, dob, NOW)
		months = between_dates(rrule.MONTHLY, dob, NOW)
		years = between_dates(rrule.YEARLY, dob, NOW)
		
	def display():
		v = ui.load_view('BabyAge2')
		
		v['weeks'].text = str(weeks) + '.'
		v['months'].text = str(months) + '.'
		v['years'].text = str(years) + '.'
		


		v['datepicker'].date = DOB
		v['weeks'].enabled = False
		v['months'].enabled = False
		v['years'].enabled = False
		v['weeks'].text = str(weeks) + '.'
		v['months'].text = str(months) + '.'
		v['years'].text = str(years) + '.'
		
		v.present('sheet')
		
	def main():
		display()

if __name__ == '__main__':
  main()