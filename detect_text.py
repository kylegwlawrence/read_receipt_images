import easyocr
import time

start_time = time.time()
img = '.processed_images/from_heic_IMG_4519.jpg'

reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
result = reader.readtext(img)
print(result)

print("--- %s seconds ---" % (time.time() - start_time))