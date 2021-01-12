import appex
import photos
import datetime

from PIL import Image
from PIL.ExifTags import TAGS
from dateutil import rrule


def strdate(date):
    """Create a nicely formatted date string (Example: TUE, 12.01.2021 20:55)"""
    return date.strftime('%d.%m.%Y %H:%M')


def between_dates(rule, start_date, end_date):
    """ Calculate the delta between two dates in days"""
    delta = rrule.rrule(rule, dtstart=start_date, until=end_date)
    return delta.count()


def get_exif(fn):
    """Get Image EXIF data"""
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


def get_appex_attachments(self, type):
    """AppEx: Get attachments"""
    if type == 'imagePIL':
        items = appex.get_images()
    elif type == 'image':
        items = appex.get_attachments(
            'public.jpeg')
    return items


def get_image_creation_date(self, images, index=0):
    """AppEx: Get DateTimeOriginal from Image EXIF data"""
    if images:
        try:
            a = get_exif(images[index])
        except AttributeError:
            print('AttributeError occured')
            raiseNoEXIFDataError('get_exif(images[index])', 'No EXIF data was found')
        if a.get('DateTimeOriginal'):
            crdate = a.get('DateTimeOriginal')
            return datetime.datetime.strptime(crdate, '%Y:%m:%d %H:%M:%S')
        else:
            print('No EXIF.DateTimeOriginal found')
            return None
    else:
        print('')
        raise Exception('No input image found')