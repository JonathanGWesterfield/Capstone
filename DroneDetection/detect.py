import cv2
import sys
import numpy as np
from threading import Thread
import queue
import time

class DroneTracker:
    """
    This class represents the DroneTracker object, which is responsible for
    tracking the drone in 3D space and outputting extracted coordinates
    """
    major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')

    def __init__(self, video_file_1: str, video_file_2: str) -> None:
        """
        Initializes the tracker with the video file path, and sets up data members

        :param video_file_1: the path to the x/z coordinate video to analyze
        :param video_file_2: the path to the y/z coordinate video to analyze
        """

        # Object members
        self.current_frame_1 = 0
        self.current_frame_2 = 0
        self.total_frames_1 = 0
        self.total_frames_2 = 0
        self.data_points_1 = []
        self.data_points_2 = []
        self.video_file_1 = video_file_1
        self.video_file_2 = video_file_2
        self.frame_queue_1 = queue.Queue()
        self.frame_queue_2 = queue.Queue()
        self.done_reading_1 = False
        self.done_reading_2 = False
        # This is an internal toggle to look for the light before prompting the user
        # to select the bounding box for the drone
        self.look_for_light = False

        # Thread handles
        self.video_thread_handle_1 = Thread(target=self.read_video, args=(1,))
        self.video_thread_handle_2 = Thread(target=self.read_video, args=(2,))
        self.track_thread_1 = Thread(target=self.track_drone, args=(1,))
        self.track_thread_2 = Thread(target=self.track_drone, args=(2,))

        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        self.tracker_type = tracker_types[2]

        # Here the tracker type in the above line is instantiated

        if self.tracker_type == 'BOOSTING':
            self.tracker_1 = cv2.TrackerBoosting_create()
            self.tracker_2 = cv2.TrackerBoosting_create()

        elif self.tracker_type == 'MIL':
            self.tracker_1 = cv2.TrackerMIL_create()
            self.tracker_2 = cv2.TrackerMIL_create()

        elif self.tracker_type == 'KCF':
            self.tracker_1 = cv2.TrackerKCF_create()
            self.tracker_2 = cv2.TrackerKCF_create()

        elif self.tracker_type == 'TLD':
            self.tracker_1 = cv2.TrackerTLD_create()
            self.tracker_2 = cv2.TrackerTLD_create()

        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker_1 = cv2.TrackerMedianFlow_create()
            self.tracker_2 = cv2.TrackerMedianFlow_create()

        elif self.tracker_type == 'GOTURN':
            self.tracker_1 = cv2.TrackerGOTURN_create()
            self.tracker_2 = cv2.TrackerGOTURN_create()

        elif self.tracker_type == 'MOSSE':
            self.tracker_1 = cv2.TrackerMOSSE_create()
            self.tracker_2 = cv2.TrackerMOSSE_create()

        elif self.tracker_type == "CSRT":
            self.tracker_1 = cv2.TrackerCSRT_create()
            self.tracker_2 = cv2.TrackerCSRT_create()


    def rescale_frame(self, frame: object, percent: int = 50) -> object:
        """
        Resizes a frame as a percentage of the original frame size

        :param frame: the frame to be resized
        :param percent: the percent value the frame needs to be rescaled to
        :returns: frame that is resized with the given parameter
        """

        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


    def resize_bbox(self, bbox: tuple, factor: int = 2) -> tuple:
        """
        Resizes the bounding box for translating it to the full size video
        
        In order to be able to see enough of the footage on screen to draw the box around the drone, the video frame must be resized, so the drawn bounding box must be translated back into the coordinate system the full size video uses
        
        For example, if the 4k footage is shrunk by 50% (to 1080p), the scale factor here must be 2 so the coordinates chosen in the 1080p frame will match up with the actual drone coordinates in the 4k frame

        :param bbox: bounding box of selected drone, which is (x, y, box_width, box_height)
        :param factor: the factor by which to scale the bounding box
        :return: tuple that represents the relocated bounding box
        """
        x1 = bbox[0] * factor
        y1 = bbox[1] * factor
        width = bbox[2] * factor
        height = bbox[3] * factor
        return x1, y1, width, height


    def is_light_on(self, frame: object) -> bool:
        """
        Takes in a video frame and returns the frame at which the light turns on
        This is used to synchronize the videos so they both start at the same time
        :param frame: the OpenCV frame that is to be analyzed for the light turning on
        """
        # HSV range for white light
        white_lower = np.array([0, 0, 20])
        white_upper = np.array([5, 2, 255])
        frame_count = 0
        
        # Capture frame-by-frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, white_lower, white_upper)
        count = cv2.countNonZero(mask)

        # If light is on
        if count > 100000 and count < 180000:
            return True
        else:
            return False
    
    def get_data_points(self) -> list:
        """
        Returns a list of tuples that represent the flight path of the drone
        :return: list of tuples of coordinates and time values that represent the flight path of the drones
                 in the format [(time, x_coord, y_coord, z_coord)]
        """
        points = []

        shortest_len = min(len(self.data_points_1), len(self.data_points_2))

        # Cycle through all of the data points that can be represented with the extracted coordinates
        # from both videos
        for i in range(0, shortest_len-1):
            tup = (self.data_points_1[i][2], # time value
                   (self.data_points_1[i][0]/3840)*15, # x coordinate scaled to 15 meters
                   (self.data_points_2[i][0]/3840)*15, # y coordinate scaled to 15 meters
                   (((self.data_points_1[i][1] + self.data_points_2[i][1])/2)/2160)*10 ) # z coordinate,
                                                                                         # scaled to 10 meters
            points.append(tup)

        return points

    def read_video(self, video_num: int) -> None:
        """
        This function is to be threaded, and its purpose is to read in the video file
        all at once to improve performance
        :param video_num: the video number, which can be either 1 or 2, which
        tells the function which variables to used based on which video is being read
        """

        # Set parameters based on which video is being read
        if video_num == 1:
            videoFile = self.video_file_1
            frame_queue = self.frame_queue_1
            total_frames = self.total_frames_1
            # done_reading = self.done_reading_1
        elif video_num == 2:
            videoFile = self.video_file_2
            frame_queue = self.frame_queue_2
            total_frames = self.total_frames_2
            # done_reading = self.done_reading_2

        video = cv2.VideoCapture(videoFile)
        # If unable to open the video file (probably wrong path)
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        # Read first frame.
        ok, frame = video.read()
        # If unable to get a frame (probably bad format)
        if not ok:
            print('Cannot read video file')
            sys.exit()

        total_frames += 1
        frame_queue.put(frame)

        # Read frames until the end of the video is reached (or until it hits corruption)
        while True:
            ok, frame = video.read()
            # If not ok, which is normally when the end of the file has been read, break from loop
            if not ok:
                break
            # Add the frame to the respective frame queue
            frame_queue.put(frame)
            total_frames += 1
        # Signal that the thread is done reading the video file
        if video_num == 1:
            self.done_reading_1 = True
        elif video_num == 2:
            self.done_reading_2 = True


    def process_video(self) -> list:
        """
        Starts all threads related to processing the video, including the reading of
        the video and the tracking of the drones
        This function is the only function that should be called externally other than the constructor
        :return: list of tuples of the extracted coordinates of the footage, in the format
        [(time, x_coord, y_coord, z_coord)]
        """
        # Start the video read thread for video 1
        self.video_thread_handle_1.start()
        # Start the tracker for video 1
        self.track_thread_1.start()
        # Join the video read thread for video 1
        self.video_thread_handle_1.join()
        # Join the tracker for video 1
        self.track_thread_1.join()

        # Start the video read thread for video 2
        self.video_thread_handle_2.start()
        # Start the tracker for video 2
        self.track_thread_2.start()
        # Join the video read thread for video 2
        self.video_thread_handle_2.join()
        # Join the tracker for video 2
        self.track_thread_2.join()

        # Return the processed points to the calling function
        return self.get_data_points()

    def track_drone(self, video_num) -> None:
        """
        Function that contains all code to track the drone, and is to be run
        as a thread. Does not play nicely when 2 of these threads are started
        at the same time
        :param video_num: the video number, which can be either 1 or 2, which
        tells the function which variables to used based on which video is being read
        """

        if video_num == 1:
            frame_queue = self.frame_queue_1
            tracker = self.tracker_1
            data_points = self.data_points_1
            select_str = "Select drone in x/z plane"
            tracking_str = "Tracking drone in x/z plane"
        if video_num == 2:
            frame_queue = self.frame_queue_2
            tracker = self.tracker_2
            data_points = self.data_points_2
            select_str = "Select drone in y/z plane"
            tracking_str = "Tracking drone in y/z plane"

        current_frame = 0

        # This code chunk will not start analyzing the footage until the point
        # where the light is detected to be turned on
        # Due to the way we are now synchronizing the videos, this shouldn't be called
        # but I'm leaving it here in case we go back to that method
        if self.look_for_light:
            # Loop until OpenCV detects that the light has been turned on
            while not self.is_light_on(frame):
                frame = frame_queue.get()
                self.current_frame += 1

            print("Frame when light is first on: " + str(self.current_frame))

            # Skip 30 frames, which is equivalent to one second
            # The light should be on for half a second, or 15 frames, so this skips the time the
            # light is on as well as a few frames after so the video can refocus
            for i in range(30):
                frame = frame_queue.get()

            # Reset the counter so the time from when the sync light is detected is the same for both videos
            current_frame = 0

        # Gets a frame from the frame queue
        frame = frame_queue.get()

        # Here I resize the frame to 40% of its size, so the entire frame can be displayed onto the screen
        # The 4k footage is too large for my laptop screen, so this scales it down
        resizedFrame = self.rescale_frame(frame, 40)
        # Ask the user to draw a box around the drone
        bbox = cv2.selectROI(select_str, resizedFrame, False)
        # Reposition the bounding box from 40% resolution to 100% resolution
        bbox = self.resize_bbox(bbox, 2.5)

        cv2.destroyWindow(select_str)

        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)


        # This while loop will run until the footage is finished, processing all of the drone footage
        while True:

            if video_num == 1:
                # Check if queue is empty but the read thread for video 1 is not done
                if frame_queue.empty() and not self.done_reading_1:
                    # If so, sleep for a second for the producer to catch up and try again
                    time.sleep(1)
                    print("slept for 1 second")
                    continue
                # Check if queue is empty and the read thread for video 1 is done
                if frame_queue.empty() and self.done_reading_1:
                    # If so, destroy the window and break out of loop
                    cv2.destroyWindow(tracking_str)
                    print("done tracking this drone at " + str(tm))
                    break

            elif video_num == 2:
                # Check if queue is empty but the read thread for video 2 is not done
                if frame_queue.empty() and not self.done_reading_2:
                    # If so, sleep for a second for the producer to catch up and try again
                    time.sleep(1)
                    print("slept for 1 second")
                    continue
                # Check if queue is empty and the read thread for video 1 is done
                if frame_queue.empty() and self.done_reading_2:
                    # If so, destroy the window and break out of loop
                    cv2.destroyWindow(tracking_str)
                    print("done tracking this drone at " + str(tm))
                    break

            # Get frame from the frame queue
            frame = frame_queue.get()
            
            # Start timer
            timer = cv2.getTickCount()
    
            # Update tracker
            ok, bbox = tracker.update(frame)
    
            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            tm = current_frame/30
    
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                # Should branch to below code every half second of video processed
                if current_frame % 15 == 0:
                    x_coord = bbox[0] + bbox[2]/2
                    y_coord = bbox[1] + bbox[3]/2
                    print("drone coordinate at time " + str(tm) + ": [" + str(x_coord) + ", " + str(y_coord) + "] ("
                          + str((x_coord/3860)*15) + ", " + str((y_coord/2160)*10) + ")")
                    data_points.append((x_coord, y_coord, tm))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

                # This will loop until the drone is reselected, and creates a new tracker that will
                # continue to track the drone
                while True:
                    # Rescale the frame so the user can see the entire frame to reselect the drone
                    resizedFrame = self.rescale_frame(frame, 40)
                    # Ask the user to draw a box around the drone
                    bbox = cv2.selectROI(select_str, resizedFrame, False)
                    # Reposition the bounding box from 40% resolution to 100% resolution
                    bbox = self.resize_bbox(bbox, 2.5)
                    # Close the ROI selection window
                    cv2.destroyWindow(select_str)
                    # This will skip 1 second of video if the drone is out of frame,
                    # which is detected if the user presses escape on the selectROI function
                    if bbox[0] == 0.0 and bbox[1] == 0.0 and bbox[2] == 0.0 and bbox[3] == 0.0:
                        for i in range(1, 30):
                            if current_frame % 15 == 0:
                                data_points.append((None, None, tm))
                            frame_queue.get()
                            current_frame += 1
                    # If the user selected a bounding box, create a new tracker
                    # and continue to track the drone
                    else:
                        # Creates a new KCF tracker (this is due to the update function not working
                        # the same in python as it does in C++: in C++, we could simply update the
                        # tracker with the new bounding box instead of creating a new one, but this
                        # is a known limitation in python's implementation of OpenCV and this is my workaround)
                        tracker = cv2.TrackerKCF_create()
                        # Initialize the tracker with the newly selected bounding box
                        ok = tracker.init(frame, bbox)
                        break
    
            # Display tracker type on frame
            cv2.putText(frame, self.tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

            # Resize the frame to be shown to the user while the drone is being tracked
            resizedFrame = self.rescale_frame(frame, 25)

            # Display result
            cv2.imshow(tracking_str, resizedFrame)

            current_frame += 1
    
            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
