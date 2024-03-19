import os
from PIL import Image
from pillow_heif import register_heif_opener

def list_files(directory:str) -> list:
    # get list of files in directory
    # instantiate list to store file names
    files = []
    # loop over DirEntry object with scandir
    for entry in os.scandir(images_dir):
            # filter out directories and duplicates
            if not entry.is_dir() and not entry.name.endswith('copy.JPG'):
                # DirEntry method
                files.append(entry.name)
    return files

def convert_heic_to_png(heic_file_name:str, heic_directory:str,  save_directory:str, saved_file_prefix:str='from_heic_') -> None:
    # convert an HEIC image to png
    register_heif_opener()
    image = Image.open(f'{heic_directory}/{heic_file_name}')
    image.save(f"{save_directory}/{saved_file_prefix}{heic_file_name.replace('.HEIC','.png')}", format('png'))

def convert_jpg_to_png(jpg_file_name:str, jpg_directory:str, save_directory:str, saved_file_prefix:str='from_jpg_'):
     # convert jpg image to png
    image = Image.open(f'{jpg_directory}/{jpg_file_name}')
    image.save(f"{save_directory}/{saved_file_prefix}{jpg_file_name.replace('.JPG','.png')}", format('png'))

if __name__=='__main__':
    # define directory where images are stored
    images_dir = '.images'
    # define directory where processed images will be written
    processed_images_dir = '.processed_images'
    # test a specific jpg image
    file_name = 'IMG_4633.JPG'
    convert_jpg_to_png(file_name, images_dir, processed_images_dir)
    