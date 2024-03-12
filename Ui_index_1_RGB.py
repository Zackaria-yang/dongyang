# coding:UTF-8
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from show import Ui_MainWindow
import numpy as np
import time
import gc
import os
from test import Detect
from mydetect import Segmodel
from result import *
from tcp_connect import TcpConnect
import PIL.Image as Image

sys.path.append(os.getcwd())
class MainWindow(Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.a = A()
        self.setWindowTitle("YunLuTeam-3D-First")

        self.timer = QtCore.QTimer(self)
        self.result = ''                                                       # 初始化？
        self.resultList = []
        self.rgb_count=0
        self.state_free()                                                      #显示设备空闲状态

        self.pushButton.clicked.connect(self.start_detect)                     #链接函数开始检测
        self.statementLabel.setAlignment(QtCore.Qt.AlignCenter)                #按钮参数的设置
        self.resultWidget.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setVisible(False)
        self.pushButton_2.clicked.connect(self.close)                          #关闭程序

        # self.showtimer = QtCore.QTimer()                                       #启动QT的计时器
        # self.showtimer.timeout.connect(self.showimg)                           #计时器时间到后启动相机
        # self.showtimer.start(30)                                               #设置计时器时间

        # self.model = MainModel()                           #实例化MainModel,同时加载分割模型和检测模型      modle_main_1_RGB中的函数
        self.img_pth = 'result_image/detect_img.png'       #设置图像保存路径,同时也是待检测的图片

        # self.cap = self.model.camera # 实例化摄像头
        # self.judge_ip = '127.0.0.1'                                             #裁判系统的IP地址
        gc.collect()                                                            #Python使用gc模块进行垃圾回收



    # def showimg(self):
    #     self.showWidget.setScaledContents(True)
    #     self.showWidget.setPixmap(QtGui.QPixmap('bs1/rond1/UIdemo3/r_images/{}.png'.format(camera.rgb_count - 1)))
    def showimg(self):
        self.showWidget.setScaledContents(True)
        self.showWidget.setPixmap(QtGui.QPixmap('r_images/0.png'))
    def showresimg(self):
        self.showWidget.setScaledContents(True)
        self.showWidget.setPixmap(QtGui.QPixmap('res_images/yolo2.png'))
    #   彩色图像转化成为Qimg图像
    # def ndarray2qimg(self, frame: np.ndarray) -> QtGui.QPixmap:
    #      image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_RGB888)
    #      pix = QtGui.QPixmap(image).scaled(640, 480)
    #      return pix                                                                    
    # 获取图像并显示
    # def camera(self) -> np.ndarray:
    #     color_image, _ = self.cap.capture_img(depth=True)
    #     color_image = cv2.resize(color_image, (640, 480))
    #     color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    #     return color_image

    def imagevisible(self):
        self.image.setVisible(False)

    # def signal(self)-> None:  # 接收显示转动图标信号
    #     self.state_rotate()
    #     self.timer.setInterval(5000)
    #     self.timer.start()
    #     self.image.setVisible(True)
    #     self.timer.timeout.connect(self.imagevisible)                      #时间到后终止图像访问

    def state_free(self):                                                  
        # print("空闲")
        self.statementLabel.setText("空闲")
        self.statementLabel.repaint()

    def state_detect(self):
        self.statementLabel.setText("检测中")
        self.statementLabel.repaint()

    def photo(self):
        self.statementLabel.setText("拍照中")
        self.statementLabel.repaint()

    def state_detect_end(self):
        self.statementLabel.setText("检测结束")
        self.statementLabel.repaint()

    def state_rotate(self):
        self.statementLabel.setText("转动中")
        self.statementLabel.repaint()

    # 检测槽函数
    def start_detect(self):
        
        # self.tcp_connect = TcpConnect(judge_ip=self.judge_ip)
        # frame, _ = self.cap.capture_img(depth=True)
        # self.tcp_connect.send_team_info('CSUPER-VISION')
        # cv2.imwrite(self.img_pth, frame) #保存待检测结果
        #设置标签为空闲中


        tcp_connect = TcpConnect(judge_ip = '127.0.0.1')
        print('connect successful!')
        l = tcp_connect.send_team_info('YunLuTeam')


        start = time.time()
        # self.photo()
        # camera.take_rgb_photo('bs1/rond1/UIdemo3/r_images')
        # camera.dele()
        self.showimg()
        self.state_detect()                                                     #设置标签为空闲中
        #os.mkdir(save_dir)      dao shi hou  zai zhuo mian  sheng cheng wen jian jia
        txt = []

        raw_path = 'r_images/0.png'
        """SEG"""
        seg_result_path =  'res_images/seg.png'
        mask1_path = 'res_images/mask1.png'
        mask2_path = 'res_images/mask2.png'
        yolo1_path = 'res_images/yolo1.png'
        yolo2_path = 'res_images/yolo2.png'


        seg_result = seg.detect(raw_path,seg_result_path)

        # seg_result = cv2.cvtColor(seg_result, cv2.COLOR_BGR2RGB)
        # seg_result_path = 'bs1/rond1/UIdemo3/seg_images/{}.png'.format(self.rgb_count+1)
        # cv2.imwrite(seg_result_path,seg_result)

        img = seg.mask(seg_result_path, mask1_path)  # 将分割结果转换为二值图/mask，掩膜1
        time2 = time.time()
        img = Image.open(mask1_path).convert('L')
        img = np.array(img)
        img = seg.largeConnectComponent(img)  # 求mask的最大连通域
        mask = Image.fromarray(img)
        mask.save(mask2_path)  # 保存最大连通域的mask
        rgb = Image.open(raw_path)  # rgb是原图
        mask = Image.open(mask2_path)
        mask_np = np.array(mask)

        seg_img = (np.expand_dims(mask_np != 0, -1) * np.array(rgb, np.float32)).astype('uint8')  # 将原图和mask相乘,得到分割结果
        image = Image.fromarray(np.uint8(seg_img))
        image.save(yolo1_path)  # 保存桌面最大连通分割结果
        time3 = time.time()
        print('large connect time is:', time3 - time2)

        """YOLO"""

        res = yolo.YoloDetect(yolo1_path)  # 对分割好的最大连通域进行检测  ,res是result[0]
        print("yolo finished")
        yolo.SaveResult(yolo2_path, res)  # 保存检测结果
        print("save finished")
        time11 = time.time()
        print('time yolo is:', time11 - time3)
        _, detect_object_class_label, detect_object_xxyy = detect_result_del(res)
        print("del ok")
        result_txt,_ = result_txt_generate(detect_object_class_label)
        print("result ok")
        txt.append(detect_object_class_label)
        path_txt ='1.txt'
        f = open('CSU-YunLuTeam-R1.txt', 'w')
        f.write(result_txt)
        f.close()

        print("txt ok")
        #
        # """SEG"""
        # seg_result_path =  'bs1/rond1/UIdemo3/r_images/{}.png'.format(2)
        # seg_result = seg.detect(seg_result_path)
        # seg_result = cv2.cvtColor(seg_result, cv2.COLOR_BGR2RGB)
        # seg_result_path = 'bs1/rond1/UIdemo3/seg_images/{}.png'.format(2)
        # cv2.imwrite(seg_result_path,seg_result)
        #
        #
        # # '''MASK'''
        # # path_mask = 'bs1/rond1/UIdemo3/bind_images/bind.png'
        # # mask_path =  '/home/shuaige/Desktop/measure/pyorbbecsdk/seg_images/mask.png'
        # # img = Image.open(path_mask).convert('L') #mask
        # # img = np.array(img)
        # # img = seg.largeConnectComponent(img)
        # # mask = Image.fromarray(img)
        # # mask.save(mask_path)
        # # rgb = Image.open(seg_result_path)
        # # mask = Image.open(mask_path)
        # # mask_np = np.array(mask)
        # # seg_img = (np.expand_dims(mask_np != 0, -1) * np.array(rgb, np.float32)).astype('uint8')
        # # image = Image.fromarray(np.uint8(seg_img))
        # # image .save(seg_result_path)
        #
        # """YOLO"""
        # result_path ='bs1/rond1/UIdemo3/res_images/{}.png'.format(2)
        # path=  'bs1/rond1/UIdemo3/seg_images/{}.png'.format(2)
        # res = yolo.YoloDetect(path)
        # yolo.SaveResult(result_path,res)
        # _, detect_object_class_label, detect_object_xxyy = detect_result_del(res)
        # result_txt,_ = result_txt_generate(detect_object_class_label)
        # txt.append(detect_object_class_label)
        # path_txt ='bs1/rond1/UIdemo3/txt/{}.txt'.format(2)
        # f = open(path_txt, 'w')
        # f.write(result_txt)
        # f.close()

        # end_num = num_1(txt)
        # print("num1 ok")
        # print(end_num, type(end_num), len(end_num))
        # end_txt,end_txt1 = result_txt_generate(end_num)
        # print(end_txt)
        # print("............")
        # print(end_txt1)
        # f = open('CSU-YunLuTeam-R1.txt', 'w')
        # f.write(end_txt)
        # f.close()


        l = tcp_connect.send_detect_result(result_txt)
        tcp_connect.close()


        """XUAN ZHUAN"""
        # self.image.setPixmap(QtGui.QPixmap('/home/shuaige/Desktop/UIdemo/arrow.png'))
        # self.state_rotate()
        # time.sleep(3)
        # self.image.setPixmap(QtGui.QPixmap(''))


        self.showresimg()
        # self.result = self.model.detect_and_seg(self.img_pth)
        self.show_result(_)
        print(result_txt)
        end = time.time()
        print(end -start)
        #获取一帧图像并传送给检测函数
        # 此处完成所有操作,包括发送队伍头信息,检测,分割,发送检测结果
        # self.result = self.model.result_txt_generate(self.result)
        # self.tcp_connect.send_detect_result(self.result)
        #time.sleep(3)
        print(self.result)
        #设置标签为检测完成
        self.state_detect_end()                                                 #设置标签为检测结束
        # self.tcp_connect.close()             

    def show_result(self,txt):                                                    #结果显示函数
        #将结果显示出来\
        print(txt)
        self.resultWidget.setText(txt)
        # self.result = txt
        # print("self.result:",self.result)
        # self.resultList = self.result.split('\r', -1)
        # # print(self.result)
        # for res in self.resultList:
        #     self.result = self.result + res + '\n'
        # self.resultWidget.setText(self.result)


if __name__ == '__main__':
    # camera =  Camera()
    seg = Segmodel(cuda=False, weights='segformer/best_epoch_weights.pth', mix_type=2)
    seg.init_model()
    yolo = Detect()

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)                                     #封装成一个app？？
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
