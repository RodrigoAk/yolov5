import time
import cv2
import sys
import numpy as np
import ipywidgets
sys.path.append('/home/jetbot/jetbot/')
from jetbot import Camera
from jetbot import Robot


class RoadFollower:
    def __init__(self, x_last=208, y_last=208, speed=0.4, Kp=1.25, Kd=0.75,
                 Ki=0, setpoint=0):
        self.x_last = x_last
        self.y_last = y_last
        self.angle = 0.0
        self.angle_last = 0.0
        self.speed = min(speed, 1.0)
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.setpoint = setpoint
        self.acc_error = 0
        self.start_sliders()
        self.start_robot()

    def start_robot(self):
        self.robot = Robot()
        self.robot.stop()

    def start_sliders(self):
        self.steering_bias_slider = ipywidgets.FloatSlider(min=0, max=1.0, value=0.0, description='steering bias')

        self.x_slider = ipywidgets.FloatSlider(min=-1.0, max=1.0, description='x')
        self.y_slider = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='y')
        self.steering_slider = ipywidgets.FloatSlider(min=-1.0, max=1.0, description='steering')
        self.speed_slider = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='speed')
        self.angle_slider = ipywidgets.FloatSlider(min=-10, max=+10, description='angle')

        self.left_motor = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='left motor')
        self.right_motor = ipywidgets.FloatSlider(min=0, max=1.0, orientation='vertical', description='right motor')

    def display_control_sliders(self):
        display(
            self.steering_bias_slider
        )

    def display_monitor_sliders(self):
        display(self.y_slider, self.speed_slider)
        display(self.x_slider, self.steering_slider, self.angle_slider)
        display(self.left_motor, self.right_motor)

    def execute(self, image, pred):
        """
        Parameters
        ----------
        image: numpy.array
            Image retrieved from the camera
        pred: list
            List containing objects found by your model in the image

        Returns
        -------
        image: numpy.array
            Image processed used for the PID control
        error: float
            Error calculated for the PD control
        """
        factor = 1
        if len(pred['person']) > 0:
            print("REDUCE ROBOTO!!!")
            max_width = np.asarray(pred['person']).max()
            factor = 0 if max_width >= 0.5 else (-2 * max_width + 1)
            # return image, self.angle_last

        xy, image = self.update(image)
        x, y = xy[0], xy[1]

        self.x_slider.value = x
        self.y_slider.value = y

        self.speed_slider.value = max(self.speed * factor, 0.3)

        self.angle = np.arctan2(x, y) - self.setpoint
        self.acc_error += self.angle
        self.acc_error = min(self.acc_error, 100.0) if self.acc_error >= 0 else max(self.acc_error, -100.0)
        pid = self.angle * self.Kp\
              + (self.angle - self.angle_last) * self.Kd\
              + self.acc_error * self.Ki
        self.angle_last = self.angle
        self.angle_slider.value = self.angle

        self.steering_slider.value = pid + self.steering_bias_slider.value

        self.robot.left_motor.value = max(
            min(self.speed_slider.value + self.steering_slider.value,  0.5),
            0.0
        )
        self.robot.right_motor.value = max(
            min(self.speed_slider.value - self.steering_slider.value, 0.5),
            0.0
        )
        self.left_motor.value = max(
            min(self.speed_slider.value + self.steering_slider.value,  0.5),
            0.0
        )
        self.right_motor.value = max(
            min(self.speed_slider.value - self.steering_slider.value,  0.5),
            0.0
        )
        return image, self.angle

    def update(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        roi = [[300,-1],[50,-50]]
        image = image[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]]
        # (thresh, image) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        (thresh, image) = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
        Blackline = cv2.inRange(image, 0, thresh)
        kernel = np.ones((3,3), np.uint8)
        Blackline = cv2.erode(Blackline, kernel, iterations=5)
        Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
        contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        x = 0
        y = 0
        contours_blk_len = len(contours_blk)
        if contours_blk_len > 0 :
            if contours_blk_len == 1 :
                blackbox = cv2.minAreaRect(contours_blk[0])
                (x, y), (w_min, h_min), ang = blackbox
            else:
                for c in contours_blk:
                    blackbox = cv2.minAreaRect(c)
                    (x_min, y_min), (w_min, h_min), ang = blackbox
                    x += x_min
                    y += y_min
                x = x / contours_blk_len
                y = y / contours_blk_len
            self.x_last = x
            self.y_last = y
            box = cv2.boxPoints(blackbox)
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,0),3)
            cv2.circle(image, (image.shape[1]//2, image.shape[0]//2), 5, (0,0,0), 3)
            cv2.circle(image, (int(x), int(y)), 5, (255,255,255), 3)
            xy = [
                (x - image.shape[1]/2.0) / (image.shape[1]/2.0),
                -(y - image.shape[0]) / image.shape[0]
            ]
        else:
            xy = [
                (self.x_last - image.shape[1]/2.0) / (image.shape[1]/2.0),
                -(self.y_last - image.shape[0]) / image.shape[0]
            ]
            return xy, image
        return xy, image
