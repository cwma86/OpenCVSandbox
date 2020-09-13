#! /usr/bin/env python3
import argparse
import cv2
import logging
import matplotlib
import numpy
import os

def arguments():
    parser = argparse.ArgumentParser(description='open cv image')
    parser.add_argument('filePath', metavar='Image file path', type=str,
                        help='file path to the image')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose logging output')
    args = parser.parse_args()
    logLevel = logging.INFO
    if (args.verbose):
        logLevel = logging.DEBUG
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logging.DEBUG)
    return args

def main(args):
    print("args.filePath %s" %args.filePath)
    if (not os.path.isfile(args.filePath)):
        raise FileNotFoundError("Image file does not exists at %s" %os.path.abspath(args.filePath))

    # Read the image in as gray scale
    img1 = cv2.imread( os.path.abspath(args.filePath), cv2.IMREAD_GRAYSCALE)

    # Write the image
    cv2.imwrite('newFile.jpg', img1)

if __name__ == "__main__":
    args = arguments()
    main(args)