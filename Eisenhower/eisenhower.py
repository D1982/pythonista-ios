
import reminders
import ui
import dialogs
import shelve
import datetime
from dateutil import rrule


DB_FILE = 'data/storage.db'


class MatrixView(ui.View):
  APP_NAME = 'Eisenhower Matrix'
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    settings = self.load('settings')
    if not settings:
      settings = {}
      settings['name'] = ''
      settings['max_items'] = 8 # Maximum number of items
    self.settings = settings
    
    self.main_view = self.create_main_view()


  def create_main_view(self):
    scroll = ui.ScrollView()
    scroll.name = self.APP_NAME
    scroll.width = self.width
    scroll.height = self.height
    scroll.background_color = 'white'
    scroll.content_size = (self.width, self.height)

    scroll.always_bounce_vertical = True
    scroll.always_bounce_horizontal = True
    
    close = lambda s: self.close()
    btni_close = ui.ButtonItem(title="Close", action=close)
    scroll.left_button_items = [btni_close]
    
    # btni_settings = ui.ButtonItem(
    #   title='Settings',
    #   action=self.settings_action
    # )
    # scroll.right_button_items = [
    #   btni_settings,
    # ]
    return scroll

  def load(self, key):
    try:
      with shelve.open(DB_FILE) as db:
      	data = db.get(key, None)
    except:
      data = None
    
    return data

def render(self):
  todo = reminders.get_reminders(completed=False)
  done = reminders.get_reminders(completed=True)
  
  text = ('TODO List\n=========')
  
  for r in todo:
    text = text + f'[ ]{r.title}'
  
  for r in done:
    text = text + f'[X]{r.title}'
    
    print(text)

if __name__ == '__main__':
  w, h = ui.get_screen_size()
  f = (0, 0, w, h)
  view = MatrixView(frame=f)
  view.present(style='sheet', hide_title_bar=False)
