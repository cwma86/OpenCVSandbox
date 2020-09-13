#! /usr/bin/env python3
import argparse
import cv2
import logging
import matplotlib
import numpy
import os

def arguments():
    parser = argparse.ArgumentParser(description='open cv image')
    parser.add_argument('filePath1', metavar='Image file 1 path', type=str,
                        help='file path to the image 1')
    parser.add_argument('filePath2', metavar='Image file 2 path', type=str,
                        help='file path to the image 2')
    parser.add_argument('-w1',  metavar='weight of image 1' , type=float, default=0.9,
                        help='weight of image 1')
    parser.add_argument('-w2',  metavar='weight of image 2' , type=float, default=0.4,
                        help='weight of image 2')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='verbose logging output')
    args = parser.parse_args()
    logLevel = logging.INFO
    if (args.verbose):
        logLevel = logging.DEBUG
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
        level=logLevel)
    return args

def main(args):
    logging.debug("args.filePath %s" %args.filePath1)
    logging.debug("args.filePath %s" %args.filePath2)
    if (not os.path.isfile(args.filePath1)):
        raise FileNotFoundError("Image file does not exists at %s" %os.path.abspath(args.filePath1))
    if (not os.path.isfile(args.filePath2)):
        raise FileNotFoundError("Image file does not exists at %s" %os.path.abspath(args.filePath2))

    # Read the image in as gray scale
    img1 = cv2.imread( os.path.abspath(args.filePath1))
    img2 = cv2.imread( os.path.abspath(args.filePath2))

    # resize the images to be the same size
    if( img1.shape[0] != img2.shape[0] or img1.shape[1] !=  img2.shape[1]):
        logging.info("Image height or weight not equal resizing image 2 to match image 1")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Combine the images
    weightedSum = cv2.addWeighted(img1, args.w1, img2, args.w2, 0)

    # Write the image
    cv2.imwrite('newFile.jpg', weightedSum)
    logging.info("new image written to %s" %os.path.abspath('newFile.jpg'))


if __name__ == "__main__":
    args = arguments()
    main(args)