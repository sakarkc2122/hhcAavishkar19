# USAGE
# python text_detection_video_01.py --east frozen_east_text_detection.pb

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import imutils
import time
import cv2
import pytesseract
from PIL import Image
import mysql.connector



location_01=["BANESHWOR", "KOTESHWOR", "JADIBUTI","SINAMANGAL","GWARKO","BALKUMARI","LUBHU","PQR","ABC"]
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
    # os.remove(temp)

    return result
def decode_predictions(scores, geometry):
	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []

	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the
		# geometrical data used to derive potential bounding box
		# coordinates that surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability,
			# ignore it
			if scoresData[x] < args["min_confidence"]:
				continue

			# compute the offset factor as our resulting feature
			# maps will be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)

			# extract the rotation angle for the prediction and
			# then compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			# use the geometry volume to derive the width and height
			# of the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]

			# compute both the starting and ending (x, y)-coordinates
			# for the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)

			# add the bounding box coordinates and probability score
			# to our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# return a tuple of the bounding boxes and associated confidences
	return (rects, confidences)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-east", "--east", type=str, required=True,
	help="path to input EAST text detector")
ap.add_argument("-v", "--video", type=str,
	help="path to optinal input video file")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
	help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=640,
	help="resized image width (should be multiple of 32)")
ap.add_argument("-e", "--height", type=int, default=480,
	help="resized image height (should be multiple of 32)")
args = vars(ap.parse_args())

# initialize the original frame dimensions, new frame dimensions,
# and ratio between the dimensions
(W, H) = (None, None)
(newW, newH) = (args["width"], args["height"])
(rW, rH) = (None, None)

# define the two output layer names for the EAST detector model that
# we are interested -- the first is the output probabilities and the
# second can be used to derive the bounding box coordinates of text
layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]

# load the pre-trained EAST text detector
print("[INFO] loading EAST text detector...")
net = cv2.dnn.readNet(args["east"])

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# start the FPS throughput estimator
fps = FPS().start()

# loop over frames from the video stream
while True:
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="Hackathon"
	)

	# Read the data from mysql
	mycursor = mydb.cursor()
	mycursor.execute("SELECT distance1 FROM ultrasonic WHERE id=(SELECT MAX(id) FROM ultrasonic)")
	myresult = mycursor.fetchall()
	for x in myresult:
		distance1 = x[0]
		#distance2 = x[1]
	distance1 = float(distance1)
	#distance2 = int(distance2)
	# mydb.close()

	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame

	# check to see if we have reached the end of the stream
	if frame is None:
		break

	# resize the frame, maintaining the aspect ratio
	frame = imutils.resize(frame, width=1000)
	orig = frame.copy()

	# if our frame dimensions are None, we still need to compute the
	# ratio of old frame dimensions to new frame dimensions
	if W is None or H is None:
		(H, W) = frame.shape[:2]
		rW = W / float(newW)
		rH = H / float(newH)

	# resize the frame, this time ignoring aspect ratio
	frame = cv2.resize(frame, (newW, newH))

	# construct a blob from the frame and then perform a forward pass
	# of the model to obtain the two output layer sets
	blob = cv2.dnn.blobFromImage(frame, 1.0, (newW, newH),
		(123.68, 116.78, 103.94), swapRB=True, crop=False)
	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)

	# decode the predictions, then  apply non-maxima suppression to
	# suppress weak, overlapping bounding boxes
	(rects, confidences) = decode_predictions(scores, geometry)
	boxes = non_max_suppression(np.array(rects), probs=confidences)

	# loop over the bounding boxes
	for (startX, startY, endX, endY) in boxes:
		# scale the bounding box coordinates based on the respective
		# ratios
		print("initial: ", startX, endX, startY, endY)
		startX = int(startX * rW)
		startY = int(startY * rH)
		endX = int(endX * rW)
		endY = int(endY * rH)

		print("second: ", startX, endX, startY, endY)		# just to see
		print(rW, rH)										# just to see

		# draw the bounding box on the frame
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

	# update the FPS counter
	fps.update()

	# show the output frame
	cv2.imshow("Text Detection", orig)
	key = cv2.waitKey(1) & 0xFF

	# if the `s` key was pressed, save the image and crop the character detected frame

	cv2.imwrite(filename='saved_img.png', img=frame)
	im = Image.open(r"D:\\image processing\\saved_img.png")

	width, height = im.size
	print("img size: ", width, height)
	(rects, confidences) = decode_predictions(scores, geometry)
	boxes = non_max_suppression(np.array(rects), probs=confidences)

	startX = int(startX / rW)
	startY = int(startY / rH)
	endX = int(endX / rW)
	endY = int(endY / rH)

	im1 = im.crop((startX-15, startY-10, endX+10, endY+10))
	if (distance1):
		im1.save("D:\\image processing\\final_saved.png", "PNG")

		test = (get_string(src_path + "\\final_saved.png"))
		print(test)
		if test in location_01:
		# test_01 = test.split(", ")

			try:
				connection = mysql.connector.connect(host="localhost",
													 database="Hackathon",
													 user="root",
													 password="")
				mySql_insert_query = ("""INSERT INTO location(address) VALUES(%s)""", (test,))

				cursor = connection.cursor()
				cursor.execute(*mySql_insert_query)
				connection.commit()
				print(cursor.rowcount, "Record inserted successfully into Location")
				#cursor.close()

			except mysql.connector.Error as error:
				print("Failed to insert record into Location {}".format(error))

			finally:
				if (connection.is_connected()):
					connection.close()

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# if we are using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()

# otherwise, release the file pointer
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()