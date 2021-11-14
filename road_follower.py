import time
import cv2
import sys
import numpy as np
sys.path.append('/home/jetbot/jetbot/')
from jetbot import Camera


def main():
    cap = Camera.instance(
        width=416,
        height=416,
        fps=120,
        capture_width=1280,
        capture_height=720
    )
    threshold = 100
    x_last = 0
    y_last = 0
    while True:
        image = cap.value
        #image = image[300:415, :]  # Region Of Interest
        Blackline = cv2.inRange(image, (0,0,0), (threshold,threshold,threshold))	
        kernel = np.ones((3,3), np.uint8)
        Blackline = cv2.erode(Blackline, kernel, iterations=5)
        Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
        contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        contours_blk_len = len(contours_blk)
        if contours_blk_len > 0 :
            if contours_blk_len == 1 :
                blackbox = cv2.minAreaRect(contours_blk[0])
            else:
                canditates=[]
                off_bottom = 0	   
                for con_num in range(contours_blk_len):		
                    blackbox = cv2.minAreaRect(contours_blk[con_num])
                    (x_min, y_min), (w_min, h_min), ang = blackbox		
                    box = cv2.boxPoints(blackbox)
                    (x_box,y_box) = box[0]
                    if y_box > 358 :		 
                        off_bottom += 1
                    canditates.append((y_box,con_num,x_min,y_min))		
                canditates = sorted(canditates)
                if off_bottom > 1:	    
                    canditates_off_bottom=[]
                    for con_num in range ((contours_blk_len - off_bottom), contours_blk_len):
                        (y_highest,con_highest,x_min, y_min) = canditates[con_num]		
                        total_distance = (abs(x_min - x_last)**2 + abs(y_min - y_last)**2)**0.5
                        canditates_off_bottom.append((total_distance,con_highest))
                    canditates_off_bottom = sorted(canditates_off_bottom)         
                    (total_distance,con_highest) = canditates_off_bottom[0]         
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])	   
                else:		
                    (y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]		
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])	 
            (x_min, y_min), (w_min, h_min), ang = blackbox
            x_last = x_min
            y_last = y_min
            if ang < -45 :
                ang = 90 + ang
            if w_min < h_min and ang > 0:	  
                ang = (90-ang)*-1
            if w_min > h_min and ang < 0:
                ang = 90 + ang	  
            setpoint = 350
            error = int(x_min - setpoint) 
            ang = int(ang)	 
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,255),3)	 
            cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image,str(error),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.line(image, (int(x_min),0 ), (int(x_min),50 ), (255,0,0),3)
            cv2.circle(image, (208, 50), 5, (0,255,0), 3)
            cv2.circle(image, (int(x_min), int(y_min)), 5, (0,155,155), 3)
            cv2.circle(image, (int(x_min-(w_min/2)), int(y_min-(h_min/2))), 5, (0,155,155), 3)
        cv2.imshow("Test", image)
        key = cv2.waitKey(1) & 0xFF	
        if key == ord("q"):
            break
    cap.stop()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    main()
