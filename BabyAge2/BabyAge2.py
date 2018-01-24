import ui
import datetime
import clipboard
import appex
import photos
from dateutil import rrule
from enum import Enum
from PIL import Image
from PIL.ExifTags import TAGS



# Customization: Add your names here
class Names(Enum):
	CHILD1 = 'CHILD1'
	CHILD2 = 'CHILD2'
	CHILD3 = 'CHILD3'
	
	
# Customization: Add your birthdays here
class Birthdays(Enum):
	CHILD1 = datetime.datetime(2017, 9, 8, 2, 44)
	CHILD2 = datetime.datetime(1982, 10, 22, 7, 20)
	CHILD3 = datetime.datetime(1986, 6, 9, 2, 42)
	

class Contexts(Enum):
	TODAY = 'Today'
	IMAGE = 'Image'

	
class BabyAge2:
	CHILDREN = dict([(Names.CHILD1.value, Birthdays.CHILD1.value), (Names.CHILD2.value, Birthdays.CHILD2.value), (Names.CHILD3.value, Birthdays.CHILD3.value)])
	
	# Initialization
	def __init__(self, name, dob):
		self.PYUI = self.__class__.__name__
		self._name = name
		self._dob = dob
		self._now = datetime.datetime.now()
		self._now_img = None
		self._context = None
		self._ui_init()

	def _ui_init(self):
		self._ui = ui.load_view(self.PYUI)
		
		# Bind actions to class methods
		self._ui['button_pick_image'].action = self.button_pick_image_action
		self._ui['button_child1'].action = self.button_child1_action
		self._ui['button_child2'].action = self.button_child2_action
		self._ui['button_child3'].action = self.button_child3_action
		self._ui['datepicker_now'].action = self.datepicker_now_action
		self._ui['datepicker_dob'].action = self.datepicker_dob_action
		self._ui['seg_cntrl_now'].action = self.seg_cntrl_now_action

		# Set button caption
		for key, value in self.CHILDREN.items():
			if key == Names.CHILD1.value:
				self._ui['button_child1'].title = str(key)
			elif key == Names.CHILD2.value:
				self._ui['button_child2'].title = str(key)
			elif key == Names.CHILD3.value:
				self._ui['button_child3'].title = str(key)
		
		self._ui['text_name'].enabled = False
		self._ui['text_name'].text = self._name
		self._ui_set_context(Contexts.TODAY.value, freeze=True)	
		
	def _ui_refresh(self):
		self._ui['label_age'].text = 'Week: ' + str(self._weeks) +', Month: ' + str(self._months) + ', Year: ' + str(self._years)
		self._ui['datepicker_dob'].date = self._dob
		self._ui['text_name'].text = self._name
		
		if self._ui['seg_cntrl_now'].selected_index <= 0:
			self._ui['label_now_detail'].text = 'Now'
		else:
			self._ui['label_now_detail'].text = 'Image'
		self._ui['label_dob_detail'].text = self._name
		
		if self._now == self._now_img:
			self._ui['datepicker_now'].date = self._now_img
			self._ui['label_now_detail'].text = 'Image: ' + self._strdate(self._now_img)
		else:
			self._ui['datepicker_now'].date = self._now
			if self._now.date() != datetime.datetime.now().date():
				self._ui['label_now_detail'].text = 'Custom'
			
	def _ui_set_context(self, context, freeze=False):
		self._context = context
		if context == Contexts.TODAY.value:
			idx = 0
		elif context == Contexts.IMAGE.value:
			idx = 1
		enabled = not freeze
		self._ui['seg_cntrl_now'].enabled = enabled
		self._ui['seg_cntrl_now'].selected_index = idx

	# Run App 
	def run(self):
		if appex.is_running_extension():
			self._appex_action()
		self._calc()
		self._ui_refresh()
		self._ui.present('sheet')

	def _calc(self):
		self._weeks = between_dates(rrule.WEEKLY, self._dob, self._now)
		self._months = between_dates(rrule.MONTHLY, self._dob, self._now)
		self._years = between_dates(rrule.YEARLY, self._dob, self._now)		
		self._ui_refresh()
		
	# UI Action Handlers
	def datepicker_now_action(self, sender):
		self._now = sender.date
		self._info_msg('Today manually set: ' + self._strdate(self._now))
		self._calc()

	def datepicker_dob_action(self, sender):
		self._name = 'Unknown'
		self._dob = sender.date
		self._info_msg('Birthday manually set: ' + self._strdate(self._dob))
		self._calc()

	def button_pick_image_action(self, sender):
		self.pick_image_action(sender)

	def button_child1_action(self, sender):
		self._name = Names.CHILD1.value
		self._dob = Birthdays.CHILD1.value
		self._button_action(sender)
		
	def button_child2_action(self, sender):
		self._name = Names.CHILD2.value
		self._dob = Birthdays.CHILD2.value
		self._button_action(sender)
		
	def button_child3_action(self, sender):
		self._name = Names.CHILD3.value
		self._dob = Birthdays.CHILD3.value
		self._button_action(sender)
		
	def seg_cntrl_now_action(self, sender):
		if sender.selected_index <= 0:
			self._now = datetime.datetime.now()
		else:
			# TODO: Check for image (or pick one) here
			if not self._now_img:
				self.pick_image_action(sender)	
			if self._now_img:
				self._now = self._now_img
		self._calc()
		
	def pick_image_action(self, sender):
		albums = photos.get_smart_albums()
		if albums:
			for album in albums:
				if album.title.lower() == 'camera roll':
					assets = album			
			if assets:
				asset = photos.pick_asset(assets = assets, title = 'Pick a photo ...')
			else:
				asset = photos.pick_asset()	
			if asset:
			# imageView.image = asset.get_ui_image()
				crdate = asset.creation_date
				if crdate:
					self._now_img = crdate
					self._now = self._now_img
					imageView = self._ui['ImageView']
					imageView.image = asset.get_ui_image(size=[imageView.x, imageView.y], crop=False)
					self._info_msg('Image selected')
					self._ui_set_context(Contexts.IMAGE.value)
					self._calc()
					self._button_action(sender)
		
	# Common Button Action Handler
	def _button_action(self, sender):
		self._ui = sender.superview
		self._info_msg('Birthday ' + self._name + ' set: ' + self._strdate(self._dob))	
		self._calc()
		
	# App Extension: Script invoked via AppEx Share Screen
	def _appex_action(self):
		if not appex.is_running_extension():
			self._err_msg('This script was not started from the shared app extension (AppEx). This allows to see the Baby\'s age at image creation date.')
			return
		else:
			# Set image
			imgView = self._ui['ImageView']
			imgView.image = ui.Image.from_data(appex.get_image_data())
			self._images = self.get_appex_attachments('image')
			if self._images:
				try:
					self._now_img = 						self.get_image_creation_date(self._images, 0)
				except NoEXIFDataError as ex:
					print(ex.expr + ' -> ' + ex.msg)
				if self._now_img:
					self._now = self._now_img
					self._debug('EXIF.DateTimeOriginal', self._strdate(self._now))
					self._info_msg('Image creation date received from AppEx: ' + self._strdate(self._now))
					self._ui_set_context(Contexts.IMAGE.value)	
					self._calc()
				else:
					self._err_msg('EXIF.DateTimeOriginal could not be converted into a date object.')
					
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
			try:
				a = get_exif(images[index])
			except AttributeError:
				print('AttributeError occured')
				raise NoEXIFDataError('get_exif(images[index])', 'No EXIF data was found')
			if a.get('DateTimeOriginal'):
				crdate = a.get('DateTimeOriginal')
				self._debug('get_image_creation_date.crdate', crdate)
				return datetime.datetime.strptime(crdate, '%Y:%m:%d %H:%M:%S')
			# clipboard.set(self.msg)
			else:
				self._err_msg('No EXIF.DateTimeOriginal found')
				return None
		else:
			self._err_msg('No input image found')
			raise NoImageFound
			
	# Utilities
	def _strdate(self, date):
		return date.strftime('%d.%m.%Y %H:%M')
		
	def _debug(self, msg, value):
		print('DEBUG: ' + msg + ' => ' + value)
		
	def _info_msg(self, msg):
		self._ui['label_msg'].text_color = str('blue')
		self._ui['label_msg'].text = str(msg)
		
	def _err_msg(self, msg):
		self._ui['label_msg'].text_color = str('red')
		self._ui['label_msg'].text = str(msg)
		

class NoEXIFDataError(Exception):
    """Exception raised when there is no image EXIF data found.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

# Avoid warnings due to dynamic binding
def datepicker_now_action(sender):
	pass
	
def datepicker_dob_action(sender):
	pass

def button_pick_image_action(sender):
	pass
	
def button_child1_action(sender):
	pass
	
def button_child2_action(sender):
	pass
	
	
def button_child3_action(sender):
	pass
	
	
def pick_image_action(sender):
	pass
	
	
def seg_cntrl_now_action(sender):
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
	babyage = BabyAge2(Names.CHILD1.value, Birthdays.CHILD1.value)
	babyage.run()
	
	
if __name__ == '__main__':
	main()
