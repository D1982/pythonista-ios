import ui
import datetime
from dateutil import rrule

def between_dates(rule, start_date, end_date):
		delta = rrule.rrule(rule, dtstart=start_date, until=end_date)
		return delta.count()

class BabyAge2:
	NOW = datetime.datetime.now()
	child1 = 'Smilla'
	dob = None
	vroot = None
	
	weeks = None
	months = None
	years = None
	full_weeks = None
	
	def __init__(self, dob):
		self.dob = dob
		
	def datepicker_action(self, sender):
		self.dob = sender.date
		self.calc()
		self.set()

	def button_child1_action(self, sender):
		self.dob = datetime.datetime(2017, 9, 8, 2, 44)
		v = sender.superview
		v['datepicker'].date = self.dob
		self.calc()
		self.set()
		
	def calc(self):
		self.weeks = between_dates(rrule.WEEKLY, self.dob, self.NOW)
		self.months = between_dates(rrule.MONTHLY, self.dob, self.NOW)
		self.years = between_dates(rrule.YEARLY, self.dob, self.NOW)
		
	def set(self):
		self.vroot['weeks'].text = str(self.weeks) + '.'
		self.vroot['months'].text = str(self.months) + '.'
		self.vroot['years'].text = str(self.years) + '.'
		
	def display(self):
		self.vroot = ui.load_view('BabyAge2')
		
		# Bind actions to class methods
		self.vroot['button_child1'].action = self.button_child1_action
		
		self.vroot['button_child1'].title = self.child1
			
		self.vroot['datepicker'].action = self.datepicker_action
		
		self.vroot['datepicker'].date = self.dob
		
		self.vroot['weeks'].enabled = False
		self.vroot['months'].enabled = False
		self.vroot['years'].enabled = False
		
		self.vroot.present('sheet')

# Avoid warnings due to dynamic binding
def datepicker_action(sender):
	pass
	
def button_child1_action(sender):
	pass
		
def main():
	babyage = BabyAge2(datetime.datetime(1982, 10, 22, 7, 20))
	babyage.calc()
	babyage.display()

if __name__ == '__main__':
  main()
