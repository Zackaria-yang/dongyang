from ultralytics import YOLO
import cv2


class Detect:
    def __init__(self):
        self.model = YOLO("best.pt", task='detect')

    def YoloDetect(self,path):
        results = self.model.predict(source=path,save=True, save_txt=True, save_conf=True)
        return results[0]

    def SaveResult(self,path,res):
        file = open ('yolo_result.txt',mode = 'w',encoding = 'utf-8')
        file.write(str(res.boxes.xyxy))
        file.write(str(res.boxes.cls))
        cv2.imwrite(path,res.plot())


# yolo = Detect()
# result_path = '/home/shuaige/Desktop/3D/yolov8/1.png'
# path = '/home/shuaige/Desktop/ultralytics-main/img_0.png'
# res = yolo.YoloDetect(path)
# yolo.SaveResult(result_path,res)
# _, detect_object_class_label, detect_object_xxyy = detect_result_del(res)
# print(detect_object_class_label)
# result_txt = result_txt_generate(detect_object_class_label)
# path_txt ='/home/shuaige/Desktop/0.txt'
# f = open(path_txt, 'w')
# f.write(result_txt)
# f.close()
