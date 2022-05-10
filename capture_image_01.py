#capture images and read the character
#taken reference from https://www.pyimagesearch.com/

import cv2
import os
import numpy as np
import pytesseract
from PIL import Image
from time import sleep

key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)


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
    # os.remove(temp)

    return result

while True:

    try:
        src_path = "D:\\image processing"
        check, frame = webcam.read()
        print(check)  # prints true as long as the webcam is running
        print(frame)  # prints matrix values of each framecd
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='saved_img.png', img=frame)

            im = Image.open(r"D:\\image processing\\saved_img.png")

            width, height = im.size
            print("img size: ", width, height)
            # webcam.release()
            # print("Processing image...")
            # img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            # print("Converting RGB image to grayscale...")
            # gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)

            # print("Converted RGB image to grayscale...")
            # print("Resizing image to 28x28 scale...")
            # img_ = cv2.resize(gray, (28, 28))
            # print("Resized...")
            # img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            # print("Image saved!")

            test = (get_string(src_path + "\\saved_img.png"))
            print(test)
            FIRST = "first.txt"
            message = open(FIRST, 'w')
            message.write(test)
            message.close()
            break

        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break