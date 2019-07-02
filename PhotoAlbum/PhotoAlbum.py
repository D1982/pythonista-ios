import photos
import time
import ui
import appex
import os

FIRE = True
SLEEP = 0.5

class PhotoAlbum:
	
	def __init__(self, mode='ui'):
		self.PYUI = self.__class__.__name__
		self._mode = mode
		if self._mode == 'ui':
			self._ui_init()

	""" Initialize UI components """
	def _ui_init(self):
		self._ui = ui.load_view(self.PYUI)
		
		# Bind actions to class methods
		self._ui['button_list_albums'].action = self.button_list_albums_action
		self._ui['button_count_albums'].action = self.button_count_albums_action
		self._ui['button_delete_albums'].action = self.button_delete_albums_action
		self._ui['button_batch_delete_albums'].action = self.button_batch_delete_albums_action

		
	""" Refresh UI with latest data """
	def _ui_refresh(self):
		self._ui['textview_log'].text = '' 
	
	def _msg (self, text, type='i', prnt=True, linesep=True):
			if linesep is True:
				linesep = os.linesep
			else:
				linesep = ''

			log = self._ui['textview_log']		
			log.text = log.text + linesep + text
			if prnt is True:
				print(text)
	
	""" Run the Appex Code """
	def _appex_action():
		pass
	
	""" Run the App """
	def run(self):
		if appex.is_running_extension():
			self._appex_action()
		self._ui.present('sheet')
	
	""" Get the Albums of interest """
	def get_albums(self):
		albums = photos.get_albums()
		return albums

	""" Analyze an album (Asset Collection) """
	def analyze_album(self, index, album):
		
		title = album.title
		length = len(album.assets)
			
		if length == 0 and album.can_delete is True:
			action = 'DELETE'
			comment = 'Deletable'
		elif length == 0 and a.can_delete is False:
			action = 'IGNORE'
			comment = 'Undeletable'
		elif length > 0:
			action = 'IGNORE'
			comment = 'Not in scope'
		else:
			action = 'N.A.'
			comment = 'Error'
		
		metadata = dict()
		metadata['index'] = index
		metadata['title'] = title
		metadata['length'] = length
		metadata['action'] = action
		metadata['comment'] = comment	

		return metadata

	""" Print version of an album """
	def str_albums(self, albums):
		lst = '<<Albums>>'
		for k,a in enumerate(albums):
			i = self.analyze_album(k, a)
			lst = lst + os.linesep + i['title']
		return lst

	""" Delete albums (interactive or as batch) """
	def delete_albums(self, batch=False):
		self._ui_refresh()
		albums = self.get_albums()
		print(type(albums))

		
		# Creata a collection representing all candidates to be deleted
		del_albums = albums.copy() # self.get_albums()
		for k,a in enumerate(albums):
			# Get the album metadata
			i = self.analyze_album(k, a)
			# Remove element if the album contains photos
			if i['length'] > 0:
				del del_albums[k]

		# Finally delete interactively or as batch
		if batch is False:
			self._msg('Preparing interactive delete of albums ...')
			if FIRE is True:
				# Delete albums in an iteration
				for k,a in enumerate(del_albums):
					# Get the album metadata
					i = self.analyze_album(k, a)
					if i['action'] == 'DELETE':
						try:
							self._msg('Trying to delete {t}...'.format(t=i['title']))
							a.delete()
							time.sleep(SLEEP)
							self._msg(text='Finished', linesep=False)
						except Exception as ex:
							self._msg('Error: ' + str(ex))
							self._msg(os.linesep + '{l}'.format(l=self.str_albums(del_albums)))

				self._msg(os.linesep + '{l}'.format(l=self.str_albums(del_albums)))

		elif batch is True:
			self._msg('Preparing batch delete of albums...')
			if FIRE is True:
				try:
					self._msg('Trying to delete all albums at once...')
					print(type(del_albums))
					# photos.batch_delete(del_albums)
					self._msg(text='Not yet supported', linesep=False)
					self._msg(os.linesep + '{l}'.format(l=self.str_albums(del_albums)))
				except Exception as ex:
					self._msg('Error: ' + str(ex))
					self._msg(os.linesep + '{l}'.format(l=self.str_albums(del_albums)))


		if FIRE is False:
			self._msg('... Skipped due to test mode!')
			self._msg(os.linesep + '{l}'.format(l=self.str_albums(del_albums)))

	""" Button Action: List all albums + metadata """
	def button_list_albums_action(self, sender):
		self._ui_refresh()
		albums = self.get_albums()
		for k,a in enumerate(albums):
			# Get the album metadata
			i = self.analyze_album(k, a)
			# Prepare a formatted string of the metadata Result
			text = 'A:{a}, L:{l}, T:{t}, No:{n}'.format(
				a=i['action'], l=str(i['length']), t=i['title'], n=i['index'])			
			# Put message to the TextView 
			self._msg(text)
	
	""" Button Action: Count all albums + stats """
	def button_count_albums_action(self, sender):
		self._ui_refresh()
		albums = self.get_albums()

		cnt = 0
		cnt_empty = 0

		for k,a in enumerate(albums):
			# Get the album metadata
			i = self.analyze_album(k, a)
			if i['length'] == 0:
				cnt_empty += 1
			else:
				cnt += 1		
		# Put message to the TextView
		self._msg('{t} album(s) => {e} are empty'.format(e=str(cnt_empty), t=str(cnt + cnt_empty)))

	""" Button Action: Delete all albums (interactively) """
	def button_delete_albums_action(self, sender):
		self._ui_refresh()
		self.delete_albums(batch=False)

	""" Button Action: Delete all albums (at once as batch) """
	def button_batch_delete_albums_action(self, sender):
		self._ui_refresh()
		self.delete_albums(batch=True)

""" Avoid warnings due to dynamic binding using function stubs """
def button_list_albums_action(sender):
	pass

def button_count_albums_action(sender):
	pass
	
def button_delete_albums_action(sender, batch=False):
	pass

def button_batch_delete_albums_action(sender, batch=False):
	pass

""" Run the code """
def main():
	pa = PhotoAlbum('ui')
	pa.run()
	
if __name__ == '__main__':
	main()

