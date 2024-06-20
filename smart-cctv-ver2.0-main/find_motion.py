import cv2
from spot_diff import spot_diff
import time
import numpy as np


def find_motion():

	motion_detected = False
	is_start_done = False

	cap = cv2.VideoCapture(0)#script creates a VideoCapture object using cv2.VideoCapture(0) to capture video from the default camera (index 0)

	check = []
	
	print("waiting for 2 seconds")
	time.sleep(2) #to allow the camera to stabilize.
	frame1 = cap.read() #script reads the initial frame from the video 

	_, frm1 = cap.read()
	frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY) #this frame is converted to grayscale

	
	while True: #script enters an infinite loop to continuously process frames from the video
		_, frm2 = cap.read()
		frm2 = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)

		diff = cv2.absdiff(frm1, frm2) #absolute difference between the current frame (frm2) and 
										#the previous frame (frm1) is calculated and stored in the diff 

		_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)# applies a threshold to the frame difference image and store 

		contors = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]#find contours in the thresholded image (thresh).

		#look at it
		contors = [c for c in contors if cv2.contourArea(c) > 25] #Filter contours-Contours with an area less than 25 are removed from the contors list.


		if len(contors) > 5: #If the number of remaining contours is greater than 5, motion is considered detected.
			cv2.putText(thresh, "motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
			motion_detected = True
			is_start_done = False
		
		elif motion_detected and len(contors) < 3:#Track motion duration: If motion is detected (motion_detected is True), 
			if (is_start_done) == False:		  #the script tracks the duration of motion by measuring the time elapsed since the motion started (start and end variables). 
				start = time.time()				  #If the elapsed time is greater than 4 seconds, further processing is performed.
				is_start_done = True
				end = time.time()

			end = time.time()

			print(end-start)
			if (end - start) > 4:
				frame2 = cap.read()
				cap.release()
				cv2.destroyAllWindows()
				x = spot_diff(frame1, frame2)
				if x == 0:
					print("running again")
					return

				else:
					print("found motion")
					return

		else:
			cv2.putText(thresh, "no motion detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

		cv2.imshow("winname", thresh)

		_, frm1 = cap.read()
		frm1 = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)

		if cv2.waitKey(1) == 27:
			
			break

	return
