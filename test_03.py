import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path of working folder on Disk
src_path = "D:\\image processing"

def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    # kernel = np.ones((1, 1), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "\\sakar.png", img)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "\\sakar01.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "\\sakar01.png"))

    # Remove template file
    #os.remove(temp)

    return result


#print('--- Start recognize text from image ---')
test = (get_string(src_path + "\\final_saved.png"))
print(test)
FIRST = "first.txt"
message = open(FIRST, 'w')
message.write(test)
message.close()

test_01 = test.split(", ")
if "sakar" in test:
    print("helloworld")

if "is" in test:
    print("a")
else:
    print("you made a mistake")
