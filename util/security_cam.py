import os
import cv2
from datetime import datetime

dt_min = 1
t_start = None
t_end = None
dir = '/home/lxf470/Downloads/security_cam/'
video_file = None
initial = True
prev_motion = False

cap = cv2.VideoCapture(0)

# We need to check if camera is opened previously or not 
if (cap.isOpened() == False):  
    print("Error reading video file") 

mog = cv2.createBackgroundSubtractorMOG2()
  
# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height) 

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    fgmask = mog.apply(gray)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) < 1000:
            continue
        
        # # Draw bounding box around contour
        # x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    if contours:
        if initial:
            initial = False
        else:          
            if not prev_motion:
                t_start = datetime.now()
                print(f'{t_start.strftime("%Y/%m/%d %H:%M:%S")}: Start recording')

                video_file = dir+str(t_start.strftime('%Y%m%d-%H-%M-%S'))+'.avi'
                # VideoWriter object will create a frame stored in 'filename.avi' file. 
                result = cv2.VideoWriter(video_file,
                                        cv2.VideoWriter_fourcc(*'MJPG'), 
                                        30, size) 

            # Write the frame into the file 
            result.write(frame) 
            prev_motion = True
    else:
        if prev_motion:
            
            # release video write objects 
            result.release() 

            t_end = datetime.now()
            print(f'Motion duration {(t_end - t_start).total_seconds()}')

            if (t_end - t_start).total_seconds() > 1:
                print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}: Save video')
                print('-'*20)
            else:
                os.remove(video_file)

        prev_motion = False 

    cv2.imshow('Motion Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()