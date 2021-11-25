import time
import cv2
import sys
import numpy as np
import ipywidgets
sys.path.append('/home/jetbot/jetbot/')
from jetbot import Camera


class RoadFollower:
    def __init__(self, x_last=0, y_last=0, threshold=100):
        self.x_last = x_last
        self.y_last = y_last
        self.setpoint = (0.5, 0.5)
        self.threshold = threshold
        self.angle = 0.0
        self.angle_last = 0.0
        self.start_sliders()
        # self.start_robot()

    # def start_robot(self):
    #     self.robot = Robot()

    def start_sliders(self):
        self.speed_gain_slider = ipywidgets.FloatSlider(min=0.0, max=1.0, step=0.01, description='speed gain')
        self.steering_gain_slider = ipywidgets.FloatSlider(min=0.0, max=1.0, step=0.01, value=0.2, description='steering gain')
        self.steering_dgain_slider = ipywidgets.FloatSlider(min=0.0, max=0.5, step=0.001, value=0.25, description='steering kd')
        self.steering_bias_slider = ipywidgets.FloatSlider(min=-0.3, max=0.3, step=0.01, value=0.0, description='steering bias')

        self.x_slider = ipywidgets.FloatSlider(min=-1.0, max=1.0, description='x')
        self.y_slider = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='y')
        self.steering_slider = ipywidgets.FloatSlider(min=-1.0, max=1.0, description='steering')
        self.speed_slider = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='speed')

        self.left_motor = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='left motor')
        self.right_motor = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='right motor')

    def display_control_sliders(self):
        display(
            self.speed_gain_slider,
            self.steering_gain_slider,
            self.steering_dgain_slider,
            self.steering_bias_slider
        )

    def display_monitor_sliders(self):
        display(self.y_slider, self.speed_slider)
        display(self.x_slider, self.steering_slider)
        display(self.left_motor, self.right_motor)

    def execute(self, image):
        xy, image = self.update(image)
        # image = change['new']
        # xy = model(preprocess(image)).detach().float().cpu().numpy().flatten()
        x = xy[0]
        y = (0.5 - xy[1]) / 2.0

        self.x_slider.value = x
        self.y_slider.value = y

        self.speed_slider.value = self.speed_gain_slider.value

        self.angle = np.arctan2(x, y)
        pid = self.angle * self.steering_gain_slider.value\
              + (self.angle - self.angle_last) * self.steering_dgain_slider.value
        self.angle_last = self.angle

        self.steering_slider.value = pid + self.steering_bias_slider.value

        # robot.left_motor.value = 
        self.left_motor.value = max(
            min(self.speed_slider.value + self.steering_slider.value, 1.0),
            0.0
        )
        self.right_motor.value = max(
            min(self.speed_slider.value - self.steering_slider.value, 1.0),
            0.0
        )
        return image

    def update(self, image):
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        roi = [[250,-1],[0,-1]]
        image = image[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]]
        # image = image[300:415, :]  # Region Of Interest
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(image.shape)
        (thresh, image) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Blackline = cv2.inRange(image, (0,0,0), (self.threshold,self.threshold,self.threshold))
        Blackline = cv2.inRange(image, 0, thresh)
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
                        total_distance = (abs(x_min - self.x_last)**2 + abs(y_min - self.y_last)**2)**0.5
                        canditates_off_bottom.append((total_distance,con_highest))
                    canditates_off_bottom = sorted(canditates_off_bottom)         
                    (total_distance,con_highest) = canditates_off_bottom[0]         
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])	   
                else:		
                    (y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]
                    blackbox = cv2.minAreaRect(contours_blk[con_highest])
            (x_min, y_min), (w_min, h_min), ang = blackbox
            self.x_last = x_min
            self.y_last = y_min
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,0),3)
            cv2.line(image, (int(x_min),0 ), (int(x_min),50 ), (0,0,0),3)
            cv2.circle(image, (image.shape[1]//2, image.shape[0]//2), 5, (0,0,0), 3)
            cv2.circle(image, (int(x_min), int(y_min)), 5, (255,255,255), 3)
            xy = [(x_min - image.shape[1]/2.0) / image.shape[1], (y_min - image.shape[0]/2.0) / image.shape[0]]
        else:
            xy = [0.0, 0.0]
        return xy, image