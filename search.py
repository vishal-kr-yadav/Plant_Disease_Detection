# import os
# os.chdir('D:/projects/Plant_Disease_Detection')

# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
ap.add_argument("-r", "--resultpath", required = True,
	help = "Path to the result path")
args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and describe it
query = cv2.imread(args["query"])
# query = cv2.imread('queries/GuavaAlgalSpot_7.png')
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
# searcher = Searcher("index.csv")
results = searcher.search(features)
results.pop(0)

# display the query
cv2.imshow("Query", query)

# loop over the results
for (score, resultID) in results:
	# load the result image and display it
	result = cv2.imread(resultID)
    #result = cv2.imread(resultID)
	cv2.imshow("Result", result)
	cv2.waitKey(0)