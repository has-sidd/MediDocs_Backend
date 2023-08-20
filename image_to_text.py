# import the necessary packages
from cv2 import rotate
import numpy as np
import cv2
import base64
import re
from datetime import datetime
import re
import pytesseract
import os



def base64toimage(encoded):
	decoded_data = base64.b64decode(encoded)
	filename = 'report_recieved.jpg'
	with open(filename, 'wb') as f:
		f.write(decoded_data)

	return True

def GetText(encoded):
	base64toimage(encoded)
	# image = cv2.imread('some_image.jpg')
	# cv2.imshow('Original image', image)
	# cv2.waitKey(1)
	# cv2.destroyAllWindows()

	# Image_rotation(image)
	# image1 = cv2.imread('0001.jpg')
	# outputText = CBC_OCR_AGU(image1)
	# print("CBC",outputText)
	# outputText = plasma_to_text()

	# image1 = cv2.imread('0001.jpg')
	# result = CBC_OCR_AGU(image1)
	# print("CBC",result)
	
	# output = plasma_to_text()
	image1 = cv2.imread('NIBD_CBC_3.jpg')
	# Grayscale, Gaussian blur, Otsu's threshold
	gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	# blur = cv2.GaussianBlur(gray, (3,3), 0)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	# Morph open to remove noise and invert image
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))	
	# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
	invert = 255 - thresh

	cv2.imshow('thresh', thresh)
	cv2.imshow('invert', invert)
	cv2.waitKey()

	image2 = cv2.imread('try.png')
	Image_rotation(image2)

	output = CBC_OCR_AGU(invert)

	return output


def Image_rotation(image):
	# convert the image to grayscale and flip the foreground and background to ensure foreground is now "white" and
	# the background is "black"

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)

	# threshold the image, setting all foreground pixels to
	# 255 and all background pixels to 0

	thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# cv2.imshow('Threshold image', thresh)
	# cv2.waitKey(1)

	# grab the (x, y) coordinates of all pixel values that
	# are greater than zero, then use these coordinates to
	# compute a rotated bounding box that contains all coordinates

	coords = np.column_stack(np.where(thresh > 0))
	angle = cv2.minAreaRect(coords)[-1]
	print("angle is",angle)
	# the `cv2.minAreaRect` function returns values in the
	# range [-90, 0); as the rectangle rotates clockwise the
	# returned angle trends to 0 -- in this special case we
	# need to add 90 degrees to the angle

	if angle < -45:
		angle = -(90 + angle)

	# otherwise, just take the inverse of the angle to make
	# it positive
	
	elif angle == 90:
		return
		
	else:
		angle = -angle

	# rotate the image to deskew it

	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

	# draw the correction angle on the image so we can validate it
	cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# show the output image
	print("[INFO] angle: {:.3f}".format(angle))
	cv2.imshow("Rotated", rotated)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	return rotated

def CBC_OCR_AGU(image):
	text = str(pytesseract.image_to_string(image, lang='eng', config='--psm 6'))
	
	return text



def Image_to_text():
	
	image = cv2.imread('sample2.jpg')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)

	# threshold the image, setting all foreground pixels to
	# 255 and all background pixels to 0

	thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	text = str(pytesseract.image_to_string(image, config='--psm 4'))
	print("text would be",text)

	return