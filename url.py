# import requests
# import cv2
# import numpy as np
# from urllib.request import urlopen
#
# url = "http://192.168.1.65:8080/shot.jpg"
#
# while True:
#
#     img_resp = urlopen(url)
#     img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
#     img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
#
#     cv2.imshow("AndroidCam", img)
#
#     if cv2.waitKey(1) == 27:
#         break


# # import the necessary packages
# import numpy as np
# from urllib.request import urlopen
# import cv2
#
#
# # METHOD #1: OpenCV, NumPy, and urllib
# def url_to_image(url):
#     # download the image, convert it to a NumPy array, and then read
#     # it into OpenCV format
#     resp = urlopen(url)
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#
#     # return the image
#     return image
#
#
# # initialize the list of image URLs to download

#
# # loop over the image URLs
# for url in urls:
#     # download the image URL and display it
#     print("downloading %s" % (url))
#     image = url_to_image(url)
#     print(image)
#     print(type(image))
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)



# METHOD #2: scikit-image
from skimage import io
import cv2
urls = [
     "http://192.168.1.65:8080/shot.jpg",
     "https://www.pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png",
     "https://www.pyimagesearch.com/wp-content/uploads/2015/01/google_logo.png"
]
# loop over the image URLs
for url in urls:
    # download the image using scikit-image
    print("downloading %s" % (url))
    image = io.imread(url)
    print(type(image))
    cv2.imshow("Incorrect", image)
    cv2.imshow("Correct", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)