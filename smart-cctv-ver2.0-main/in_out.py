import cv2
from datetime import datetime
def in_out():
    cap = cv2.VideoCapture(0)#script creates a VideoCapture object using cv2.VideoCapture(0) to capture video from the default camera (index 0)

    right, left = "", ""

    while True:#script enters an infinite loop to continuously process frames from the video.
        _, frame1 = cap.read()#script reads two consecutive frames from the video using cap.read()
        frame1 = cv2.flip(frame1, 1)#frames are flipped horizontally using cv2.flip()
        _, frame2 = cap.read()
        frame2 = cv2.flip(frame2, 1)

        diff = cv2.absdiff(frame2, frame1)#bsolute difference between the two frames
        
        diff = cv2.blur(diff, (5,5))#difference frame is blurred
        
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)#converted to grayscale
        
        _, threshd = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
        
        contr, _ = cv2.findContours(threshd, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #If at least one contour is found (len(contr) > 0), 
        # the script identifies the largest contour as the motion region.
        #  It calculates the bounding rectangle of the contour using cv2.boundingRect() and 
        # draws a rectangle and a text label on the frame to indicate motion.
        x = 300
        if len(contr) > 0:
            max_cnt = max(contr, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(max_cnt)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame1, "MOTION", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
            
        #checking direction of the object
        if right == "" and left == "":
            if x > 500:
                right = True
            
            elif x < 200:
                left = True
                
        elif right:
                if x < 200:
                    print("to left")
                    x = 300
                    right, left = "", ""
                    cv2.imwrite(f"visitors/in/{datetime.now().strftime('%-y-%-m-%-d-%H:%M:%S')}.jpg", frame1)
            
        elif left:
                if x > 500:
                    print("to right")
                    x = 300
                    right, left = "", ""
                    cv2.imwrite(f"visitors/out/{datetime.now().strftime('%-y-%-m-%-d-%H:%M:%S')}.jpg", frame1)
            
            
        
        cv2.imshow("", frame1)
        
        k = cv2.waitKey(1)
        
        if k == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
        
# this is change made 
#one more
