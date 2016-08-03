#!/usr/bin/python
from sys import argv
import zbar
import Image
import PythonMagick
import os
import time
import sys

if len(argv) < 2: exit(1)

sFileExt = ".png"

def ClearFile():
	try:
		os.remove("test" + sFileExt)
	except:
		pass

def GetBarcode(sFileName):
	sBarCode = ""
	# create a reader
	scanner = zbar.ImageScanner()

	# configure the reader
	scanner.parse_config('enable')

	# obtain image data
	#pil = Image.open(argv[1]).convert('L')
	pil = Image.open(sFileName).convert('L')
	width, height = pil.size
	raw = pil.tostring()

	# wrap image data
	image = zbar.Image(width, height, 'Y800', raw)

	# scan the image for barcodes
	scanner.scan(image)

	# extract results
	for symbol in image:
	    # do something useful with results
	    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
	    sBarCode = symbol.data
	    if sBarCode.find("-") > -1:
	    	aryBC = sBarCode.split("-")
	    	nOrderID = aryBC[0]
	    	nProductID = aryBC[1]
	    	if len(nOrderID) != 16:
	    		nOrderID = ""
	    		sBarCode = ""
	    else:
	    	print "Invalid scan: " + sBarCode

	# clean up
	del(image)
	
	return sBarCode

ClearFile()

#Use PythonMagik to convert the pdf to a tiff
img = PythonMagick.Image(argv[1])

# Try a raw return
print "raw check..."
img.write("test" + sFileExt)
sBC = GetBarcode("test" + sFileExt)

if sBC == "":
	print "enhance..."
	ClearFile()
	img.enhance()
	img.write("test" + sFileExt)
	sBC = GetBarcode("test" + sFileExt)

if sBC == "":
	print "sharpen..."
	ClearFile()
	img.sharpen()
	img.write("test" + sFileExt)
	sBC = GetBarcode("test" + sFileExt)

if sBC == "":
	print "despeckle..."
	ClearFile()
	img.despeckle()
	img.write("test" + sFileExt)
	sBC = GetBarcode("test" + sFileExt)

if sBC == "":
	print "rotate..."
	ClearFile()
	img.rotate(180)
	img.write("test" + sFileExt)
	sBC = GetBarcode("test" + sFileExt)

if sBC.find("-") > -1:
	aryBC = sBC.split("-")
	nOrderID = aryBC[0]
	nProductID = aryBC[1]
	print "O: " + nOrderID + " P: " + nProductID
else:
	print "failed to scan bar code..."
#time.sleep(10)
