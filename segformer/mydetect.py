import time
import numpy as np
from PIL import Image
import os
from .segformer_main import SegFormer_Segmentation

# if os.getcwd().endswith('\segformer'):
#     from segformer_main import SegFormer_Segmentation
# else:
#     from .segformer_main import SegFormer_Segmentation

import cv2

'''
predict.py有几个注意点
1、该代码无法直接进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
具体流程可以参考get_miou_prediction.py，在get_miou_prediction.py即实现了遍历。
2、如果想要保存，利用r_image.save("img.jpg")即可保存。
3、如果想要原图和分割图不混合，可以把blend参数设置成False。
4、如果想根据mask获取对应的区域，可以参考detect_image函数中，利用预测结果绘图的部分，判断每一个像素点的种类，然后根据种类获取对应的部分。
seg_img = np.zeros((np.shape(pr)[0],np.shape(pr)[1],3))
for c in range(self.num_classes):
    seg_img[:, :, 0] += ((pr == c)*( self.colors[c][0] )).astype('uint8')
    seg_img[:, :, 1] += ((pr == c)*( self.colors[c][1] )).astype('uint8')
    seg_img[:, :, 2] += ((pr == c)*( self.colors[c][2] )).astype('uint8')
'''

class Segmodel():
    def __init__(self, weights, cuda=False, mix_type=2):
        #初始化模型
        self.seg = SegFormer_Segmentation(weights=weights ,cuda=cuda, mix_type=mix_type, input_shape=[512, 512])

    def init_model(self):
        print("begin load seg model")
        self.seg.init_model()
        print("seg model load successful")

    def detect(self, img):
        #传入参数img改为ndarray
        image = Image.open(img)
        # print(image)
        t1 = time.time()
        r_image = self.seg.detect_image(image=image)
        print("seg time:",time.time()-t1)
        return np.array(r_image)

if __name__ == "__main__":
    img = 'img/2.png'
    path =' 22.png'
    segmodel = Segmodel(cuda=False, weights='/home/shuaige/Desktop/3D/segformer/best_epoch_weights.pth', mix_type=2)
    segmodel.init_model()  
    seg_result = segmodel.detect('/home/shuaige/Desktop/UIdemo/2.png')
    seg_result = cv2.cvtColor(seg_result, cv2.COLOR_BGR2RGB)
    cv2.imshow("seg result",seg_result)
    cv2.imwrite(path,seg_result)
    # cv2.waitKey(0)
    