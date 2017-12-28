import ui
import datetime
from dateutil import rrule
from enum import Enum
# Photo analysis
import appex
from PIL import Image
from PIL.ExifTags import TAGS
import clipboard


# Customization: Add your names here
class Names(Enum):
	CHILD1 = 'SM'
	CHILD2 = 'DO'
	CHILD3 = 'VM'
	
	
# Customization: Add your birthdays here
class Birthdays(Enum):
	CHILD1 = datetime.datetime(2017, 9, 8, 2, 44)
	CHILD2 = datetime.datetime(1982, 10, 22, 7, 20)
	CHILD3 = datetime.datetime(1986, 6, 9, 2, 42)
	
	
class BabyAge2:
	CHILDREN = dict([(Names.CHILD1.value, Birthdays.CHILD1.value), (Names.CHILD2.value, Birthdays.CHILD2.value), (Names.CHILD3.value, Birthdays.CHILD3.value)])
	
	# Init
	def __init__(self, dob):
		self.PYUI = self.__class__.__name__
		self._dob = dob
		self._now = datetime.datetime.now()
		self._now_img = None
		self._ui_init()
		self._ui_info('Please choose an action...')
		
	# Run App
	def run(self):
		self._appex_action(False)
		# info = self._images[0].info
		self._calc()
		self._ui_set_values()
		self._ui.present('sheet')
		
	# Init UI
	def _ui_init(self):
		self._ui = ui.load_view(self.PYUI)
		
		# Bind actions to class methods
		self._ui['button_child1'].action = self.button_child1_action
		self._ui['button_child2'].action = self.button_child2_action
		self._ui['button_child3'].action = self.button_child3_action
		self._ui['datepicker'].action = self.datepicker_action
		self._ui['button_appex'].action = self.button_appex_action
		self._ui['label_header'].text = 'Age for birthday ' + self._date_format(self._dob)
		
		# Set Button Captions
		for key, value in self.CHILDREN.items():
			if key == Names.CHILD1.value:
				self._ui['button_child1'].title = str(key)
			elif key == Names.CHILD2.value:
				self._ui['button_child2'].title = str(key)
			elif key == Names.CHILD3.value:
				self._ui['button_child3'].title = str(key)
				
		# Set text fields to output only
		self._ui['weeks'].enabled = False
		self._ui['months'].enabled = False
		self._ui['years'].enabled = False
		if appex.is_running_extension():
			self._ui['button_appex'].enabled = False
		
	def _calc(self):
		self._weeks = between_dates(rrule.WEEKLY, self._dob, self._now)
		self._months = between_dates(rrule.MONTHLY, self._dob, self._now)
		self._years = between_dates(rrule.YEARLY, self._dob, self._now)
		self._ui_set_values()
		
	def _ui_set_values(self):
		self._ui['weeks'].text = str(self._weeks) + '.'
		self._ui['months'].text = str(self._months) + '.'
		self._ui['years'].text = str(self._years) + '.'
		self._ui['datepicker'].date = self._dob
		
	# GUI Action Handlers
	def datepicker_action(self, sender):
		self._dob = sender.date
		if self._now == self._now_img:
			self._ui['label_header'].text = str('Age for selected birthday as of image creation date')
		else:
			self._ui['label_header'].text = str('Age for selected birthday as of today')
		self._ui_info('Birthday manually set: ' + self._date_format(self._dob))
		self._calc()
		
	def button_child1_action(self, sender):
		self._dob = Birthdays.CHILD1.value
		self._ui_info('Birthday ' + Names.CHILD1.value + ' set: ' + self._date_format(self._dob))
		self._button_action(sender)
		
	def button_child2_action(self, sender):
		self._dob = Birthdays.CHILD2.value
		self._ui_info('Birthday ' + Names.CHILD2.value + ' set: ' + self._date_format(self._dob))
		self._button_action(sender)
		
	def button_child3_action(self, sender):
		self._dob = Birthdays.CHILD3.value
		self._ui_info('Birthday ' + Names.CHILD3.value + ' set: ' + self._date_format(self._dob))
		self._button_action(sender)
		
	def button_appex_action(self, sender):
		self._appex_action(True)
		
	# Common Button Action Handler
	def _button_action(self, sender):
		self._ui = sender.superview
		
		if self._now == self._now_img:
			self._ui['label_header'].text = str(sender.title) + '\'s age as of image creation date'
		else:
			self._ui['label_header'].text = str(sender.title) + '\'s age as of today'
		self._calc()
		
	# App Extension: Script invoked via AppEx Share Screen
	def _appex_action(self, check=True):
		if not appex.is_running_extension():
			if check:
				self._ui_error('This script was not started from the shared app extension. Doing so one can see the Baby\'s age at image creation date.')
			return
		else:
			self._imagesPIL = self.get_appex_attachments('imagePIL')
			if self._imagesPIL:
				self._debug('type(_imagesPIL)', str(type(self._imagesPIL)))
				self._debug('type(_imagesPIL[0])', str(type(self._imagesPIL[0])))
				
			self._images = self.get_appex_attachments('image')
			if self._images:
				self._debug('type(_images)', str(type(self._images)))
				self._debug('type(_images[0])', str(type(self._images[0])))
				self._debug('_images[0]', str(self._images[0]))
				
				self._now_img = self.get_image_creation_date(self._images, 0)
				if self._now_img:
					self._now = self._now_img
					self._debug('EXIF.DateTimeOriginal', self._date_format(self._now))
					self._ui_info('Image creation date received from AppEx: ' + self._date_format(self._now))
					self._calc()
				else:
					self._ui_error('EXIF. DateTimeOriginal could not be converted into a date object.')
					
	# AppEx: Get attachments
	def get_appex_attachments(self, type):
		if type == 'imagePIL':
			items = appex.get_images()
		elif type == 'image':
			items = appex.get_attachments('public.jpeg')
		return items
		
	# AppEx: Get DateTimeOriginal from Image EXIF data
	def get_image_creation_date(self, images, index=0):
		if images:
			a = get_exif(images[index])
			if a.get('DateTimeOriginal'):
				crdate = a.get('DateTimeOriginal')
				self._debug('get_image_creation_date.crdate', crdate)
				return datetime.datetime.strptime(crdate, '%Y:%m:%d %H:%M:%S')
			# clipboard.set(self.msg)
			else:
				self._ui_error('No EXIF.DateTimeOriginal found')
				return None
		else:
			self._ui_error('No input image found')
			raise NoImageFound
			
	# Utilities
	def _date_format(self, date):
		return date.strftime('%d.%m.%Y %H:%M')
		
	def _debug(self, msg, value):
		print('DEBUG: ' + msg + ' => ' + value)
		
	def _ui_info(self, msg):
		self._ui['label_msg'].text_color = str('blue')
		self._ui['label_msg'].text = str(msg)
		
	def _ui_error(self, msg):
		self._ui['label_msg'].text_color = str('red')
		self._ui['label_msg'].text = str(msg)
		
		
# Avoid warnings due to dynamic binding
def datepicker_action(sender):
	pass
	
	
def button_child1_action(sender):
	pass
	
	
def button_child2_action(sender):
	pass
	
	
def button_child3_action(sender):
	pass
	
	
def button_appex_action(sender):
	pass
	
	
# Date Delta Calculation
def between_dates(rule, start_date, end_date):
	delta = rrule.rrule(rule, dtstart=start_date, until=end_date)
	return delta.count()
	
	
# Get Image EXIF data
def get_exif(fn):
	ret = {}
	i = Image.open(fn)
	info = i._getexif()
	for tag, value in info.items():
		decoded = TAGS.get(tag, tag)
		ret[decoded] = value
	return ret
	
	
def main():
	babyage = BabyAge2(Birthdays.CHILD1.value)
	babyage.run()
	
	
if __name__ == '__main__':
	main()
