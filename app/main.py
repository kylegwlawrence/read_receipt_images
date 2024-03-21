from functions import list_files, transform_image, detect_text, parse_ocr_data
import pandas as pd
import argparse

def main(args, raw_dir='.images/.raw_images', processed_dir='.images/.processed_images', markedup_dir='.images/.markedup_images'):
    file_name = args.file_name
    """
    pipeline to transform heic images to jpgs, store all jpgs in processed folder, run text detection
    model on each image, parse detection results, draw rectangles on images to visualize easyocr results,
    save drawn-on images to a markedup_dir and provide the ocr results in a dataframe.
    """
    transformed_file_name = transform_image(raw_dir, processed_dir, file_name)

    # detect text in image
    ocr_result = detect_text(processed_dir, transformed_file_name)

    # parse the results
    df = parse_ocr_data(processed_dir, markedup_dir, transformed_file_name, ocr_result)

    print('---First ten rows---')
    print(df.head(10))
    print('---Last ten rows---')
    print(df.tail(10))
    print('---info---')
    print(df.info())
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='detect text in an image file')
    parser.add_argument('--file_name', required=True, help='file_name (not path) from .images directory with extension')
    args = parser.parse_args()
    #payload = {
    #    'file_name': file_name
    #    , 'raw_dir':'.images'
    #    , 'processed_dir':'.processed_images'
    #    , 'markedup_dir':'.markedup_images'
    #    }
    df = main(args)

    print_extra = False
    if print_extra:
        for index, row in df.iterrows():
            text = row['text']
            if text == '':
                print(f'\nText for index {index}: {text} (text value is empty string)\n')
            elif text == None:
                print(f'\nText for index {index}: {text} (text value is None)\n')
            else:
                print(f'Text for index {index}: {text}')