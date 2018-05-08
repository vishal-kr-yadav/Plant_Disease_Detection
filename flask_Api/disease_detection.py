import sys,os
sys.path.insert(0,'/home/vishal/Dropbox/ML/Plant_Disease_Detection')
from os import listdir

# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2
import pandas as pd

def Disease_Detection( image_path ):
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        # load the query image and describe it
        # query = cv2.imread(args["query"])
        filenames = listdir(image_path)
        a = [filename for filename in filenames if filename.endswith('.png')]
        path=image_path+'/'+a[0]
        print(path)
        query = cv2.imread(path)
        print("query==",query)
        features = cd.describe(query)

        # perform the search
        #searcher = Searcher(args["index"])
        searcher = Searcher("../index.csv")
        results = searcher.search(features)
        results.pop(0)
        print("==============", results)
        print()
        # disease_name = results[1][1].split("_")[0].split("\\")[1]   #.... extracting disease name

        # print("**********",disease_name)
        return( results[1][1].split("_")[0] )


# Disease_Detection('/home/vishal/Dropbox/ML/Plant_Disease_Detection/queries')