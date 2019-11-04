import cv2
import sys
import numpy as np

class DroneTracker:

    major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')

    def __init__(self, videoFile):
        self.current_frame = 0
        self.data_points = []
        self.videoFile = videoFile


        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
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

    # def place_image_text(self, frame, fps):


    # Resizes a frame as a percentage of the original frame size
    def rescale_frame(self, frame, percent=50):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # Resizes the bounding box for translating it to the full size video
    # In order to be able to see enough of the footage on screen to draw the box around the drone,
    # the video frame must be resized, so the drawn bounding box must be translated back into the proper
    # coordinate system the full size video uses
    # For example, if the 4k footage is shrunk by 50% (to 1080p), the scale factor here must be 2 so the coordinates
    # chosen in the 1080p frame will match up with the actual drone coordinates in the 4k frame
    def resize_bbox(self, bbox, factor=2):
        x1 = bbox[0] * factor
        y1 = bbox[1] * factor
        width = bbox[2] * factor
        height = bbox[3] * factor
        return (x1, y1, width, height);


    #Takes in video and return the frame at which the light turns on
    def is_light_on(self, frame):
        # HSV range for white light
        white_lower = np.array([0, 0, 20])
        white_upper = np.array([5, 2, 255])
        frame_count = 0
        
        # Capture frame-by-frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, white_lower, white_upper)
        count = cv2.countNonZero(mask)
        #light is on
        if count > 100000 and count < 180000:
            return True
        else:
            return False

    def trackDrone(self):

        # Read video
        video = cv2.VideoCapture(self.videoFile)

        # Exit if video not opened.
        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        # Read first frame.
        ok, frame = video.read()
        if not ok:
            print('Cannot read video file')
            sys.exit()

        # Loop until OpenCV detects that the light has been turned on
        while not self.is_light_on(frame):
            ok, frame = video.read()
            self.current_frame += 1
        
        print("frame when light is on: " + str(self.current_frame))

        # Skip 30 frames, which is equivalant to one second
        # The light should be on for half a second, or 15 frames, so this skips the time the
        # light is on as well as a few frames after so the video can refocus
        for i in range(30):
            ok, frame = video.read()

        # Reset the counter so the time from when the sync light is detected is the same for both videos
        self.current_frame = 0

        # Here I resize the frame to 40% of its size, so the entire frame can be displayed onto the screen
        # The 4k footage is too large for my laptop screen, so this scales it down
        resizedFrame = self.rescale_frame(frame, 40)
        # Ask the user to draw a box around the drone
        bbox = cv2.selectROI(resizedFrame, False)
        # Reposition the bounding box from 40% resolution to 100% resolution
        bbox = self.resize_bbox(bbox, 2.5)

        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(frame, bbox)

        
        #
        while True:
            # Read a new frame
            ok, frame = video.read()
            if not ok:
                break
            
            # Start timer
            timer = cv2.getTickCount()
    
            # Update tracker
            ok, bbox = self.tracker.update(frame)
    
            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            time = self.current_frame/30
    
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                if (self.current_frame % 15 == 0):
                    x_coord = bbox[0] + bbox[2]/2
                    y_coord = bbox[1] + bbox[3]/2
                    print("drone coordinate at time " + str(time) + ": [" + str(x_coord) + ", " + str(y_coord) + "]")
                    self.data_points.append((x_coord, y_coord, time))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

                self.data_points.append( (None, None, time) )
    
            # Display tracker type on frame
            cv2.putText(frame, self.tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

            resizedFrame = self.rescale_frame(frame, 40)

            # Display result
            cv2.imshow("Tracking", resizedFrame)

            self.current_frame += 1;
    
            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break






if __name__ == '__main__' :

    tracker = DroneTracker("D:/Projects/Capstone/Drone-Detection/video/floodlight_outside.mp4")

    tracker.trackDrone()

    # Set up tracker.

    # tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    # tracker_type = tracker_types[2]

    # # here the tracker type in the above line is instantiated

    # if tracker_type == 'BOOSTING':
    #     tracker = cv2.TrackerBoosting_create()
    # elif tracker_type == 'MIL':
    #     tracker = cv2.TrackerMIL_create()
    # elif tracker_type == 'KCF':
    #     tracker = cv2.TrackerKCF_create()
    # elif tracker_type == 'TLD':
    #     tracker = cv2.TrackerTLD_create()
    # elif tracker_type == 'MEDIANFLOW':
    #     tracker = cv2.TrackerMedianFlow_create()
    # elif tracker_type == 'GOTURN':
    #     tracker = cv2.TrackerGOTURN_create()
    # elif tracker_type == 'MOSSE':
    #     tracker = cv2.TrackerMOSSE_create()
    # elif tracker_type == "CSRT":
    #     tracker = cv2.TrackerCSRT_create()

    # data_points = []
    # current_frame = 0;

    # # Read video
    # video = cv2.VideoCapture("D:/Projects/Capstone/Drone-Detection/video/floodlight_outside.mp4")
    # # trimmed_1_drone.mp4")

    # # Exit if video not opened.
    # if not video.isOpened():
    #     print("Could not open video")
    #     sys.exit()

    # # Read first frame.
    # ok, frame = video.read()
    # if not ok:
    #     print('Cannot read video file')
    #     sys.exit()

    # # Define an initial bounding box
    # #bbox = (287, 23, 86, 320)


    # while not is_light_on(frame):
    #     ok, frame = video.read()
    #     current_frame += 1
    
    # print("frame when light is on: " + str(current_frame))
 
    # # Uncomment the line below to select a different bounding box
    # # resizedFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    # resizedFrame = rescale_frame(frame, 40)
    # bbox = cv2.selectROI(resizedFrame, False)
    # bbox = resize_bbox(bbox, 2.5)
    # # Initialize tracker with first frame and bounding box
    # ok = tracker.init(frame, bbox)

    
 
    # while True:
    #     # Read a new frame
    #     ok, frame = video.read()
    #     if not ok:
    #         break
         
    #     # Start timer
    #     timer = cv2.getTickCount()

    #     # resizedFrame = rescale_frame(frame)
 
    #     # Update tracker
    #     ok, bbox = tracker.update(frame)
    #     # ok, bbox = tracker.update(resizedFrame)
 
    #     # Calculate Frames per second (FPS)
    #     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    #     time = current_frame/30
 
    #     # Draw bounding box
    #     if ok:
    #         # Tracking success
    #         p1 = (int(bbox[0]), int(bbox[1]))
    #         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    #         if (current_frame % 15 == 0):
    #             x_coord = bbox[0] + bbox[2]/2
    #             y_coord = bbox[1] + bbox[3]/2
    #             print("drone coordinate at time " + str(time) + ": [" + str(x_coord) + ", " + str(y_coord) + "]")
    #             data_points.append((x_coord, y_coord, time))
    #         cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    #         # cv2.rectangle(resizedFrame, p1, p2, (255,0,0), 2, 1)

    #     else :
    #         # Tracking failure
    #         cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    #         # cv2.putText(resizedFrame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    #         data_points.append( (None, None, time) )
 
    #     # Display tracker type on frame
    #     cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    #     # cv2.putText(resizedFrame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
    #     # Display FPS on frame
    #     cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
    #     # cv2.putText(resizedFrame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);s

    #     resizedFrame = rescale_frame(frame, 40)

    #     # Display result
    #     # cv2.imshow("Tracking", frame)
    #     cv2.imshow("Tracking", resizedFrame)

    #     current_frame += 1;
 
    #     # Exit if ESC pressed
    #     k = cv2.waitKey(1) & 0xff
    #     if k == 27 : break