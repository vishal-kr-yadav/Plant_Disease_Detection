# import os
# os.chdir('D:/projects/Plant_Disease_Detection')

# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2
import pandas as pd
import os

def Disease_Detection( image_path ):
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        # load the query image and describe it
        # query = cv2.imread(args["query"])
        filelist = [file for file in os.listdir(image_path) if file.endswith('.png')]
        query = cv2.imread( image_path + filelist[0] )
        # query = cv2.imread( 'D:\\projects\\Plant_Disease_Detection\\dataset\\CollarRot_1.png' )
        features = cd.describe(query)

        # perform the search
        #searcher = Searcher(args["index"])
        searcher = Searcher( image_path + "/index.csv")
        results = searcher.search(features)
        results.pop(0)

        disease_name = results[1][1].split("_")[0].split("\\")[1]   #.... extracting disease name

        return( disease_name )



        # index = pd.read_csv( 'index.csv' )

        # disease_name_list = index.iloc[:,0].copy()

        # images_to_show = disease_name_list[ disease_name_list.str.contains(disease_name, case=False) ].tolist()




