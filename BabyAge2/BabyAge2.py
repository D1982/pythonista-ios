import ui
import datetime
from dateutil import rrule
from enum import Enum


# Customization: Add your names here
class Names(Enum):
    CHILD1 = 'SM'
    CHILD2 = 'DO'


# Customization: Add your birthdays here
class Birthdays(Enum):
    CHILD1 = datetime.datetime(2017, 9, 8, 2, 44)
    CHILD2 = datetime.datetime(1982, 10, 22, 7, 20)


class BabyAge2:
    CHILDREN = dict([(Names.CHILD1.value, Birthdays.CHILD1.value), (Names.CHILD2.value, Birthdays.CHILD2.value)])

    def __init__(self, dob):
        self.PYUI = self.__class__.__name__
        self._dob = dob
        self._now = datetime.datetime.now()
        self._ui_init()

    def datepicker_action(self, sender):
        self._dob = sender.date
        self._date_action(sender)

    def button_child1_action(self, sender):
        self._dob = Birthdays.CHILD1.value
        self._date_action(sender)

    def button_child2_action(self, sender):
        self._dob = Birthdays.CHILD2.value
        self._date_action(sender)

    def _date_action(self, sender):
        self._ui = sender.superview
        self._calc()

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

    def _ui_init(self):
        self._ui = ui.load_view(self.PYUI)

        # Bind actions to class methods
        self._ui['button_child1'].action = self.button_child1_action
        
        self._ui['button_child2'].action = self.button_child2_action
        
        self._ui['datepicker'].action = self.datepicker_action

        # Set Button Captions
        for key, value in self.CHILDREN.items():
            if key == Names.CHILD1.value:
                self._ui['button_child1'].title = str(key)
            elif key == Names.CHILD2.value:
               self._ui['button_child2'].title = str(key)

        # Set text fields to output only
        self._ui['weeks'].enabled = False
        self._ui['months'].enabled = False
        self._ui['years'].enabled = False

    def run(self):
        self._calc()
        self._ui_set_values()
        self._ui.present('sheet')


# Avoid warnings due to dynamic binding
def datepicker_action(sender):
    pass


def button_child1_action(sender):
    pass


def button_child2_action(sender):
    pass


# Date Delta Calculation
def between_dates(rule, start_date, end_date):
    delta = rrule.rrule(rule, dtstart=start_date, until=end_date)
    return delta.count()


def main():
    babyage = BabyAge2(Birthdays.CHILD1.value)
    babyage.run()


if __name__ == '__main__':
    main()
