# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import pytesseract
from image_to_text import *
from preprocessing import *
from flask import jsonify
import os

def txt_file(text):
	f = open("report.txt", "w")
	f.write(text)
	f.close()

def scanned_img(img):
	base64toimage(img)
	#Read the image and convert it to grayscale
	image = cv2.imread('report_recieved.jpg')
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	# image = cv2.resize(image, None, fx=0.6,fy=0.6)
	image = imutils.resize(image, height = 500)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#Now convert the grayscale image to binary image
	ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	#Now detect the contours
	cnts = cv2.findContours(binary.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			screenCnt = approx
			valid_img = True
			# break
		else:
			screenCnt = None
			valid_img = False

	if(valid_img == True):
		# draw contours on the original image
		cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

		# apply the four point transform to obtain a top-down
		warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

		# convert the warped image to grayscale, then threshold it to give it that 'black and white' paper effect
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

		print("STEP 3: Apply perspective transform")
		cv2.imshow("Outline", imutils.resize(image, height = 600))
		cv2.imshow("Scanned", imutils.resize(warped, height = 600))

		cv2.waitKey(0)
		cv2.destroyAllWindows()

		text = str(pytesseract.image_to_string(warped, lang='eng', config='--psm 6'))
		tokens = generate_tokens(text)
		# if os.path.exists('report_recieved.jpg'):
		# 	os.remove('report_recieved.jpg')
	else:
		tokens = None

	response = jsonify({'success': valid_img, 'tokens': tokens})

	return response
