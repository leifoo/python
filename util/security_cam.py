import cv2
from datetime import datetime

dir = '/home/lxf470/Downloads/security_cam/'

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

start = True
prev_motion = False

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
        if start:
            start = False
        else:
            # print(str(datetime.now().strftime('%Y%m%d-%H%M%S')))

            if not prev_motion:
                print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}: Start recording')
                # Below VideoWriter object will create 
                # a frame of above defined The output  
                # is stored in 'filename.avi' file. 
                result = cv2.VideoWriter(dir+str(datetime.now().strftime('%Y%m%d-%H-%M-%S'))+'.avi',  
                                        cv2.VideoWriter_fourcc(*'MJPG'), 
                                        20, size) 

            # Write the frame into the 
            # file 'filename.avi' 
            result.write(frame) 
            prev_motion = True
    else:
        if prev_motion:
            print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}: Save video')
            print('-'*20)

            # release video write objects 
            result.release() 
        prev_motion = False 

    cv2.imshow('Motion Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()