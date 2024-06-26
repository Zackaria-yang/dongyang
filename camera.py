import copy
from pyorbbecsdk import *
import cv2
import numpy as np
from utils import frame_to_bgr_image
import os
import argparse
import time

class Camera:
    def __init__(self):
        self.pipeline = Pipeline()
        self.config = Config()
        self.saved_color_cnt: int = 0
        self.rgb_count = 0
        self.has_color_sensor = False
        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            if profile_list is not None:
                color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(1920, 0, OBFormat.RGB,30)   #ke yi tiao fen bian  lv
                
                self.config.enable_stream(color_profile)
                self.has_color_sensor = True
        except OBError as e:
            print(e)
        self.pipeline.start(self.config)

    def take_rgb_photo(self, save_path):
        """
        拍一张rgb图片
        :param save_path: 图片保存文件夹路径
        :return: None
        """
        #self.pipeline.start(self.config)
        while True:
            frames = self.pipeline.wait_for_frames(100)
            if frames is None:
                print('color frame is None!')
                continue
            if self.has_color_sensor:
                if self.saved_color_cnt >= 2:  # how many rgb 
                    break
            try:
                color_frame = frames.get_color_frame()
                if color_frame is not None and self.saved_color_cnt < 2:  # how many rgb 
                    self.save_color_frame(color_frame, self.rgb_count, save_path)
                    # print(filename)
                    self.saved_color_cnt += 1
                    self.rgb_count += 1
                    time.sleep(0.7)
            except KeyboardInterrupt:
                break

    def take_rgb_photo2(self, save_path):
        """
        拍一张rgb图片
        :param save_path: 图片保存文件夹路径
        :return: None
        """
        self.pipeline.start(self.config)
        while True:
            frames = self.pipeline.wait_for_frames(100)
            if frames is None:
                print('color frame is None!')
                continue
            if self.has_color_sensor:
                if self.saved_color_cnt >= 4:  # how many rgb 
                    break
            try:
                color_frame = frames.get_color_frame()
                if color_frame is not None and self.saved_color_cnt < 4:  # how many rgb 
                    self.save_color_frame(color_frame, self.rgb_count, save_path)
                    # print(filename)
                    self.saved_color_cnt += 1
                    self.rgb_count += 1
                    time.sleep(0.7)
            except KeyboardInterrupt:
                break

    def take_rgb_photo3(self, save_path):
        """
        拍一张rgb图片
        :param save_path: 图片保存文件夹路径
        :return: None
        """
        self.pipeline.start(self.config)
        while True:
            frames = self.pipeline.wait_for_frames(100)
            if frames is None:
                print('color frame is None!')
                continue
            if self.has_color_sensor:
                if self.saved_color_cnt >= 6:  # how many rgb 
                    break
            try:
                color_frame = frames.get_color_frame()
                if color_frame is not None and self.saved_color_cnt < 6:  # how many rgb 
                    self.save_color_frame(color_frame, self.rgb_count, save_path)
                    # print(filename)
                    self.saved_color_cnt += 1
                    self.rgb_count += 1
                    time.sleep(0.7)
            except KeyboardInterrupt:
                break
        
        
    
    # def take_rgb_photo(self, save_path):
    #     """
    #     拍一张rgb图片
    #     :param save_path: 图片保存文件夹路径
    #     :return: None
    #     """
    #     while True:
    #         frames = self.pipeline.wait_for_frames(100)
    #         if frames is None:
    #             print('color frame is None!')
    #             continue
    #         else:
    #             color_frame = frames.get_color_frame()
    #             if color_frame is not None:
    #                 self.current_img_path = self.save_color_frame(color_frame, self.rgb_count, save_path)
    #                 self.rgb_count += 1
    #                 break
    #             else:
    #                 continue
    #     return self.current_img_path





    def save_color_frame(self, frame: ColorFrame, index, save_dir):
        if frame is None:
            return
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        filename = save_dir + "/{}.png".format(index)
        image = frame_to_bgr_image(frame)
        if image is None:
            print("failed to convert frame to image")
            return
        cv2.imwrite(filename, image)

    def dele(self):
        self.pipeline.stop()



if __name__ == '__main__':
    camera = Camera()
    camera.take_rgb_photo('./r_images')
    data = camera.take_depth_photo('./d_images')
    cv2.imshow('img', data)
    cv2.waitKey(0)
