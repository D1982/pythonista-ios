import datetime
from enum import Enum


# Customization: Add your names here
class Names(Enum):
	CHILD1 = 'CHILD1'
	CHILD2 = 'CHILD2'
	CHILD3 = 'CHILD3'
	
	
# Customization: Add your birthdays here
class Birthdays(Enum):
	CHILD1 = datetime.datetime(1900, 12, 31, 0, 00) # YYYY MM DD HH MM
	CHILD2 = datetime.datetime(1900, 12, 31, 0, 00) 
	CHILD3 = datetime.datetime(1900, 12, 31, 0, 00) 

class Contexts(Enum):
	TODAY = 'Today'
	IMAGE = 'Image'