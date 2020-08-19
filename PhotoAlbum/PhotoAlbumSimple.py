import photos

if __name__ == '__main__':
	photos.create_album('Test1')
	photos.create_album('Test2')
	
	albums = photos.get_albums()
	for k, a in enumerate(albums):
		if a.title in ('Test1', 'Test2'):
			print(f'Deleting album "{a.title}"...')
			a.delete()
			print(f'"{a.title}" is gone, dude!')
