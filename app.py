import os
import shutil
from PIL import Image, ImageDraw, ExifTags
from pillow_heif import register_heif_opener
import pandas as pd
import easyocr
import time
import sys

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
    
def transform_image(from_dir, to_dir, file_name) -> str:
    """
    Performs some transformation on an image in the from_dir then stores it in the to_dir.

        Parameters:
            from_dir (str): directory where raw image is stored
            to_dir (str): directory where transformed image will be stored
            file_name (str): name of the file in from_dir

        Returns:
            str: file name for the transformed image in to_dir
    """
    # copy jpg file_name from raw directory to processed directory
    if file_name.upper().endswith('JPG') and not file_name.upper().endswith('COPY.JPG'):
        file_path = f'{from_dir}/{file_name}'
        image = Image.open(file_path)
        img_exif = image.getexif()
        exif_dict = {}
        if img_exif is None:
            print('Sorry, image has no exif data.')
        else:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    exif_dict[ExifTags.TAGS[key]] = val
                    #print('--Keys are in ExifTags--')
                    #print(f'{ExifTags.TAGS[key]}:{val}')
                else:
                    exif_dict[key] = val
                    #print(f'{key}:{val}')
        print(exif_dict)
        if 'Orientation' in exif_dict:
            orientation = exif_dict['Orientation']
            print(f'image orientation from exif data is {orientation}')
            if orientation == 6:
                image=image.rotate(270, expand=True)
        else:
            print('There is no Orientation key in exif data')
        #print(f'Information for {file_path}: {image.info}')
        # save the file in to_dir
        new_file_name = file_name.lower()
        image.save(f"{to_dir}/{new_file_name}")
        print(f"Transformed image saved to {new_file_name}")
        return new_file_name
    # do some transformation if it is an HEIC file
    elif file_name.upper().endswith('HEIC'):
        # convert an HEIC image to JPG
        register_heif_opener()
        image = Image.open(f'{from_dir}/{file_name}')
        print(f"original orientation for {file_name}: {image.info['original_orientation']}")
        # rotate the image to its correct orientation
        if image.info['original_orientation']==3:
            image = image.rotate(90, expand=True)
        else:
            print(f'The orientation of {file_name} is not 3')
        # save the file in to_dir
        new_file_name = file_name.replace('.HEIC','.JPG').lower()
        image.save(f"{to_dir}/{new_file_name}")
        print(f"image saved to {new_file_name}")
        return new_file_name
    else:
        raise RuntimeError(f'File {from_dir}/{file_name} is not type HEIC or JPG')
    
def detect_text(dir, file_name:str) -> list:
    """
    Detects text in the image

        Parameters:
            dir (str): directory where image is stored. 
            file_name (str): name of the file in dir. Must include .jpg file type in name.

        Returns:
            list: result from the easyocr detector
    """
    start_time = time.time()
    file_path = f"{dir}/{file_name}"
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    try:
        result = reader.readtext(file_path)
        return result
    except Exception as e:
        print(f'readtext failed for {file_name}\n {e}')
    finally:
        print("--- %s seconds ---" % (time.time() - start_time))

def parse_ocr_data(from_dir, to_dir, file_name:str, ocr_result:list) -> pd.DataFrame:
    """
    Parses the easyocr detection results into a df, marks up the image with boxes
    for each dtected text, and stores markedup images in a separate directory

        Parameters:
            from_dir (str): directory where transformed image is stored
            to_dir (str): directory where marked up image will be stored
            file_name (str): name of the file associated with the ocr_result
            ocr_result (str): the list of results from the easyocr detector

        Returns:
            pd.DataFrame: detected text, confidence, coordinates, and file path

    """
    if ocr_result==None:
        print('There is no data in the ocr result')
        return None
    text = []
    confidence = []
    coordinates = []
    words = {'text':text, 'confidence':confidence, 'coordinates':coordinates}
    # iterate over the words detected
    for i in ocr_result[0:len(ocr_result)+1]:
        ocr_text = i[1]
        ocr_confidence = i[2]
        ocr_coordinates = (i[0][0][0], i[0][0][1], i[0][2][0], i[0][2][1])
        words['text'].append(ocr_text)
        words['confidence'].append(ocr_confidence)
        words['coordinates'].append(ocr_coordinates)

    # store results in a dataframe
    df = pd.DataFrame.from_dict(words)
    df = df.sort_values(by='confidence', ascending=False)
    df['filepath'] = f"{to_dir}/{file_name}"
    df.reset_index(inplace=True, names='id')

    # draw boxes on the image
    img = Image.open(f"{from_dir}/{file_name}")
    draw = ImageDraw.Draw(img)
    for index, row in df.iterrows():
        coords = row['coordinates']
        draw.rectangle(coords, outline=(255, 0, 0)) # first and third elements of coordinates in tuple of ocr data

    # save marked up image
    img.save(f"{to_dir}/{file_name}")

    return df
    
def read_expenses(file:str='Budget - Expenses.csv'):
    # ingest the expenses sheet from a local csv and do some transformation
    df = pd.read_csv(file, usecols=[0,2,3,4,5,6])
    new_col_names = {
        'Purchase Date (mm-dd-yy)':'purchase_date'
        ,'Item_lowercase':'item'
        ,'Price':'price'
        ,'Receipt Number':'receipt_number'
        ,'Biz Name':'business_name'
        ,'IS CAD':'is_cad'
        }
    df.rename(columns=new_col_names, inplace=True)
    df['receipt_number'] = df['receipt_number'].astype("Int64")
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], format='%m/%d/%Y')
    for col in ['item','business_name']:
        df[col] = df[col].str.lower()
    return df