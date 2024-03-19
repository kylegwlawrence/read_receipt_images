import os

# define directory where images are stored
images_dir = '.images'

# get list of files in directory
# instantiate list to store file names
files = []
# loop over DirEntry object with scandir
for entry in os.scandir(images_dir):
        if not entry.is_dir():
            # DirEntry method
            files.append(entry.name)
print(files)