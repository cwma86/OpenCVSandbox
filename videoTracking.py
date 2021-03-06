#! /usr/bin/env python3
import argparse
import cv2
import imutils
import logging
import time

from imutils.video import VideoStream
from imutils.video import FPS


def argumentsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str,
                        help="input video file path")
    parser.add_argument("-t", "--tracker", type=str, default="csrt",
                        help="OpenCV object tracker type")
    parser.add_argument('-v', '--verbose', action='store_true',
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
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }
    tracker = OPENCV_OBJECT_TRACKERS[args.tracker]()
    # initialize the bounding box coordinates of the object we are going
    # to track
    initBB = None

    if not (args.video):
      logging.info("Start webcam Stream")
      vs = VideoStream(src=0).start()
      time.sleep(1.0)
    else:
      logging.info("using input video %s" %args.video)
      vs = cv2.VideoCapture(args.video)

    # loop over frames
    fps = None
    while True:
      # Get the first frame
      frame = vs.read()
      frame = frame[1] if args.video else frame
      # Check for end of the video
      if frame is None:
        break
      # resize the frame (so we can process it faster) and grab the
      # frame dimensions
      frame = imutils.resize(frame, width=500)
      (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
      if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
          (x, y, w, h) = [int(v) for v in box]
          cv2.rectangle(frame, (x, y), (x + w, y + h),
            (0, 255, 0), 2)
        # update the FPS counter
        fps.update()
        fps.stop()
        # initialize the set of information we'll be displaying on
        # the frame
        info = [
          ("Tracker", args.tracker),
          ("Success", "Yes" if success else "No"),
          ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
          text = "{}: {}".format(k, v)
          cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

              # show the output frame
      cv2.imshow("Frame", frame)
      key = cv2.waitKey(1) & 0xFF
      # if the 's' key is selected, we are going to "select" a bounding
      # box to track
      if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
          showCrosshair=True)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()

          # if the `c` key was pressed, break from the loop
      elif key == ord("c"):
        break
    # if we are using a webcam, release the pointer
    if not args.video:
      vs.stop()
    # otherwise, release the file pointer
    else:
      vs.release()
    # close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
  args = argumentsParser()
  main(args)