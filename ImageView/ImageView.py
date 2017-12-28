# coding: utf-8

import photos, ui

@ui.in_background
def get_image(sender):
    view = sender.superview
    image = view['Image']
    try:
    	image.image = ui.Image.from_data(photos.pick_image(raw_data = True))
    except:
        view.close()
        raise

view = ui.View(background_color = '#FFFFFF')
view.add_subview(ui.Button(name = 'image button', frame = (0,0,80,32)))
view['image button'].action = get_image
view['image button'].title = 'Set image'
view.add_subview(ui.ImageView(name = 'Image', frame = (0,32,80,100)))
view.present()
