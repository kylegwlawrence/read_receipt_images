# operate this file for one image
# so iterate over list of files and execute main for each file
# copy_files_files to dir should be copy one jpg file to dir
# alternatively could have a function called transform_image which
# would transform the HEIC image and move to processed folder
# and then just move jpgs to processed folder
# big TO DO: why can't detect-text be run on an original JPG image? issue with cv2

from app import list_files, transform_image, detect_text, parse_ocr_data
import pandas as pd

def main(raw_dir, processed_dir, markedup_dir, file_name):
    """
    pipeline to transform heic images to jpgs, store all jpgs in processed folder, run text detection
    model on each image, parse detection results, draw rectangles on images to visualize easyocr results,
    save drawn-on images to a markedup_dir and provide the ocr results in a dataframe.
    """
    # transform JPG and HEIC files ansd store in another directory
    transformed_file_name = transform_image(raw_dir, processed_dir, file_name)

    # detect text in image
    ocr_result = detect_text(processed_dir, transformed_file_name)

    # parse the results
    df = parse_ocr_data(processed_dir, markedup_dir, transformed_file_name, ocr_result)

    return df

if __name__ == '__main__':
    file_name = 'IMG_4557.HEIC'
    payload = {
        'file_name': file_name
        , 'raw_dir':'.images'
        , 'processed_dir':'.processed_images'
        , 'markedup_dir':'.markedup_images'
        }
    df = main(**payload)
    print('---First ten rows---')
    print(df.head(10))
    print('---Last ten rows---')
    print(df.tail(10))
    print('---info---')
    print(df.info())