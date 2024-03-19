import os
from PIL import Image
from pillow_heif import register_heif_opener

# define directory where images are stored
images_dir = '.images'

# get list of files in directory
# instantiate list to store file names
files = []
# loop over DirEntry object with scandir
for entry in os.scandir(images_dir):
        # filter out directories and duplicates
        if not entry.is_dir() and not entry.name.endswith('copy.JPG'):
            # DirEntry method
            files.append(entry.name)

# convert an HEIC image to png
register_heif_opener()

image = Image.open(f'{images_dir}/IMG_4511.HEIC')
image.save('.processed_images/from_heic_IMG_4511.png', format('png'))