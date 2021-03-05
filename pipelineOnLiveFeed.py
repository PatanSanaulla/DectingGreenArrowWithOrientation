import cv2
import numpy as np
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime

def detectOBI(image):
    height = (image.shape[0])
    width = (image.shape[1])
    
    #getting the HSV
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #setting the threshold for the color
    #print(hsvImage)
    #blankImage = np.zeros(shape=[height, width, 1], dtype=np.uint8)
    
    #for i in range(0,height):
    #    for j in range(0,width):
    #        if 65 <= hsvImage[i][j][0] and 85 >= hsvImage[i][j][0] and 60 <= hsvImage[i][j][1] and 255 >= hsvImage[i][j][1] and 60 <= hsvImage[i][j][2] and 255 >= hsvImage[i][j][0]:
    #            blankImage[i][j] = 255
                     
    #threshold = cv2.inRange(hsvImage, (65, 60, 60), (85, 255, 255))
    
    GB = cv2.GaussianBlur(threshold,(5,5), cv2.BORDER_DEFAULT)
    
    #applying Harris Corner
    #dst = cv2.cornerHarris(GB, 2, 3, 0.04)
    #dst = cv2.dilate(dst, None)
    #image[dst>0.01*dst.max()] = [0, 0, 255]
    
    #applying Shi_tomasi method
    corners = cv2.goodFeaturesToTrack(GB, 7, 0.01, 10)
    try:
        corners = np.int0(corners)
    except:
        return image
    #print(corners)
    
    ((cx,cy), radius) = cv2.minEnclosingCircle(corners)
    image = cv2.circle(image, (int(cx),int(cy)), 2, (0, 0, 255), 2)
    
    x_coord = []
    y_coord = []
    for i in corners:
        x, y = i.ravel()
        x_coord.append(x)
        y_coord.append(y)
        cv2.circle(image, (x,y), 2, (0, 0, 255), 2)
        
    x_diff = abs(max(x_coord) - min(x_coord))
    y_diff = abs(max(y_coord) - min(y_coord))
    pointsWithin = 0
    if y_diff > x_diff:
        #cv2.putText(image, "up/Down", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        #to check if lies within up
        y_diff = abs(int(cy)-min(y_coord))
        Area_of_side = x_diff * y_diff
        
        for i in range(0, len(x_coord)):
            Area_sum = (0.5)*(x_diff)*abs(y_coord[i]-int(cy)) + (0.5)*(x_diff)*abs(y_coord[i]-min(y_coord)) + (0.5)*(y_diff)*abs(x_coord[i]-min(x_coord)) + (0.5)*(y_diff)*abs(max(x_coord)-x_coord[i])
    
            if Area_sum <= Area_of_side:
                pointsWithin = pointsWithin + 1
        
        if pointsWithin > 3:
            cv2.putText(image, "Orientation: UP", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Orientation: DOWN", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        
        #to check if lies within left
        X_diff = abs(int(cx)-min(x_coord))
        Area_of_side = x_diff * y_diff
        
        for i in range(0, len(x_coord)):
            Area_sum = (0.5)*(x_diff)*abs(max(y_coord)-y_coord[i]) + (0.5)*(x_diff)*abs(y_coord[i]-min(y_coord)) + (0.5)*(y_diff)*abs(x_coord[i]-min(x_coord)) + (0.5)*(y_diff)*abs(int(cx)-x_coord[i])
            
            if Area_sum <= Area_of_side:
                pointsWithin = pointsWithin + 1
        
        if pointsWithin > 3:
            cv2.putText(image, "Orientation: LEFT", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Orientation: RIGHT", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
     
    return image
    
#cv2.drawContours(image, contours
# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('greenArrow.avi', fourcc, 10, (640, 480))
# write frame to video file

#to write time delta in a file
#file = open('hw3data.txt','a')

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    # grab the current frame
    start = datetime.datetime.now()
    
    image = frame.array
    image = cv2.rotate(image, cv2.ROTATE_180)
    
    processedImage = detectOBI(image)
    out.write(processedImage)
    
    # show the frame to our screen
    cv2.imshow("Frame", processedImage)
    
    end = datetime.datetime.now()
    delta = end - start
    #print(str(delta))
    
    #file.write(str(delta.total_seconds())+'\n')
    
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # press the 'q' key to stop the video stream
    if key == ord("q"):
        break
    
#cv2.waitKey(0)
#cv2.destroyAllWindows()
