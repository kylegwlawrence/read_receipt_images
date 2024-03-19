import os
import shutil
from PIL import Image
import exif
from pillow_heif import register_heif_opener

def list_files(directory:str) -> list:
    # get list of files in directory
    # excludes copies
    # instantiate list to store file names
    files = []
    # loop over DirEntry object with scandir
    for entry in os.scandir(directory):
            # filter out directories and duplicates
            if not entry.is_dir() and not entry.name.endswith('copy.JPG'):
                # DirEntry method
                files.append(entry.name)
    return files

def copy_files_to_dir(files:list, copy_from:str, copy_to:str):
    # references list of file names and copies them from one directory to another
    for f in files:
        f = f'{copy_from}/{f}'
        print(f'copying {f} to {copy_to}')
        shutil.copy(f, copy_to)

def convert_heic_to_jpg(heic_directory:str, heic_file_name:str,  save_directory:str, saved_file_prefix:str='from_heic_') -> None:
    # converts HEIC image to JPG
    if file_name.endswith('.HEIC'):
        # convert an HEIC image to JPG
        register_heif_opener()
        image = Image.open(f'{heic_directory}/{heic_file_name}')
        print(f"original orientation for {file_name}: {image.info['original_orientation']}")
        if image.info['original_orientation']==3:
            image = image.rotate(90, expand=True)
        else:
            print(f'The orientation of {file_name} is not 3')
        new_image_name = f"{save_directory}/{saved_file_prefix}{heic_file_name.replace('.HEIC','.jpg')}"
        image.save(new_image_name)
        print(f"image saved to {new_image_name}")
    else:
        raise RuntimeError('File is not type HEIC')

def get_exif_data(directory:str, file_name:str):
    if file_name.upper().endswith('.JPG'):
        # use exif library to get exif data from a jpg image
        with open(f'{directory}/{file_name}', 'rb') as image_file:
            my_image = exif.Image(image_file)
            if my_image.has_exif:
                print(f'Image has exif data:\n {dir(my_image)}')
                print(f'orientation: {my_image["orientation"]}')
                if my_image["orientation"] == 3:
                    my_image["orientation"] = 5
            else:
                raise RuntimeError('Image does not have exif data.')
        with open(f'{directory}/{file_name}', 'wb') as transformed_image:
            transformed_image.write(my_image.get_file())
    else:
        raise RuntimeError('The file type must be JPG')

if __name__=='__main__':
    images_dir = '.images'
    file_name = 'IMG_4582.HEIC'
    saved_file_prefix = 'from_heic_'
    processed_images_dir = '.processed_images'

    #convert_heic_to_jpg(images_dir, file_name, processed_images_dir)
    #get_exif_data(processed_images_dir, f"{saved_file_prefix}{file_name.replace('HEIC','jpg')}")

    list_images = list_files(images_dir)
    jpgs = [image for image in list_images if image.upper().endswith('JPG')]
    copy_files_to_dir(jpgs, images_dir, processed_images_dir)
    #print(list_images)