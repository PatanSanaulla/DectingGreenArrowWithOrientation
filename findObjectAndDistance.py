import cv2
import os
import RPi.GPIO as gpio
import time

# Define pin alloc
trig = 16
echo = 18

def distance():
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    
    #Ensure outout has no value
    gpio.output(trig, False)
    time.sleep(0.01)

    #Generate Trigger oulse
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    #Generate Echo time signal
    while gpio.input(echo) == 0:
        pulse_start = time.time()

    while gpio.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    #Convert time to distance
    distance = pulse_duration*17150
    distance = round(distance, 2)
        
    #clear the output pins
    gpio.cleanup()
        
    return distance


command = 'sudo modprobe  bcm2835-v4l2'
os.system(command)

#open video capture
cap = cv2.VideoCapture(0) # 0 for first camera

while True:
    check, img = cap.read() #check is a bool
    
    img = cv2.rotate(img, cv2.ROTATE_180)
    
    distance_sum = 0;
    for i in range(0,10):
        distance_sum = distance_sum + distance()
    
    avg_distance = distance_sum / 10
    
    cv2.putText(img, "Distance : "+str(avg_distance)+"cm", (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
      
    #show result to screen
    cv2.imshow("Distance Measurement",img)

    #Break out of the loop by q key
    if(cv2.waitKey(1) == ord("q")):
        cv2.imwrite("objectAndDistance.jpg", img)
        break

cap.release()
cv2.destroyAllWindows()