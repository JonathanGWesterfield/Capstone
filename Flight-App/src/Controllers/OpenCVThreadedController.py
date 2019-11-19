#!/usr/bin/env python3

import cv2
import re
import sys
import os
import argparse
import numpy as np
from threading import Thread
import queue

import time

import json

class VideoNotPresentException(Exception):
    """
    This error is raised when the video for processing is not there, or if an incorrect path is given
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the exception be being thrown.
        """
        Exception.__init__(self, message)

class VideoCorruptedException(Exception):
    """
    This error is raised if the video being read is corrupted, or if the frames cannot be
    successfully extracted from the video files
    """
    def __init__(self, message: str):
        """
        Calls the base Python Exception class and provides it with the error message we want to display.

        :param message: The error message we want the exception to contain to help with figuring out why the exception be being thrown.
        """
        Exception.__init__(self, message)

class DroneTracker:
    """
    This class is intended to track sUASs in video recorded from the smartphone app
    All containing code to track the drone and output the coordinates extracted from
    the recorded video is contained within this class, and this file is intended
    to be run as a separate process so that both of the recordings can be processed
    in parallel (don't try this on Windows though).
    """

    major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')

    def __init__(self, videoFile) -> None:
        """
        Initializes the tracker with the video file path

        :param videoFile: the path to the video to analyze
        """
        self.current_frame = 0
        self.total_frames = 0
        self.data_points = []
        self.videoFile = videoFile
        self.frame_queue = queue.Queue(maxsize=100)
        self.done_reading = False
        self.read_video_thread = Thread(target=self.read_video, args=())

        tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = tracker_types[2]

        # here the tracker type in the above line is instantiated

        if self.tracker_type == 'BOOSTING':
            self.tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == 'MIL':
            self.tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == 'KCF':
            self.tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == 'TLD':
            self.tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == 'GOTURN':
            self.tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == 'MOSSE':
            self.tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()


    def rescale_frame(self, frame, percent=50):
        """
        Resizes a frame as a percentage of the original frame size

        :param frame: the frame to be resized
        :param percent: the percent value the frame needs to be rescaled to
        """
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def resize_bbox(self, bbox: tuple, factor=2) -> tuple:
        """
        Resizes the bounding box for translating it to the full size video.
        In order to be able to see enough of the footage on screen to draw the box around the drone,
        the video frame must be resized, so the drawn bounding box must be translated back into the
        coordinate system the full size video uses.
        For example, if the 4k footage is shrunk by 50% (to 1080p), the scale factor here must be 2
        so the coordinates chosen in the 1080p frame will match up with the actual drone coordinates in the 4k frame.

        :param bbox: bounding box of selected drone, which is (x, y, box_width, box_height)
        :param factor: the factor by which to scale the bounding box
        :return: tuple
        """
        x1 = bbox[0] * factor
        y1 = bbox[1] * factor
        width = bbox[2] * factor
        height = bbox[3] * factor
        return (x1, y1, width, height);

    def is_light_on(self, frame) -> bool:
        """
        Takes in a video frame and returns the frame at which the light turns on.

        :param frame: A single video frame to see if the light is on.
        :return: True if the light is on, false otherwise.
        """
        # HSV range for white light
        white_lower = np.array([0, 0, 20])
        white_upper = np.array([5, 2, 255])
        frame_count = 0

        # Capture frame-by-frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, white_lower, white_upper)
        count = cv2.countNonZero(mask)
        # light is on
        if count > 100000 and count < 180000:
            return True
        else:
            return False
    

    def read_video(self) -> None:
        """
        This function is to be threaded, and its purpose is to read in the video file
        all at once to improve performance.
        """

        video = cv2.VideoCapture(self.videoFile)
        # If unable to open the video file (probably wrong path)
        if not video.isOpened():
            raise VideoNotPresentException("Could not open video")

        # Read first frame.
        ok, frame = video.read()
        # If unable to get a frame (probably bad format)
        if not ok:
            raise VideoCorruptedException("Cannot read video file")

        self.total_frames += 1
        self.frame_queue.put(frame)

        # Read frames until the end of the video is reached (or until it hits corruption)
        while True:
            ok, frame = video.read()
            # If not ok, which is normally when the end of the file has been read, break from loop
            if not ok:
                break
            # Add the frame to the respective frame queue
            self.frame_queue.put(frame, block=True)
            self.total_frames += 1
        
        # Signal that the thread is done reading the video file
        self.done_reading = True


    def trackDrone(self) -> list:
        """
        Function that contains all code to track the drone, and is to be run
        as a thread. Will run much slower if 2 processes running this method are started and run on different
        videos at the same time.

        :return: List of tuples of the extracted coordinates of the footage, in the format [(time, x_coord, y_coord, z_coord)].
        """
        # Start video thread
        self.read_video_thread.start()

        # Reset the counter so the time from when the sync light is detected is the same for both videos
        self.current_frame = 0

        frame = self.frame_queue.get(block=True)

        # Here I resize the frame to 40% of its size, so the entire frame can be displayed onto the screen
        # The 4k footage is too large for my laptop screen, so this scales it down
        resizedFrame = self.rescale_frame(frame, 30)
        # Ask the user to draw a box around the drone
        bbox = cv2.selectROI("Select Drone", resizedFrame, False)
        # Reposition the bounding box from 40% resolution to 100% resolution
        bbox = self.resize_bbox(bbox, 3.33)

        cv2.destroyWindow("Select Drone")

        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(frame, bbox)

        # This while loop will run until the footage is finished, processing all of the drone footage
        while True:
            # Check if queue is empty but the read thread for the video is not done
            if self.frame_queue.empty() and not self.done_reading:
                # If so, sleep for a second for the producer to catch up and try again
                time.sleep(1)
                print("slept for 1 second")
                continue

            # Check if queue is empty and the read thread for video 1 is done
            if self.frame_queue.empty() and self.done_reading:
                # If so, destroy the window and break out of loop
                cv2.destroyWindow("Tracking")
                print("done tracking this drone at " + str(tm) + " seconds")
                break

            # Get frame from the frame queue
            frame = self.frame_queue.get(block=True)

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok, bbox = self.tracker.update(frame)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            tm = self.current_frame / 30

            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                if self.current_frame % 15 == 0:
                    x_coord = bbox[0] + (bbox[2] / 2)
                    y_coord = bbox[1] + (bbox[3] / 2)
                    print("drone coordinate at time " + str(tm) + ": [" + str(x_coord) + ", " + str(y_coord) + "] ("
                          + str((x_coord/3860)*15) + ", " + str((y_coord/2160)*10) + ")")
                    self.data_points.append((x_coord, y_coord, tm))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

                skip = 5

                # This will loop until the drone is reselected, and creates a new tracker that will
                # continue to track the drone
                while True:
                    # Rescale the frame so the user can see the entire frame to reselect the drone
                    resizedFrame = self.rescale_frame(frame, 30)
                    # Ask the user to draw a box around the drone
                    bbox = cv2.selectROI("Reselect Drone", resizedFrame, False)
                    # Reposition the bounding box from 40% resolution to 100% resolution
                    bbox = self.resize_bbox(bbox, 3.33)
                    # Close the ROI selection window
                    cv2.destroyWindow("Reselect Drone")
                    # This will skip 1 second of video if the drone is out of frame,
                    # which is detected if the user presses escape on the selectROI function
                    if bbox[0] == 0.0 and bbox[1] == 0.0 and bbox[2] == 0.0 and bbox[3] == 0.0:

                        print("skipping " + str(skip) + " frames")
                        for i in range(1, skip):
                            if self.current_frame % 15 == 0:
                                tm = self.current_frame / 30
                                self.data_points.append((None, None, tm))
                            # If the video has totally been processed, exit the function
                            # Kind of a hacky way to do it, but I need to break out of 3 loops here
                            # so returning is easier than functionalizing the small parts of this giant function
                            if self.frame_queue.empty() and self.done_reading:
                                self.read_video_thread.join()
                                return self.data_points
                            frame = self.frame_queue.get(block=True)
                            self.current_frame += 1

                        if skip == 5:
                            skip = 15
                        elif skip == 15:
                            skip = 30
                        elif skip == 30:
                            skip = 60
                        # else:
                        #     skip += 30

                    # If the user selected a bounding box, create a new tracker
                    # and continue to track the drone
                    else:
                        # Creates a new KCF tracker (this is due to the update function not working
                        # the same in python as it does in C++: in C++, we could simply update the
                        # tracker with the new bounding box instead of creating a new one, but this
                        # is a known limitation in python's implementation of OpenCV and this is my workaround)
                        self.tracker = cv2.TrackerKCF_create()
                        # Initialize the tracker with the newly selected bounding box
                        ok = self.tracker.init(frame, bbox)
                        break

            # Display tracker type on frame
            cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            resizedFrame = self.rescale_frame(frame, 20)

            # Display result
            cv2.imshow("Tracking", resizedFrame)

            self.current_frame += 1;

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            # if k == 27:
            #     break

            # Allows the user to reset the bounding box in the case that the tracker
            # begins to track a different object or isn't tracking the drone accurately
            # enough
            if "r" == chr(k):
                # Rescale the frame so the user can see the entire frame to reselect the drone
                resizedFrame = self.rescale_frame(frame, 40)
                # Ask the user to draw a box around the drone
                bbox = cv2.selectROI("Reselect Drone", resizedFrame, False)
                # Reposition the bounding box from 40% resolution to 100% resolution
                bbox = self.resize_bbox(bbox, 2.5)
                # Close the ROI selection window
                cv2.destroyWindow("Reselect Drone")

                # Creates a new KCF tracker (this is due to the update function not working
                # the same in python as it does in C++: in C++, we could simply update the
                # tracker with the new bounding box instead of creating a new one, but this
                # is a known limitation in python's implementation of OpenCV and this is my workaround)
                self.tracker = cv2.TrackerKCF_create()
                # Initialize the tracker with the newly selected bounding box
                ok = self.tracker.init(frame, bbox)

        self.read_video_thread.join()

        return self.data_points

def merge_data_points(phone1Points:list, phone2Points:list) -> dict:
    """
    Takes the points outputted by the opencv analysis and merges the points together to create
    the 3D coordinates needed to output the visual flight path.

    :param phone1Points: The opencv datapoints created from the main method of this class for the first phone
    :param phone2Points: The opencv datapoints created from the main method of this class for the second phone
    :return: List of tuples of coordinates and time values that represent the flight path of the drone in the format [(time, x_coord, y_coord, z_coord)]
    """
    points = []

    shortest_len = min(len(phone1Points), len(phone2Points))

    # Cycle through all of the data points that can be represented with the extracted coordinates
    # from both videos
    for i in range(0, shortest_len - 1):
        if phone1Points[i][0] == None or phone2Points[i][0] == None or \
            phone1Points[i][1] == None or phone2Points[i][1] == None:
            tup = (phone1Points[i][2], None, None, None)
        else:
            tup = (phone1Points[i][2],  # time value
                   (phone1Points[i][0] / 3840) * 15,  # x coordinate scaled to 15 meters
                   (phone2Points[i][0] / 3840) * 15,  # y coordinate scaled to 15 meters
                   ( (2160 - ((phone1Points[i][1] + phone2Points[i][1]) / 2) ) / 2160) * 10)  # z coordinate,
            # scaled to 10 meters
        points.append(tup)

    return points

def get_phone_id(filename:str) -> str:
    """
    Gets the phone Id from the end of the file name so we can keep track of the json and lock files.

    :param filename: The file name of the video file. Should have "phone-#.mp4" file names.
    :return: The ID of the phone from the file name
    """

    fileTokens = re.split('_|\.', filename)

    return fileTokens[-2]

def main(filename:str) -> None:
    """
    Will take the filename passed in and analyze the footage. All coordinates of the drone in the footage
    will be output to a json file.

    :return: None
    """
    try:
        # get the correct directory for this thing to work in.
        pathToDroneFiles = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/drone-tracker/opencv-output/')

        phoneID = get_phone_id(filename)

        # create lock file to let the parent process know that this is still running
        lock = open(pathToDroneFiles + phoneID + '.lock', 'w').close()

        print(filename)

        if not(os.path.exists(filename)):
            print("Couldn't find the video file given!!!")

        tracker = DroneTracker(filename)
        data_points = tracker.trackDrone()  # Extract the coordinates

        # data = {"coords": data_points}

        js = json.dumps(data_points, indent=4)

        # write the extracted coordinates to a json file
        with open(pathToDroneFiles + phoneID + ".json", "w") as fh:
            fh.write(js)

        # # Remove the lock file to let the parent process know that the extraction is complete
        # if os.path.exists(pathToDroneFiles + filename + '.lock'):
        #     os.remove(pathToDroneFiles + filename + '.lock')
        # else:
        #     print("The file does not exist")

    except Exception as e:
        print("ERROR: ", e)

        # Remove the lock file to let the parent process know that the extraction is complete even if it failed
        if os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/drone-tracker/opencv-output/') + phoneID + '.lock'):
            os.remove(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/drone-tracker/opencv-output/') + phoneID + '.lock')
        else:
            print("The file does not exist")

    finally:
        # Remove the lock file to let the parent process know that the execution finished regardless of success
        if os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')),
                                       'Desktop/drone-tracker/opencv-output/') + phoneID + '.lock'):
            os.remove(os.path.join(os.path.join(os.path.expanduser('~')),
                                   'Desktop/drone-tracker/opencv-output/') + phoneID + '.lock')
        else:
            print("The file does not exist")
        sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     'Process the drone footage to output all of the X, Y coordinates of the drone')
    # parser.add_argument('filename', action='store', help='The file name of the video to analyze')
    #
    # args = parser.parse_args()

    main(sys.argv[1])




# if __name__ == '__main__':
    # tracker_1 = DroneTracker("/Users/jgwesterfield/Documents/CSCE 483/Drone-Tracker/Flight-App/src/Controllers/pixel_synced_Trim_Trim.mp4")

    # data_points_1 = tracker_1.trackDrone()

    # tracker_2 = DroneTracker("/Users/jgwesterfield/Documents/CSCE 483/Drone-Tracker/Flight-App/src/Controllers/s10_synced_Trim_Trim.mp4")

    # data_points_2 = tracker_2.trackDrone()

    # coords = tracker_2.get_data_points(data_points_1, data_points_2)

    # data = {"coords": coords}

    # js = json.dumps(data, indent=4)

    # print(js)

    # tracker = DroneTracker(str(sys.argv[1]))

    # points = tracker.trackDrone()

    # print(points)