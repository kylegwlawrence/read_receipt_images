import easyocr
import time

def detect_text(file_name:str):
    start_time = time.time()

    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    result = reader.readtext(file_name)
    print(result)

    print("--- %s seconds ---" % (time.time() - start_time))
