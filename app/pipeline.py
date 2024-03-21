from functions import list_files, transform_image, detect_text, parse_ocr_data, main
import argparse

def pipeline(args, **kwargs):
    """
    Runs the file or files through the text detection pipeline

        Parameters:
            files_name (str or list): string for one file or list of multiple files to send through the pipeline
        
        Returns:
            pd.DataFrame: detected text, confidence, coordinates, and file path
    """
    file_names = args.file_names
   # if isinstance(file_names, str) and ',' not in file_names :
    #    file_names = [file_names]
    #elif not isinstance(file_names, list):
    #    raise TypeError('parameter file_names must be a string for one file name or a list of strings for multiple file names')
    for file in file_names:
        df = main(file, **kwargs)
        print(f'------Do something with this dateframe such as load to postgres------\n{df.head(3)}')
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='detect text in an image file')
    parser.add_argument('-f', '--file_names', required=True, help='file_names (not path) from .images directory with extension, or a space separated string of file names', metavar='N', type=str, nargs='+')
    args = parser.parse_args()

    pipeline(args)